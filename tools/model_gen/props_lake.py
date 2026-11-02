"""Акт 3 — Озеро боли (острова 51–70): тёмная вода, плот, острова-соблазны.
Острова — общая основа (холм) + набор декораций, их можно комбинировать."""
import math
from mg_lib import Prop

CATEGORY = "lake"


def _figure(p, x, y, z, m="black", h=1.75, pose="stand", rot=0):
    """Обобщённая человеческая фигура без лица (силуэты острова)."""
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))

    def T(lx, ly, lz):
        return (x + lx * c - ly * s, y + lx * s + ly * c, z + lz)
    k = h / 1.75
    if pose == "stand":
        for sx in (-1, 1):
            p.beam(T(sx * 0.1 * k, 0, 0), T(sx * 0.11 * k, 0, 0.85 * k), 0.13 * k, m)
            p.beam(T(sx * 0.24 * k, 0, 1.42 * k), T(sx * 0.28 * k, 0, 0.8 * k), 0.09 * k, m)
        p.box(( 0.42 * k, 0.24 * k, 0.62 * k), T(0, 0, 1.15 * k), m, rot=(0, 0, rot), bevel=0.04 * k)
    else:  # kneel
        for sx in (-1, 1):
            p.beam(T(sx * 0.1 * k, -0.05, 0.05), T(sx * 0.1 * k, 0.4 * k, 0.05), 0.13 * k, m)
            p.beam(T(sx * 0.1 * k, 0.4 * k, 0.08), T(sx * 0.1 * k, 0.05, 0.5 * k), 0.13 * k, m)
            p.beam(T(sx * 0.22 * k, -0.05, 0.95 * k), T(sx * 0.12 * k, -0.25 * k, 0.6 * k), 0.08 * k, m)
        p.box((0.4 * k, 0.24 * k, 0.55 * k), T(0, -0.02, 0.78 * k), m, rot=(-15, 0, rot), bevel=0.04 * k)
    top = 1.62 if pose == "stand" else 1.2
    p.cyl(0.05 * k, 0.1 * k, T(0, 0, (top - 0.17) * k), m, segs=6)
    p.sphere(0.12 * k, T(0, 0, top * k), m, segs=8, rings=6, scale=(0.9, 1, 1.15))


def raft():
    """Плот экспедиции: брёвна, связанные верёвкой, настил, шесты, ящик и фонарь на шесте."""
    p = Prop("raft")
    for i in range(8):
        x = -1.12 + i * 0.32
        p.cyl(0.16, 3.4, (x, -1.7, 0.0), "wood_old", segs=7, rot=(-90, 0, 0), jitter=0.01)
        p.cyl(0.13, 0.02, (x, -1.71, 0.0), "wood_light", segs=7, rot=(-90, 0, 0))
    for y in (-1.3, 0, 1.3):
        p.box((2.7, 0.14, 0.08), (0, y, 0.18), "wood_dark")
        for i in range(8):
            p.cyl(0.165, 0.04, (-1.12 + i * 0.32, y + 0.1, 0.0), "cloth_gray", segs=7, rot=(-90, 0, 0))
    for i in range(6):
        p.box((0.24, 1.1, 0.03), (-0.6 + i * 0.25, 0.4, 0.22), "wood", bevel=0.005)
    p.box_floor((0.6, 0.45, 0.4), (0.7, -0.9, 0.16), "paint_army", bevel=0.02)
    p.cyl(0.05, 2.0, (-1.0, 1.4, 0.16), "wood_dark", segs=6)
    p.beam((-1.0, 1.4, 2.1), (-0.7, 1.4, 2.0), 0.03, "wood_dark")
    p.cyl(0.07, 0.18, (-0.7, 1.4, 1.75), "metal_dark", segs=6)
    p.cyl(0.05, 0.1, (-0.7, 1.4, 1.79), "lamp_glow", segs=6)
    p.beam((1.2, 1.0, 0.25), (-0.3, -0.6, 0.3), 0.05, "wood_light", segs=6)  # весло-шест
    p.collider((2.7, 3.4, 0.35), (0, 0, 0.05))
    return p


def pier():
    """Пирс 2×8 м на сваях: доски с щелями, поперечины, швартовые тумбы, фонарь на конце."""
    p = Prop("pier")
    rng = p.rng
    for i in range(20):
        p.box((2.0 + rng.uniform(-0.05, 0.05), 0.34, 0.06), (rng.uniform(-0.03, 0.03), -3.8 + i * 0.4, 0.5),
              "wood_old", rot=(0, rng.uniform(-1, 1), rng.uniform(-1.5, 1.5)))
    for x in (-0.85, 0.85):
        p.box((0.12, 8.0, 0.15), (x, 0, 0.4), "wood_dark")
    for y in (-3.8, -1.3, 1.3, 3.8):
        for x in (-0.9, 0.9):
            p.cyl(0.1, 2.0, (x, y, -1.5), "wood_dark", segs=6, jitter=0.01)
        p.beam((-0.9, y, -0.9), (0.9, y, 0.3), 0.06, "wood_dark")
    for x in (-0.9, 0.9):
        p.cyl(0.08, 0.35, (x, 3.85, 0.53), "metal_dark", segs=8)
        p.cyl(0.1, 0.05, (x, 3.85, 0.85), "metal_dark", segs=8)
    p.cyl(0.05, 2.2, (0.9, -3.85, 0.53), "wood_dark", segs=6)
    p.box((0.2, 0.2, 0.3), (0.9, -3.85, 2.85), "metal_dark")
    p.box((0.16, 0.16, 0.22), (0.9, -3.85, 2.82), "sodium")
    p.cable((0.9, 3.85, 0.8), (1.5, 4.8, 0.0), 0.15, "cloth_gray", 0.03)
    p.collider((2.0, 8.0, 0.1), (0, 0, 0.5))
    return p


def island_base():
    """Основа острова: неровный холм ~16×10 м с камнями и травой, поверхность ~Z 1.2."""
    p = Prop("island_base")
    p.blob(8.0, (0, 0, -0.6), "sand_dark", scale=(1.0, 0.65, 0.23), jitter=0.04, subdiv=3)
    rng = p.rng
    for _ in range(9):
        a = rng.uniform(0, math.tau)
        r = rng.uniform(0.7, 0.95)
        p.blob(rng.uniform(0.3, 0.8), (7.6 * r * math.cos(a), 4.9 * r * math.sin(a), 0.1), "rock", jitter=0.3)
    for _ in range(14):  # кочки травы
        x, y = rng.uniform(-5, 5), rng.uniform(-3, 3)
        z = 1.25 * (1 - (x / 8) ** 2 - (y / 5.2) ** 2) - 0.03
        for k in range(4):
            a = k * 1.57 + rng.uniform(0, 0.5)
            p.beam((x, y, z), (x + 0.15 * math.cos(a), y + 0.15 * math.sin(a), z + rng.uniform(0.25, 0.45)), 0.04,
                   "grass")
    p.collider((12.0, 7.5, 1.6), (0, 0, -0.1))
    return p


def island_rock():
    """Валун с наростом и мелкими камнями вокруг."""
    p = Prop("island_rock")
    p.blob(0.8, (0, 0, 0.35), "rock", scale=(1.3, 1.0, 0.75), jitter=0.22, subdiv=2)
    p.blob(0.35, (0.7, 0.4, 0.15), "rock", jitter=0.3)
    p.blob(0.2, (-0.8, -0.5, 0.08), "rock", jitter=0.3)
    p.blob(0.3, (0.1, 0.2, 0.9), "grass", scale=(1.2, 1, 0.3), jitter=0.3)
    return p.collider((2.0, 1.6, 1.0), (0, 0, 0.45))


def palm_tree():
    """Остров плоти (51): пальма с кольчатым стволом, разлапистыми листьями и плодами."""
    p = Prop("palm_tree")
    pts = [(0, 0, 0), (0.12, 0, 1.0), (0.3, 0, 2.0), (0.36, 0, 3.0), (0.3, 0, 3.6)]
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        p.beam(a, b, 0.3 - i * 0.04, "bark", segs=7, thick2=0.26 - i * 0.04)
    for i in range(10):
        t = i / 10
        z = 0.2 + t * 3.3
        x = 0.36 * math.sin(t * 1.6)
        p.cyl(0.16 - t * 0.06, 0.06, (x, 0, z), "wood_dark", segs=7)
    top = pts[-1]
    for a in range(0, 360, 45):
        r = math.radians(a + 10)
        mid = (top[0] + 1.0 * math.cos(r), top[1] + 1.0 * math.sin(r), top[2] + 0.35)
        tip = (top[0] + 2.0 * math.cos(r), top[1] + 2.0 * math.sin(r), top[2] - 0.55)
        p.beam(top, mid, 0.05, "palm_leaf").beam(mid, tip, 0.04, "palm_leaf")
        for t in (0.3, 0.55, 0.8):  # перья листа
            base = [top[k] + (tip[k] - top[k]) * t for k in range(3)]
            base[2] += 0.35 * math.sin(math.pi * t)
            for sgn in (-1, 1):
                off = (base[0] - 0.35 * math.sin(r) * sgn, base[1] + 0.35 * math.cos(r) * sgn, base[2] - 0.25)
                p.beam(tuple(base), off, 0.12, "palm_leaf")
    for dx, dy in ((0.15, 0.1), (-0.1, 0.12), (0.05, -0.15), (0.18, -0.08)):
        p.sphere(0.13, (top[0] + dx, top[1] + dy, top[2] - 0.2), "skin", segs=7, rings=5, jitter=0.01)
    return p.collider((0.4, 0.4, 3.6), (0.18, 0, 1.8))


def outdoor_bed():
    """Остров сна (52): мягкая кованая кровать под открытым небом, подушки, смятое одеяло."""
    p = Prop("outdoor_bed")
    p.box_floor((2.0, 1.0, 0.1), (0, 0, 0.3), "metal_dark")
    p.box_floor((1.95, 0.95, 0.25), (0, 0, 0.4), "cloth_white", bevel=0.06)
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.cyl(0.03, 0.4 if sx > 0 else 1.1, (sx * 0.98, sy * 0.48, 0), "metal_dark", segs=6)
    for k in range(6):
        y = -0.4 + k * 0.16
        p.beam((-0.98, y, 0.4), (-0.98, y, 0.95 + 0.1 * math.sin(math.pi * k / 5)), 0.02, "metal_dark")
    p.curve_tube([(-0.98, -0.48, 1.1), (-0.98, -0.25, 1.05), (-0.98, 0, 1.12), (-0.98, 0.25, 1.05), (-0.98, 0.48, 1.1)],
                 0.035, "metal_dark")
    p.beam((0.98, -0.48, 0.4), (0.98, 0.48, 0.4), 0.03, "metal_dark")
    for y in (-0.22, 0.22):
        p.box((0.4, 0.42, 0.14), (-0.7, y, 0.72), "cloth_white", rot=(0, -12, 0), bevel=0.06)
    p.blob(0.55, (0.3, 0, 0.66), "cloth_blue", scale=(1.3, 0.95, 0.2), jitter=0.18, subdiv=2)
    p.box((0.6, 0.2, 0.005), (0.8, 0.58, 0.003), "cloth_blue", rot=(0, 0, 10))  # сползший край
    return p.collider((2.0, 1.0, 0.65), (0, 0, 0.32))


def statue_pedestal():
    """Остров славы (53): золотая статуя с поднятой рукой на ступенчатом постаменте с венками и табличкой."""
    p = Prop("statue_pedestal")
    p.box_floor((2.4, 2.4, 0.3), (0, 0, 0), "marble", bevel=0.03)
    p.box_floor((1.8, 1.8, 0.25), (0, 0, 0.3), "marble", bevel=0.03)
    p.box_floor((1.4, 1.4, 1.2), (0, 0, 0.55), "marble", bevel=0.02)
    p.box_floor((1.6, 1.6, 0.15), (0, 0, 1.75), "marble", bevel=0.02)
    p.box((0.8, 0.02, 0.35), (0, -0.71, 1.2), "gold")
    p.text("ТЕБЕ", (0, -0.725, 1.2), 0.2, "black", depth=0.006)
    b = 1.9
    for sx in (-1, 1):
        p.beam((sx * 0.13, 0, b), (sx * 0.16, -0.05 * (sx + 1), b + 1.0), 0.2, "gold", segs=6)
    p.box((0.62, 0.36, 0.9), (0, 0, b + 1.45), "gold", bevel=0.08)
    p.box((0.7, 0.4, 0.25), (0, 0, b + 1.0), "gold", bevel=0.06)
    p.cyl(0.08, 0.15, (0, 0, b + 1.9), "gold", segs=6)
    p.sphere(0.21, (0, 0, b + 2.17), "gold", segs=10, rings=7, scale=(0.9, 1.0, 1.15))
    p.beam((-0.36, 0, b + 1.8), (-0.48, -0.1, b + 1.15), 0.14, "gold", segs=6)
    p.beam((0.36, 0, b + 1.8), (0.62, -0.05, b + 2.45), 0.14, "gold", segs=6)
    p.beam((0.62, -0.05, b + 2.45), (0.75, -0.08, b + 3.0), 0.12, "gold", segs=6)
    p.sphere(0.08, (0.77, -0.08, b + 3.08), "gold", segs=6, rings=4)
    p.box((0.5, 0.12, 0.6), (0.05, 0.2, b + 1.4), "gold", rot=(10, 0, 0))  # плащ
    for sx in (-1, 1):  # венки
        p.arc_tube((sx * 0.9, -0.95, 0.55), 0.22, 0, 360, 0.07, "foliage", steps=10, plane="xz")
        p.box((0.06, 0.02, 0.3), (sx * 0.9, -0.96, 0.25), "crimson")
    return p.collider((2.4, 2.4, b), (0, 0, b / 2)).collider((0.8, 0.5, 2.4), (0, 0, b + 1.2))


def kneeling_figure():
    """Остров мести (54) / Покоя (59): коленопреклонённая фигура-силуэт без лица."""
    p = Prop("kneeling_figure")
    _figure(p, 0, 0, 0, "black", pose="kneel")
    return p.collider((0.55, 0.7, 1.35), (0, 0.1, 0.67))


def knife():
    """Нож с гардой, клёпками на рукояти и тусклым лезвием."""
    p = Prop("knife")
    p.poly_prism([(0, -0.012), (0.17, -0.012), (0.22, 0.012), (0, 0.016)], 0.004, (0.0, 0, 0.012), "metal", rot=(0, 0, 0))
    p.box((0.012, 0.045, 0.02), (-0.006, 0.002, 0.012), "metal_dark")
    p.box((0.11, 0.026, 0.022), (-0.067, 0.002, 0.012), "wood_dark", bevel=0.004)
    for x in (-0.04, -0.09):
        p.cyl(0.004, 0.024, (x, 0.002, 0.0), "metal", segs=6)
    return p


def gold_pile():
    """Остров богатства (55): гора монет, слитков, кубков и сундук."""
    p = Prop("gold_pile")
    p.blob(1.2, (0, 0, 0), "gold", scale=(1, 1, 0.55), jitter=0.05, subdiv=2)
    rng = p.rng
    for i in range(26):
        a = i * 2.4
        r = 0.3 + (i % 6) * 0.18
        z = 0.05 + 0.72 * (1 - (r / 1.25) ** 2)
        p.cyl(0.07, 0.02, (r * math.cos(a), r * math.sin(a), z), "gold", segs=8, rot=(rng.uniform(-35, 35), rng.uniform(-35, 35), 0))
    for _ in range(4):  # слитки
        a = rng.uniform(0, math.tau)
        p.poly_prism([(-0.12, 0), (0.12, 0), (0.09, 0.06), (-0.09, 0.06)], 0.09,
                     (0.9 * math.cos(a), 0.9 * math.sin(a), 0.25), "gold", rot=(90, 0, math.degrees(a)))
    p.tube(0.08, 0.07, 0.12, (0.2, -0.3, 0.72), "gold", segs=8)  # кубок
    p.cyl(0.02, 0.1, (0.2, -0.3, 0.62), "gold", segs=6)
    p.box_floor((0.7, 0.45, 0.4), (-1.55, 1.0, 0), "wood_dark", rot=(0, 0, 25), bevel=0.02)
    p.box((0.72, 0.47, 0.05), (-1.55, 1.0, 0.2), "gold", rot=(0, 0, 25))
    p.box((0.7, 0.08, 0.42), (-1.65, 1.22, 0.55), "wood_dark", rot=(-20, 0, 25))  # откинутая крышка
    for k in range(5):
        p.cyl(0.07, 0.02, (-1.6 + k * 0.06, 0.95 + k * 0.02, 0.4), "gold", segs=8)
    return p.collider((2.3, 2.3, 0.8), (0, 0, 0.4))


def childhood_house():
    """Остров дома (56): деревянный дом детства: сруб, резные наличники, крыльцо, труба с дымом, свет в окнах."""
    p = Prop("childhood_house")
    W, D, H = 6.0, 4.5, 2.8
    p.box_floor((W + 0.2, D + 0.2, 0.4), (0, 0, 0), "brick")
    for i in range(9):  # венцы сруба брёвнами
        z = 0.4 + i * 0.27 + 0.135
        for sy in (-1, 1):
            p.cyl(0.14, W + 0.5, (-W / 2 - 0.25, sy * D / 2, z), "wood", segs=6, rot=(0, 90, 0))
        for sx in (-1, 1):
            p.cyl(0.14, D + 0.5, (sx * W / 2, -D / 2 - 0.25, z + 0.07), "wood", segs=6, rot=(-90, 0, 0))
    p.box_floor((W - 0.1, D - 0.1, H), (0, 0, 0.4), "wood_dark")
    rz = H + 0.4
    p.poly_prism([(-W / 2 - 0.5, 0), (W / 2 + 0.5, 0), (0, 2.2)], D + 0.8, (0, 0, rz), "wood_dark")
    for sx in (-1, 1):  # скаты крыши
        ang = math.degrees(math.atan2(2.2, W / 2 + 0.5))
        p.box((math.hypot(W / 2 + 0.5, 2.2) + 0.1, D + 1.0, 0.08), (sx * (W / 4 + 0.25), 0, rz + 1.1 + 0.04),
              "brick_roof", rot=(0, sx * -ang, 0))
    for sy in (-1, 1):  # фронтон с окошком
        p.poly_prism([(-W / 2 + 0.2, 0), (W / 2 - 0.2, 0), (0, 2.0)], 0.05, (0, sy * (D / 2 + 0.38), rz), "wood_light")
        p.box((0.5, 0.06, 0.5), (0, sy * (D / 2 + 0.41), rz + 0.8), "window_lit")
    p.box_floor((0.5, 0.5, 1.7), (1.6, 0.6, rz + 0.6), "brick")
    p.box_floor((0.6, 0.6, 0.1), (1.6, 0.6, rz + 2.3), "concrete_dark")
    for k in range(4):  # дым
        p.blob(0.25 + k * 0.1, (1.6 + k * 0.25, 0.6 + k * 0.1, rz + 2.7 + k * 0.5), "cloth_gray", jitter=0.3)
    for x in (-1.8, 1.8):
        p.box((1.0, 0.08, 0.9), (x, -D / 2 - 0.15, 1.8), "window_lit")
        p.box((0.06, 0.1, 0.9), (x, -D / 2 - 0.18, 1.8), "wood_light")
        p.box((1.0, 0.1, 0.06), (x, -D / 2 - 0.18, 2.0), "wood_light")
        p.poly_prism([(-0.7, 0), (0.7, 0), (0.5, 0.15), (0, 0.32), (-0.5, 0.15)], 0.06, (x, -D / 2 - 0.2, 2.25),
                     "cloth_white")  # резной наличник
        p.box((1.3, 0.08, 0.1), (x, -D / 2 - 0.2, 1.3), "cloth_white")
        for sx in (-1, 1):
            p.box((0.3, 0.05, 1.0), (x + sx * 0.68, -D / 2 - 0.2, 1.8), "paint_blue")  # ставни
    p.box((0.95, 0.08, 1.9), (0, -D / 2 - 0.15, 1.35), "window_lit")
    p.box((0.9, 0.06, 1.85), (0.38, -D / 2 - 0.55, 1.35), "wood", rot=(0, 0, -70))  # открытая дверь
    p.box_floor((2.0, 1.1, 0.4), (0, -D / 2 - 0.7, 0), "wood_old")
    for k in range(2):
        p.box_floor((1.2, 0.3, 0.13 * (k + 1)), (0, -D / 2 - 1.4 + k * 0.0 - (1 - k) * 0.3, 0), "wood_old")
    for x in (-0.9, 0.9):
        p.cyl(0.06, 2.0, (x, -D / 2 - 1.15, 0.4), "wood_light", segs=6)
    p.box((2.2, 1.4, 0.08), (0, -D / 2 - 0.65, 2.45), "brick_roof", rot=(-15, 0, 0))
    p.collider((W + 0.2, D + 0.2, H + 0.4), (0, 0, (H + 0.4) / 2))
    return p


def fence_wooden():
    """Деревянный штакетник, модуль 3 м: заострённые доски, две прожилины, столбы."""
    p = Prop("fence_wooden")
    rng = p.rng
    for x in (-1.5, 1.5):
        p.box_floor((0.12, 0.12, 1.15), (x, 0.05, 0), "wood_dark")
    for z in (0.3, 0.85):
        p.box((3.0, 0.05, 0.08), (0, 0.04, z), "wood_dark")
    for i in range(14):
        x = -1.4 + i * 0.215
        h = 1.0 + rng.uniform(-0.05, 0.05)
        p.poly_prism([(-0.05, 0), (0.05, 0), (0.05, h), (0, h + 0.08), (-0.05, h)], 0.02, (x, 0, 0.02), "wood_old",
                     rot=(90, rng.uniform(-3, 3), 0))
    return p.collider((3.0, 0.15, 1.1), (0, 0, 0.55))


def throne():
    """Остров власти (57): трон с высокой спинкой, навершиями, бархатом на трёхступенчатом подиуме с ковром."""
    p = Prop("throne")
    for i in range(3):
        s = 3.0 - i * 0.6
        p.box_floor((s, s, 0.25), (0, 0, i * 0.25), "marble", bevel=0.02)
        p.box_floor((0.8, s + 0.02, 0.252), (0, -0.01, i * 0.25), "velvet")
    p.box_floor((0.8, 1.5, 0.01), (0, -2.2, 0), "velvet")
    b = 0.75
    p.box_floor((1.1, 0.85, 0.45), (0, 0, b), "gold", bevel=0.03)
    p.box_floor((0.9, 0.7, 0.12), (0, -0.05, b + 0.45), "velvet", bevel=0.04)
    p.box_floor((1.1, 0.18, 2.3), (0, 0.38, b), "gold", bevel=0.03)
    p.box((0.75, 0.05, 1.4), (0, 0.28, b + 1.35), "velvet", bevel=0.02)
    p.poly_prism([(-0.55, 0), (0.55, 0), (0.4, 0.3), (0, 0.6), (-0.4, 0.3)], 0.18, (0, 0.38, b + 2.3), "gold")
    for x in (-0.48, 0.48):
        p.box_floor((0.14, 0.75, 0.12), (x, 0, b + 0.75), "gold", bevel=0.03)
        p.cyl(0.05, 0.3, (x, -0.3, b + 0.45), "gold", segs=6)
        p.sphere(0.08, (x, -0.33, b + 0.9), "gold", segs=8, rings=5)
        p.sphere(0.1, (x * 1.05, 0.38, b + 2.4), "gold", segs=8, rings=5)
    for x in (-0.25, 0, 0.25):
        p.sphere(0.06, (x, 0.28, b + 2.65 + (0.2 if x == 0 else 0)), "crimson", segs=6, rings=4)
    for sx in (-1, 1):  # жаровни у подиума
        p.cyl(0.06, 1.1, (sx * 1.8, -1.2, 0), "metal_dark", segs=6)
        p.tube(0.25, 0.22, 0.2, (sx * 1.8, -1.2, 1.1), "gold", segs=10)
        p.blob(0.18, (sx * 1.8, -1.2, 1.35), "sodium", scale=(1, 1, 1.4), jitter=0.35)
    return p.collider((3.0, 3.0, 0.75), (0, 0, 0.375)).collider((1.1, 0.95, 2.3), (0, 0.05, b + 1.15))


def dead_tree():
    """Остров прощения (58): сухое корявое дерево с корнями и висящей верёвкой."""
    p = Prop("dead_tree")
    p.curve_tube([(0, 0, 0), (0.08, 0, 1.2), (-0.05, 0.05, 2.4), (0.15, 0, 3.4), (0.3, -0.1, 4.2)], 0.3, "bark", segs=7)
    rng = p.rng
    for a in range(0, 360, 72):  # корни
        r = math.radians(a + 15)
        p.beam((0, 0, 0.3), (0.9 * math.cos(r), 0.9 * math.sin(r), -0.05), 0.14, "bark", segs=5, thick2=0.04)
    branches = [((0, 0, 2.2), (-1.4, 0.1, 3.0)), ((0, 0, 2.6), (1.2, 0.3, 3.4)), ((0.05, 0, 1.6), (-0.9, -0.2, 2.0)),
                ((0.15, 0, 3.4), (1.0, -0.3, 4.3)), ((0.1, 0, 3.0), (-0.7, 0.5, 3.9))]
    for base, tip in branches:
        p.beam(base, tip, 0.12, "bark", segs=5, thick2=0.04)
        for t in (0.5, 0.8):
            m = [base[k] + (tip[k] - base[k]) * t for k in range(3)]
            p.beam(tuple(m), (m[0] + rng.uniform(-0.4, 0.4), m[1] + rng.uniform(-0.4, 0.4), m[2] + rng.uniform(0.2, 0.5)),
                   0.04, "bark", segs=4, thick2=0.015)
    p.curve_tube([(-1.0, 0.07, 2.8), (-1.0, 0.07, 2.0)], 0.025, "cloth_gray", segs=4)
    p.arc_tube((-1.0, 0.07, 1.85), 0.15, 0, 360, 0.025, "cloth_gray", steps=8, plane="xz")
    return p.collider((0.4, 0.4, 4.0), (0.05, 0, 2.0))


def birch_tree():
    """Остров скорби (60): тонкая берёза с ветвями-плетями и редкой кроной."""
    p = Prop("birch_tree")
    p.curve_tube([(0, 0, 0), (0.05, 0, 2.0), (0.0, 0.05, 4.0), (0.1, 0.0, 5.0)], 0.16, "birch", segs=6)
    rng = p.rng
    for k in range(7):
        z = 2.4 + k * 0.38
        a = k * 2.3
        tip = (0.9 * math.cos(a), 0.9 * math.sin(a), z - 0.2)
        p.beam((0.03, 0.02, z), tip, 0.04, "bark", segs=4, thick2=0.015)
        for j in range(3):  # плакучие плети
            p.beam(tip, (tip[0] + rng.uniform(-0.1, 0.1), tip[1] + rng.uniform(-0.1, 0.1), tip[2] - 0.8 - j * 0.2), 0.012,
                   "bark")
        for j in range(3):
            p.blob(0.2, (tip[0] * (0.55 + j * 0.25), tip[1] * (0.55 + j * 0.25), tip[2] - 0.1 - j * 0.3), "foliage", scale=(1, 1, 1.4), jitter=0.4)
    return p.collider((0.25, 0.25, 4.8), (0.05, 0, 2.4))


def greek_temple():
    """Остров тела (61): светлый портик с каннелюрами колонн, капителями, ступенями и чашей."""
    p = Prop("greek_temple")
    W, D = 5.0, 3.5
    for k in range(3):
        p.box_floor((W + 0.8 - k * 0.4, D + 0.8 - k * 0.4, 0.12), (0, 0, k * 0.12), "marble", bevel=0.01)
    for x in (-2.1, -0.75, 0.75, 2.1):
        for y in (-1.4, 1.4):
            p.cyl(0.24, 0.12, (x, y, 0.36), "marble", segs=10)
            p.cyl(0.2, 2.76, (x, y, 0.48), "marble", segs=12, r2=0.18)
            p.box((0.5, 0.5, 0.12), (x, y, 3.3), "marble", bevel=0.02)
            p.cyl(0.26, 0.08, (x, y, 3.16), "marble", segs=10, r2=0.2)
            p.collider((0.45, 0.45, 2.9), (x, y, 1.9))
    p.box_floor((W + 0.4, D + 0.4, 0.4), (0, 0, 3.36), "marble", bevel=0.02)
    p.box((W + 0.4, 0.05, 0.12), (0, -D / 2 - 0.22, 3.55), "gold")
    p.poly_prism([(-W / 2 - 0.4, 0), (W / 2 + 0.4, 0), (0, 1.1)], D + 0.4, (0, 0, 3.76), "marble")
    p.poly_prism([(-W / 2 + 0.2, 0.1), (W / 2 - 0.2, 0.1), (0, 0.9)], 0.05, (0, -D / 2 - 0.23, 3.76), "plaster")
    p.tube(0.5, 0.45, 0.25, (0, 0, 0.9), "marble", segs=14)
    p.cyl(0.12, 0.54, (0, 0, 0.36), "marble", segs=10, r2=0.08)
    p.cyl(0.45, 0.01, (0, 0, 1.1), "water_dark", segs=14)
    p.collider((W + 0.8, D + 0.8, 0.36), (0, 0, 0.18))
    return p


def library_tower():
    """Остров знания (62): сужающаяся башня-библиотека с полками книг, карнизами, лестницей и раскрытой книгой."""
    p = Prop("library_tower")
    H, levels = 9.0, 10
    rng = p.rng
    for i in range(levels):
        r = 1.6 - i * 0.05
        z = i * H / levels
        lh = H / levels
        p.cyl(r, lh - 0.05, (0, 0, z), "wood_dark", segs=10)
        p.cyl(r + 0.06, 0.06, (0, 0, z + lh - 0.08), "wood", segs=10)
        for k in range(10):
            a = math.radians(k * 36 + 18)
            for j in range(4):  # отдельные корешки книг
                aa = a + math.radians(-12 + j * 8)
                hh = lh * rng.uniform(0.55, 0.75)
                m = ("book_a", "book_b", "book_c", "paper_old")[rng.randrange(4)]
                p.box((0.12, 0.1, hh), ((r + 0.01) * math.cos(aa), (r + 0.01) * math.sin(aa), z + 0.05 + hh / 2), m,
                      rot=(0, 0, math.degrees(aa)))
    p.cyl(1.2, 1.2, (0, 0, H), "brick_roof", segs=10, r2=0.05)
    for i in range(14):  # винтовая лестница снаружи
        a = i * 0.45
        z = i * 0.25
        p.box((0.7, 0.3, 0.06), (1.95 * math.cos(a), 1.95 * math.sin(a), z), "wood_old", rot=(0, 0, math.degrees(a)))
    p.box((1.0, 0.7, 0.04), (0, -2.6, 0.55), "paper", rot=(0, 0, 0))
    p.box((1.05, 0.72, 0.03), (0, -2.6, 0.52), "book_a")
    p.box_floor((0.6, 0.5, 0.5), (0, -2.6, 0), "wood_dark")
    p.collider((3.3, 3.3, H), (0, 0, H / 2))
    return p


def elder_scholar():
    """Старец-учёный: фигура в балахоне с капюшоном, бородой, посохом и книгой."""
    p = Prop("elder_scholar")
    p.cyl(0.4, 1.45, (0, 0, 0), "black", segs=10, r2=0.2, jitter=0.02)
    p.cyl(0.22, 0.2, (0, 0, 1.45), "black", segs=8, r2=0.16)
    p.sphere(0.2, (0, 0, 1.68), "black", segs=8, rings=6, scale=(1, 1.1, 1.2))
    p.sphere(0.12, (0, -0.1, 1.64), "skin", segs=6, rings=4, scale=(1, 0.7, 1))
    p.cyl(0.09, 0.35, (0, -0.15, 1.25), "cloth_white", segs=6, r2=0.02)
    p.beam((0.25, -0.15, 1.2), (0.42, -0.1, 0.95), 0.08, "black")
    p.beam((0.42, -0.1, 0), (0.42, -0.1, 2.0), 0.045, "wood_dark", segs=6)
    p.curve_tube([(0.42, -0.1, 2.0), (0.5, -0.1, 2.12), (0.42, -0.1, 2.2)], 0.04, "wood_dark", segs=5)
    p.box((0.22, 0.05, 0.28), (-0.25, -0.22, 1.0), "book_a", rot=(0, 0, 20))
    return p.collider((0.8, 0.8, 1.9), (0.05, 0, 0.95))


def lonely_chair():
    """Остров одиночества (63): единственный стул на голом камне; на спинке — пиджак."""
    p = Prop("lonely_chair")
    p.blob(1.6, (0, 0, -0.32), "rock", scale=(1, 1, 0.25), jitter=0.12, subdiv=2)
    from props_districts import _chair_geom
    _chair_geom(p, 0, 0, 0, "wood_dark", "wood_dark")
    p.box((0.46, 0.05, 0.4), (0, 0.22, 0.72), "cloth_gray", rot=(-5, 0, 0), bevel=0.02)
    for sx in (-1, 1):
        p.box((0.12, 0.05, 0.35), (sx * 0.27, 0.22, 0.6), "cloth_gray", rot=(0, sx * 10, 0))
    return p.collider((0.44, 0.42, 1.05), (0, 0, 0.52))


def garland():
    """Остров вседозволенности (64): гирлянда с цветными лампочками и флажками, пролёт 8 м."""
    p = Prop("garland")
    for x in (-4, 4):
        p.cyl(0.07, 3.3, (x, 0, 0), "wood_dark", segs=6)
        p.beam((x, 0, 3.1), (x * 0.95, 0, 3.3), 0.03, "metal_dark")
    pts = p.sag((-4, 0, 3.1), (4, 0, 3.1), 0.7, 16)
    p.curve_tube(pts, 0.015, "black")
    mats = ("bulb_yellow", "bulb_pink", "bulb_green", "led_red")
    for i, (x, y, z) in enumerate(pts[1:-1]):
        p.cyl(0.02, 0.04, (x, y, z - 0.05), "black", segs=5)
        p.sphere(0.06, (x, y, z - 0.1), mats[i % 4], segs=6, rings=4, scale=(1, 1, 1.3))
    pts2 = p.sag((-4, 0.05, 2.9), (4, 0.05, 2.9), 0.9, 16)
    p.curve_tube(pts2, 0.01, "cloth_white")
    flags = ("crimson", "paint_yellow", "slide_blue", "pink_flower")
    for i, (x, y, z) in enumerate(pts2[1:-1]):
        p.poly_prism([(-0.12, 0), (0.12, 0), (0, -0.3)], 0.005, (x, y, z), flags[i % 4])
    return p.collider((0.15, 0.15, 3.3), (-4, 0, 1.65)).collider((0.15, 0.15, 3.3), (4, 0, 1.65))


def radiant_figure():
    """Остров веры (65): сияющая фигура в одеянии с раскрытыми руками, нимбом и лучами."""
    p = Prop("radiant_figure")
    p.cyl(0.6, 2.2, (0, 0, 0.3), "halo", segs=12, r2=0.28)
    p.cyl(0.7, 0.3, (0, 0, 0), "marble", segs=12, r2=0.6)
    p.sphere(0.28, (0, 0, 2.75), "halo", segs=10, rings=7, scale=(1, 1, 1.2))
    for sx in (-1, 1):
        p.beam((sx * 0.25, 0, 2.3), (sx * 0.8, -0.15, 2.0), 0.14, "halo", segs=6)
        p.box((0.25, 0.05, 0.6), (sx * 0.55, -0.1, 1.8), "halo", rot=(0, sx * -20, 0))
    p.arc_tube((0, 0.12, 2.75), 0.55, 0, 360, 0.05, "halo", steps=18, segs=4)
    for a in range(0, 360, 20):
        r = math.radians(a)
        L = 2.2 if a % 40 == 0 else 1.5
        p.beam((0.7 * math.cos(r), 0.14, 2.75 + 0.7 * math.sin(r)),
               ((0.7 + L) * math.cos(r), 0.14, 2.75 + (0.7 + L) * math.sin(r)), 0.025, "lamp_glow")
    return p.collider((1.4, 1.4, 3.1), (0, 0, 1.55))


def kneeling_worshipper():
    """Поклоняющийся (65) — коленопреклонённый силуэт, ставить рядами."""
    p = Prop("kneeling_worshipper")
    _figure(p, 0, 0, 0, "black", pose="kneel", h=1.65)
    return p.collider((0.55, 0.7, 1.3), (0, 0.1, 0.65))


def playground_tower():
    """Остров юности (66): деревянная горка-башенка с лестницей, перилами, красной крышей и окошками."""
    p = Prop("playground_tower")
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.box_floor((0.12, 0.12, 3.0), (sx * 0.55, sy * 0.55, 0), "wood_dark")
    p.box_floor((1.3, 1.3, 0.08), (0, 0, 1.5), "wood")
    for sy in (-1, 1):
        p.box_floor((1.2, 0.04, 1.2), (0, sy * 0.6, 1.58), "wood_light")
    p.box_floor((0.04, 1.2, 1.2), (-0.6, 0, 1.58), "wood_light")
    for z in (2.0, 2.5):
        p.cyl(0.18, 0.06, (0, -0.63, z), "lamp_glow", segs=8, rot=(90, 0, 0))
    p.poly_prism([(-0.85, 0), (0.85, 0), (0, 1.0)], 1.5, (0, 0, 3.0), "brick_roof")
    p.beam((0.65, -0.3, 1.55), (2.8, -0.3, 0.12), 0.55, "slide_blue")
    for sy in (-0.57, -0.03):
        p.beam((0.65, sy, 1.75), (2.8, sy, 0.32), 0.05, "slide_blue", segs=6)
    for k in range(6):  # лестница
        p.box((0.06, 0.6, 0.05), (-0.65 - k * 0.12, 0, 0.25 * (k + 1)), "wood")
    for sy in (-0.3, 0.3):
        p.beam((-1.4, sy, 0), (-0.62, sy, 1.55), 0.06, "wood_dark")
    p.box_floor((1.6, 1.0, 0.03), (2.3, -0.3, 0), "sand_dark")
    return p.collider((1.3, 1.3, 4.0), (0, 0, 2.0))


def ball():
    """Мяч с полосой."""
    p = Prop("ball")
    p.sphere(0.15, (0, 0, 0.15), "rubber_red", segs=10, rings=7)
    p.cyl(0.152, 0.04, (0, 0, 0.13), "enamel", segs=10)
    return p


def flower_arch():
    """Остров любви (67): арка, оплетённая лозой и цветами, со скамейкой для двоих."""
    p = Prop("flower_arch")
    for x in (-1.2, 1.2):
        for y in (-0.15, 0.15):
            p.box_floor((0.08, 0.08, 2.2), (x, y, 0), "whitewash")
        for z in (0.5, 1.0, 1.5, 2.0):
            p.box((0.08, 0.38, 0.04), (x, 0, z), "whitewash")
    for y in (-0.15, 0.15):
        p.arc_tube((0, y, 2.2), 1.2, 0, 180, 0.08, "whitewash", steps=12)
    rng = p.rng
    for i in range(22):
        a = math.radians(i * 180 / 21)
        x, z = 1.22 * math.cos(a), 2.2 + 1.22 * math.sin(a)
        p.blob(0.14, (x, rng.uniform(-0.2, 0.2), z), "foliage", jitter=0.35)
        if i % 2 == 0:
            p.sphere(0.07, (x + rng.uniform(-0.05, 0.05), -0.22, z + rng.uniform(-0.05, 0.05)), "pink_flower", segs=6, rings=4)
    for x in (-1.25, 1.25):
        for z in (0.3, 0.75, 1.2, 1.65, 2.05):
            p.blob(0.12, (x, rng.uniform(-0.2, 0.2), z), "foliage", jitter=0.35)
            p.sphere(0.06, (x, -0.22, z + 0.05), "pink_flower", segs=6, rings=4)
    p.box((1.2, 0.4, 0.05), (0, 0.9, 0.45), "wood_light", bevel=0.01)
    for x in (-0.5, 0.5):
        p.box_floor((0.06, 0.35, 0.43), (x, 0.9, 0), "whitewash")
    p.collider((0.2, 0.4, 2.2), (-1.2, 0, 1.1)).collider((0.2, 0.4, 2.2), (1.2, 0, 1.1))
    return p


def rage_dummy():
    """Остров гнева (68): манекен «неотличимый от живого» с трещинами и сколами на стойке; кувалда и обломки."""
    p = Prop("rage_dummy")
    p.cyl(0.25, 0.08, (0, 0, 0), "metal_dark", segs=8)
    p.cyl(0.04, 1.0, (0, 0, 0.08), "metal", segs=6)
    _figure(p, 0, 0, 0.05, "skin", h=2.0)
    for a, b in (((-0.05, -0.13, 1.7), (0.08, -0.13, 1.45)), ((0.08, -0.13, 1.45), (-0.02, -0.13, 1.25)),
                 ((-0.15, -0.13, 1.1), (0.0, -0.13, 0.95)), ((0.05, -0.12, 1.95), (0.1, -0.12, 1.8))):
        p.beam(a, b, 0.02, "black")
    p.blob(0.08, (0.4, -0.3, 0.04), "skin", jitter=0.4)
    p.blob(0.06, (-0.3, -0.5, 0.03), "skin", jitter=0.4)
    p.beam((-1.0, -0.4, 0.0), (-0.75, -0.4, 0.95), 0.05, "wood", segs=6)
    p.box((0.34, 0.15, 0.15), (-0.74, -0.4, 1.0), "metal_dark", rot=(0, -15, 0), bevel=0.02)
    return p.collider((0.7, 0.45, 2.3), (0, 0, 1.15))


def envy_window():
    """Остров зависти (69): резная рама-«окно» в лучшую жизнь: за стеклом — дом, сад, солнце и семья."""
    p = Prop("envy_window")
    W, H = 3.6, 3.4
    p.box_floor((W, 0.18, 0.18), (0, 0, 0), "gold")
    p.box_floor((W, 0.18, 0.18), (0, 0, H - 0.18), "gold")
    for x in (-W / 2 + 0.09, W / 2 - 0.09):
        p.box_floor((0.18, 0.18, H), (x, 0, 0), "gold")
    p.poly_prism([(-W / 2, 0), (W / 2, 0), (W / 2 - 0.4, 0.4), (0, 0.6), (-W / 2 + 0.4, 0.4)], 0.18, (0, 0, H), "gold")
    iw, ih = W - 0.36, H - 0.36
    p.box((iw, 0.04, ih * 0.55), (0, 0.06, 0.18 + ih * 0.725), "slide_blue")
    p.box((iw, 0.04, ih * 0.45), (0, 0.06, 0.18 + ih * 0.225), "grass")
    p.cyl(0.25, 0.03, (1.0, 0.03, 2.6), "bulb_yellow", segs=10, rot=(90, 0, 0))
    p.box((1.0, 0.04, 0.8), (-0.5, 0.02, 1.9), "whitewash")
    p.poly_prism([(-0.6, 0), (0.6, 0), (0, 0.55)], 0.04, (-0.5, 0.01, 2.3), "brick_roof")
    for x in (-0.75, -0.25):
        p.box((0.22, 0.03, 0.22), (x, 0.0, 2.0), "window_lit")
    p.box((0.2, 0.03, 0.35), (-0.5, 0.0, 1.68), "wood")
    for k, x in enumerate((0.4, 0.65, 0.85)):  # силуэты семьи
        h = (0.6, 0.55, 0.35)[k]
        p.box((0.12, 0.03, h), (x, 0.0, 1.5 + h / 2), "black")
        p.cyl(0.06, 0.03, (x, 0.0, 1.5 + h + 0.06), "black", segs=6, rot=(90, 0, 0))
    for x in (-1.3, 1.4):
        p.box((0.06, 0.03, 0.4), (x, 0.0, 1.7), "bark")
        p.cyl(0.22, 0.03, (x, 0.0, 2.05), "foliage", segs=8, rot=(90, 0, 0))
    return p.collider((W, 0.2, H), (0, 0, H / 2))


def checkpoint_gate():
    """Остров возвращения (70): КПП · ВЫХОД — рабица, колючая проволока, шлагбаум, будка, прожекторы."""
    p = Prop("checkpoint_gate")
    for sx in (-1, 1):
        x0, x1 = sx * 1.8, sx * 6.8
        for x in (x0, x1, (x0 + x1) / 2):
            p.box_floor((0.1, 0.1, 2.8), (x, 0, 0), "metal_dark")
            p.beam((x, 0, 2.8), (x, -0.35, 3.1), 0.05, "metal_dark")
        cx = (x0 + x1) / 2
        p.box((5.0, 0.02, 2.5), (cx, 0, 1.3), "chain_link")
        for z in (0.05, 2.55):
            p.beam((min(x0, x1), 0, z), (max(x0, x1), 0, z), 0.04, "metal", segs=5)
        for k in range(0, 16, 2):  # спираль «егоза»
            xx = x0 + (x1 - x0) * k / 16
            p.arc_tube((xx, -0.2, 3.0), 0.18, 0, 360, 0.015, "metal", steps=8, plane="xz")

        p.beam((x0, -0.2, 3.0), (x1, -0.2, 3.0), 0.012, "metal")
        p.collider((5.0, 0.2, 2.8), (cx, 0, 1.4))
        p.box_floor((0.15, 0.15, 6.0), (sx * 4.6, 0.6, 0), "metal_dark")
        p.box((0.7, 0.35, 0.35), (sx * 4.6, 0.45, 6.1), "metal_dark", rot=(-20, 0, 0), bevel=0.02)
        p.box((0.6, 0.02, 0.28), (sx * 4.6, 0.27, 6.04), "floodlight", rot=(-20, 0, 0))
        p.cable((sx * 4.6, 0.6, 5.8), (sx * 1.8, 0.0, 2.8), 0.5)
    for x in (-1.6, 1.6):
        p.box_floor((0.2, 0.2, 3.2), (x, 0, 0), "paint_yellow")
    p.box((3.4, 0.1, 0.6), (0, -0.05, 3.5), "enamel", bevel=0.01)
    p.text("КПП · ВЫХОД", (0, -0.11, 3.5), 0.32, "black", depth=0.01)
    # шлагбаум (поднят) и будка
    p.box_floor((0.3, 0.3, 1.0), (-1.3, -1.0, 0), "concrete")
    for k in range(6):
        p.beam((-1.3 + k * 0.35 * math.cos(1.2), -1.0, 1.0 + k * 0.35 * math.sin(1.2)),
               (-1.3 + (k + 1) * 0.35 * math.cos(1.2), -1.0, 1.0 + (k + 1) * 0.35 * math.sin(1.2)), 0.08,
               "calendar_red" if k % 2 else "enamel")
    p.box_floor((1.6, 1.6, 2.4), (3.8, -2.2, 0), "paint_green", bevel=0.02)
    p.box_floor((1.8, 1.8, 0.12), (3.8, -2.2, 2.4), "metal_dark")
    p.box((1.2, 0.04, 0.6), (3.8, -3.0, 1.5), "window_lit")
    p.box((0.7, 0.04, 1.9), (3.2 + 0.0, -1.39, 0.95), "wood")
    p.collider((1.6, 1.6, 2.5), (3.8, -2.2, 1.25))
    return p


PROPS = [
    raft, pier, island_base, island_rock, palm_tree, outdoor_bed, statue_pedestal, kneeling_figure,
    knife, gold_pile, childhood_house, fence_wooden, throne, dead_tree, birch_tree, greek_temple,
    library_tower, elder_scholar, lonely_chair, garland, radiant_figure, kneeling_worshipper,
    playground_tower, ball, flower_arch, rage_dummy, envy_window, checkpoint_gate,
]
