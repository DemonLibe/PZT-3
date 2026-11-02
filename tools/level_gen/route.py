"""Маршруты локаций: длинный подход к аномальной зоне и выход за ней.
Районы — змейка дворов между девятиэтажками и гаражный кооператив; Гигадом — лабиринт модулей."""
import random
from tscn import *
from level_common import *

A = "res://assets/models/locations/"
G = "NavigationRegion3D/Geometry"


def model(sc, node_name, path, pos, yaw=0.0, parent="Props"):
    sc.node(node_name, None, parent, instance=sc.ext_res("PackedScene", A + path), transform=T(*pos, yaw=yaw))


def props_root(sc):
    if not any(n[0] == "Props" for n in sc.nodes):
        sc.node("Props", "Node3D", ".")


def sodium_lamp(sc, i, x, z, yaw=0.0):
    model(sc, f"Lamp{i}", "districts/street_lamp_sodium.glb", (x, 0, z), yaw)
    lamp(sc, f"LampLight{i}", (x, 5.6, z), color=(1.0, 0.72, 0.38), energy=1.6, rng=13.0)


def car(sc, name, x, z, yaw, color):
    paint = material(sc, color, tex="metal_clean", scale=1.0)
    glass = material(sc, (0.08, 0.09, 0.11), rough=0.3)
    sc.node(name, "Node3D", "Props", transform=T(x, 0, z, yaw=yaw))
    sc.node("Body", "CSGBox3D", f"Props/{name}", transform=T(0, 0.55, 0), size=V3(1.7, 0.7, 4.0), material=paint, use_collision=True)
    sc.node("Cabin", "CSGBox3D", f"Props/{name}", transform=T(0, 1.15, -0.2), size=V3(1.55, 0.55, 2.1), material=glass, use_collision=True)
    for i, (wx, wz) in enumerate(((-0.8, 1.3), (0.8, 1.3), (-0.8, -1.3), (0.8, -1.3))):
        sc.node(f"Wheel{i}", "CSGCylinder3D", f"Props/{name}", transform=T(wx, 0.3, wz, pitch=90, yaw=90), radius=0.3,
                height=0.2, sides=8, material=material(sc, (0.08, 0.08, 0.08)))


def fence(sc, name, x0, x1, z, mat, h=2.2):
    if x1 - x0 < 0.2:
        return
    box(sc, name, ((x0 + x1) / 2, h / 2, z), (x1 - x0, h, 0.25), mat)


# ---------------- Районы ----------------

def district_route(sc, m, seed, north=True, south=True, exit=True):
    """Подход с юга (змейка) и гаражный кооператив на севере, КПП в конце. Аномальный двор — z от −22 до 21."""
    rng = random.Random(seed)
    props_root(sc)
    lamp_i = 100
    colors = [(0.55, 0.15, 0.12), (0.2, 0.3, 0.45), (0.75, 0.72, 0.6), (0.25, 0.35, 0.25), (0.6, 0.55, 0.2)]
    z_south = 92 if south else 22
    z_north = -82 if north else -22
    # Девятиэтажки по краям всего маршрута
    k = 0
    for side in (-1, 1):
        for z in range(z_north + 6, z_south, 12):
            if -24 < z < 24:
                continue  # там пятиэтажки аномального двора
            k += 1
            model(sc, f"Tower{k}", "districts/panel_building_section.glb", (side * 27, 0, z), 90 if side < 0 else -90)
    for side in (-1, 1):
        box(sc, f"Perimeter{side}", (side * 21.2, 1.6, (z_north + z_south) / 2), (0.4, 3.2, z_south - z_north), m.fence)
    box(sc, "PerimeterSouth", (0, 1.6, z_south), (43, 3.2, 0.4), m.fence)
    if north:
        box(sc, "PerimeterNorth", (0, 1.6, z_north), (43, 3.2, 0.4), m.fence)
    if south:
        spawn(sc, "Player", (0, 0, z_south - 5), 0)
        # Змейка: заборы с проходом то слева, то справа
        gaps = [(70, "left"), (60, "right"), (50, "left"), (40, "right"), (30, "center")]
        for i, (z, where) in enumerate(gaps):
            if where == "left":
                fence(sc, f"Snake{i}", -12.0, 21.0, z, m.fence)
            elif where == "right":
                fence(sc, f"Snake{i}", -21.0, 12.0, z, m.fence)
            else:
                fence(sc, f"Snake{i}a", -21.0, -3.0, z, m.fence)
                fence(sc, f"Snake{i}b", 3.0, 21.0, z, m.fence)
        # Насыщаем каждую полосу змейки
        lanes = [(80, 88), (70, 80), (60, 70), (50, 60), (40, 50), (30, 40), (22, 30)]
        for li, (z0, z1) in enumerate(lanes):
            zc = (z0 + z1) / 2
            sodium_lamp(sc, lamp_i, -18.5 if li % 2 else 18.5, zc, 90 if li % 2 else -90)
            lamp_i += 1
            for ci in range(rng.randint(1, 3)):
                x = rng.uniform(-15, 15)
                if abs(x) < 4 and li in (6,):
                    continue
                car(sc, f"Car{li}_{ci}", x, z0 + 2.2 if ci % 2 else z1 - 2.2, 90 + rng.choice((0, 180)), rng.choice(colors))
            kind = li % 4
            if kind == 0:
                model(sc, f"Swing{li}", "districts/swing_set.glb", (rng.uniform(-8, 8), 0, zc), rng.choice((0, 90)))
                model(sc, f"BenchA{li}", "districts/bench_yard.glb", (rng.uniform(-14, -6), 0, zc + 2.5), 180)
            elif kind == 1:
                for g in range(3):
                    box(sc, f"Garage{li}_{g}", (-19.0 + 0.0, 1.2, z0 + 1.7 + g * 3.0), (3.4, 2.4, 2.9), m.garage)
                model(sc, f"Tree{li}", "districts/tree_lowpoly.glb", (rng.uniform(4, 14), 0, zc), rng.uniform(0, 360))
            elif kind == 2:
                model(sc, f"TreeA{li}", "districts/tree_lowpoly.glb", (rng.uniform(-14, -4), 0, zc), rng.uniform(0, 360))
                model(sc, f"TreeB{li}", "districts/tree_lowpoly.glb", (rng.uniform(4, 14), 0, zc - 2), rng.uniform(0, 360))
                model(sc, f"BenchB{li}", "districts/bench_yard.glb", (rng.uniform(-4, 4), 0, z1 - 1.0), 180)
            else:
                box(sc, f"Bins{li}", (rng.uniform(10, 16), 0.6, zc), (2.4, 1.2, 1.1), m.paint)
                box(sc, f"Sandbox{li}", (rng.uniform(-10, -2), 0.15, zc), (2.5, 0.3, 2.5), m.wood)
    else:
        spawn(sc, "Player", (0, 0, 16.5), 0)
    if north:
        # Гаражный кооператив: ряды гаражей с проходами и тупиками
        rows = [(-30, "right"), (-40, "left"), (-50, "right"), (-60, "left"), (-70, "center")]
        for ri, (z, where) in enumerate(rows):
            spans = {"right": [(-21, 12)], "left": [(-12, 21)], "center": [(-21, -3), (3, 21)]}[where]
            for si, (x0, x1) in enumerate(spans):
                n = int((x1 - x0) // 3.1)
                for g in range(n):
                    box(sc, f"Coop{ri}_{si}_{g}", (x0 + 1.55 + g * 3.1, 1.25, z), (3.0, 2.5, 5.0), m.garage)
            sodium_lamp(sc, lamp_i, 0, z + 5, 0)
            lamp_i += 1
            # тупиковый карман с хламом
            model(sc, f"Junk{ri}", "gigadom/junk_pile.glb", (rng.choice((-16, 16)), 0, z + 5), rng.uniform(0, 360))
            model(sc, f"Barrel{ri}", "gigadom/barrel_rusty.glb", (rng.uniform(-10, 10), 0, z + 6.5), 0)
            if ri % 2:
                car(sc, f"NCar{ri}", rng.uniform(-12, 12), z + 5, 90, rng.choice(colors))
        exit_door(sc, (0, 0, z_north + 1.0), 0)
    elif exit:
        exit_door(sc, (0, 0, -21.6), 0)
    return z_south


# ---------------- Гигадом: лабиринт ----------------

DIRS = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
OPP = {"N": "S", "S": "N", "E": "W", "W": "E"}
MODULES = {
    "straight": {"N", "S"}, "dead_end": {"S"}, "t_junction": {"N", "S", "W"}, "corner": {"S", "W"},
}
# поворот на +90° (против часовой при взгляде сверху): N→W, W→S, S→E, E→N
ROT90 = {"N": "W", "W": "S", "S": "E", "E": "N"}


def _rotate(dirs, steps):
    out = set(dirs)
    for _ in range(steps):
        out = {ROT90[d] for d in out}
    return out


def _pick_module(opens):
    for name, base in MODULES.items():
        for steps in range(4):
            if _rotate(base, steps) == opens:
                return name, steps * 90
    return None, 0


def gigadom_maze(sc, gm, prefix, origin, forward, length, seed, end="exit", lights=True):
    """Лабиринт из модулей 4×4 м. origin — центр первой ячейки, forward — общее направление ('S' или 'N').
    Путь не возвращается назад, есть тупиковые ответвления. end: 'exit' — КПП в конце, 'spawn' — точка старта."""
    rng = random.Random(seed)
    back = OPP[forward]
    perp = ["E", "W"] if forward in ("N", "S") else ["N", "S"]
    lat = 0 if forward in ("N", "S") else 1  # индекс поперечной координаты ячейки
    cells = {(0, 0): {back}}  # первая ячейка открыта в сторону зала
    path = [(0, 0)]
    cur = (0, 0)
    sideways = 0
    for _ in range(length - 1):
        options = [forward] * 2 + perp
        rng.shuffle(options)
        moved = False
        for d in options:
            dx, dz = DIRS[d]
            nxt = (cur[0] + dx, cur[1] + dz)
            step = (dx, dz)[lat]
            if nxt in cells or abs(nxt[lat]) > 5:
                continue
            if d in perp and abs(sideways + step) > 3:
                continue
            cells[cur].add(d)
            cells[nxt] = {OPP[d]}
            sideways += step if d in perp else 0
            cur = nxt
            path.append(cur)
            moved = True
            break
        if not moved:
            break
    # Тупиковые ответвления
    for _ in range(4):
        base = path[rng.randint(1, max(1, len(path) - 2))]
        if len(cells[base]) >= 3:
            continue
        for d in rng.sample(perp + [forward], 3):
            dx, dz = DIRS[d]
            nxt = (base[0] + dx, base[1] + dz)
            if nxt in cells or abs(nxt[lat]) > 5:
                continue
            cells[base].add(d)
            cells[nxt] = {OPP[d]}
            break
    ox, oz = origin
    k = 0
    keep_clear = {path[0], path[-1]}
    for (cx, cz), opens in cells.items():
        name, yaw = _pick_module(opens)
        if name is None:
            continue
        k += 1
        x, z = ox + cx * 4.0, oz + cz * 4.0
        if name == "straight" and rng.random() < 0.25:
            # прямой с дверью сбоку: проём закрыт стальной дверью
            model(sc, f"{prefix}Cell{k}", "gigadom/corridor_door_side.glb", (x, 0, z), yaw)
            side = _rotate({"E"}, yaw // 90).pop()
            dx, dz = DIRS[side]
            model(sc, f"{prefix}Door{k}", "gigadom/steel_door.glb", (x + dx * 2.05, 0, z + dz * 2.05), 90 if side in ("E", "W") else 0)
        else:
            model(sc, f"{prefix}Cell{k}", f"gigadom/corridor_{name}.glb", (x, 0, z), yaw)
        if lights and k % 2 == 0:
            model(sc, f"{prefix}Tube{k}", "gigadom/fluorescent_lamp.glb", (x, 3.0, z), yaw)
            lamp(sc, f"{prefix}Light{k}", (x, 2.7, z), color=(0.82, 0.9, 1.0), energy=0.9, rng=6.5)
        if (cx, cz) in keep_clear:
            continue
        if name == "straight" and rng.random() < 0.7:
            # хлам вдоль стены — проход остаётся
            item = rng.choice(["bunk_bed", "metal_cabinet", "barrel_rusty", "junk_pile", "barrel_rusty"])
            sx = rng.choice((-1.3, 1.3))
            px, pz = (x + sx, z) if "N" in opens else (x, z + sx)
            model(sc, f"{prefix}Prop{k}", f"gigadom/{item}.glb", (px, 0, pz), (0 if sx < 0 else 180) + (90 if "N" in opens else 0))
        elif name == "dead_end" and rng.random() < 0.6:
            model(sc, f"{prefix}Prop{k}", "gigadom/junk_pile.glb", (x, 0, z), rng.uniform(0, 360))
    ex, ez = path[-1]
    end_pos = (ox + ex * 4.0, oz + ez * 4.0)
    # куда смотрит «конец»: в сторону, откуда пришли
    prev = path[-2] if len(path) > 1 else (0, 0)
    face_dir = (prev[0] - ex, prev[1] - ez)
    # Лицо двери — локальная +Z, взгляд игрока — локальная −Z: повороты разные.
    door_yaw = {(0, 1): 0, (0, -1): 180, (1, 0): 90, (-1, 0): -90}.get(face_dir, 0)
    look_yaw = {(0, 1): 180, (0, -1): 0, (1, 0): -90, (-1, 0): 90}.get(face_dir, 0)
    if end == "exit":
        exit_door(sc, (end_pos[0] - face_dir[0] * 1.5, 0, end_pos[1] - face_dir[1] * 1.5), door_yaw)
    else:
        spawn(sc, "Player", (end_pos[0], 0, end_pos[1]), look_yaw)
    return end_pos
