"""Генерация всех моделей локаций ПЗМ-3 в .glb для Godot.

Запуск (нужен Blender 4.2+ или pip-пакет bpy):
    python3 build_models.py <папка_вывода>
    # или: blender -b -P build_models.py -- <папка_вывода>

Результат: <папка>/<category>/<name>.glb + manifest.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402
import mg_lib  # noqa: E402
import props_districts  # noqa: E402
import props_gigadom  # noqa: E402
import props_lake  # noqa: E402

MODULES = [props_districts, props_gigadom, props_lake]
if os.environ.get('ONLY_CAT'):
    MODULES = [m for m in MODULES if m.CATEGORY == os.environ['ONLY_CAT']]


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    out_root = os.path.abspath(argv[0] if argv else "models_out")
    only = set(argv[1:])
    manifest = []
    for module in MODULES:
        cat_dir = os.path.join(out_root, module.CATEGORY)
        os.makedirs(cat_dir, exist_ok=True)
        for fn in module.PROPS:
            mg_lib.reset()
            prop = fn()
            if only and prop.name not in only:
                continue
            objs = prop.build()
            main_ob = objs[0]
            path = os.path.join(cat_dir, f"{prop.name}.glb")
            mg_lib.export_glb(objs, path)
            me = main_ob.data
            me.calc_loop_triangles()
            xs = [v.co.x for v in me.vertices]
            ys = [v.co.y for v in me.vertices]
            zs = [v.co.z for v in me.vertices]
            manifest.append({
                "name": prop.name,
                "category": module.CATEGORY,
                "file": f"{module.CATEGORY}/{prop.name}.glb",
                "description": (fn.__doc__ or "").strip().split("\n")[0],
                # размеры в осях Godot: X ширина, Y высота, Z глубина
                "size_m": [round(max(xs) - min(xs), 2), round(max(zs) - min(zs), 2), round(max(ys) - min(ys), 2)],
                "triangles": len(me.loop_triangles),
                "materials": [m.name for m in me.materials],
                "colliders": len(objs) - 1,
            })
            print(f"[ok] {module.CATEGORY}/{prop.name}: {len(me.loop_triangles)} tris")
    mpath = os.path.join(out_root, "manifest.json")
    if os.path.exists(mpath) and os.environ.get("ONLY_CAT"):
        old = [m for m in json.load(open(mpath, encoding="utf-8")) if m["category"] != os.environ["ONLY_CAT"]]
        manifest = old + manifest
    with open(mpath, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print(f"Готово: {len(manifest)} моделей -> {out_root}")


if __name__ == "__main__":
    main()
