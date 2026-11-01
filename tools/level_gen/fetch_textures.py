"""Скачивает текстуры CC0 с OpenGameArt (Screaming Brain Studios, Tiny Texture Pack 1–3)
и кладёт выбранные в world/textures под понятными именами."""
import io, os, sys, urllib.request, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "world", "textures")
BASE = "https://opengameart.org/sites/default/files/"
PACKS = ["sbs_-_tiny_texture_pack_-_128x128.zip", "sbs_-_tiny_texture_pack_2_-_128x128.zip",
         "sbs_-_tiny_texture_pack_3_-_small.zip"]
# имя в игре -> имя файла в архиве (без суффикса размера)
PICK = {
    "asphalt": "Metal_17", "sidewalk": "Tile 10", "plaster": "Plaster_15", "plaster_grey": "Plaster_19",
    "plaster_warm": "Plaster_09", "roof": "Roof 16", "roof_slate": "Roof 3", "wood_door": "Wood 19",
    "wood_table": "Wood 9", "wood_fence": "Wood 24", "block_wall": "Brick 7", "metal_rust": "Metal_11",
    "metal_clean": "Metal_09", "concrete": "Stone_07", "concrete_damp": "Stone_05", "concrete_floor": "Stone_08",
    "tablecloth": "Cloth_12", "uniform": "Cloth_17", "tatami": "Weave_05",
}


def main(local_dir: str = "") -> None:
    os.makedirs(OUT, exist_ok=True)
    found = {}
    for pack in PACKS:
        data = open(os.path.join(local_dir, pack), "rb").read() if local_dir else urllib.request.urlopen(BASE + pack).read()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for name in z.namelist():
                base = os.path.basename(name)
                for key, want in PICK.items():
                    if base.startswith(want + "-") or base.startswith(want + " -"):
                        found.setdefault(key, z.read(name))
    for key, blob in found.items():
        open(os.path.join(OUT, key + ".png"), "wb").write(blob)
    missing = sorted(set(PICK) - set(found))
    print("сохранено:", len(found), "нет:", missing)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "")
