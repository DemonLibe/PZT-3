"""Акт 2 — Гигадом (секции 30–50): бесконечное бетонное строение, у угрозы есть тело.
Модульная сетка коридора: 4 м по длине (Y), ширина 4 м, высота 3 м. Модули стыкуются без зазоров."""
import math
from mg_lib import Prop

CATEGORY = "gigadom"
CW, CH, CL = 4.0, 3.0, 4.0
T = 0.25
BAND = 1.4  # высота крашеной панели снизу стены


def _wall(p, x, y0, y1, side, painted=True):
    """Стена коридора: бетон + крашеная панель снизу + плинтус. side: -1 левая, +1 правая."""
    L = y1 - y0
    yc = (y0 + y1) / 2
    p.box_floor((T, L, CH), (x, yc, 0), "concrete")
    inner = x - side * T / 2
    if painted:
        p.box_floor((0.01, L, BAND), (inner - side * 0.005, yc, 0), "paint_green")
        p.box_floor((0.02, L, 0.04), (inner - side * 0.01, yc, BAND), "metal_dark")
    p.box_floor((0.03, L, 0.1), (inner - side * 0.015, yc, 0), "concrete_dark")
    p.collider((T, L, CH), (x, yc, CH / 2))


def _shell(p, left=True, right=True, end=False, lamp=True, pipes=True, seed=0):
    p.box_floor((CW + 2 * T, CL, T), (0, 0, -T), "concrete_dark")
    p.box_floor((CW, CL, 0.005), (0, 0, 0), "tile_floor")
    p.box_floor((CW + 2 * T, CL, T), (0, 0, CH), "concrete")
    p.collider((CW + 2 * T, CL, T), (0, 0, -T / 2))
    p.collider((CW + 2 * T, CL, T), (0, 0, CH + T / 2))
    if left:
        _wall(p, -CW / 2 - T / 2, -CL / 2, CL / 2, -1)
    if right:
        _wall(p, CW / 2 + T / 2, -CL / 2, CL / 2, 1)
    if end:
        p.box_floor((CW, T, CH), (0, CL / 2 - T / 2, 0), "concrete")
        p.box_floor((CW, 0.01, BAND), (0, CL / 2 - T - 0.005, 0), "paint_green")
        p.collider((CW, T, CH), (0, CL / 2 - T / 2, CH / 2))
    # потолочные балки на стыках модулей
    p.box((CW, 0.3, 0.25), (0, -CL / 2 + 0.15, CH - 0.125), "concrete")
    if pipes:  # трубы и кабельный лоток вдоль потолка (по Y, бесшовно)
        side = -1 if left else 1
        xw = side * (CW / 2 - 0.15)
        p.pipe_run((xw, -CL / 2, CH - 0.45), (xw, CL / 2, CH - 0.45), 0.08, "rust")
        p.pipe_run((xw + -side * 0.22, -CL / 2, CH - 0.4), (xw + -side * 0.22, CL / 2, CH - 0.4), 0.05, "metal")
        p.box((0.3, CL, 0.03), (-side * 0.9, 0, CH - 0.32), "metal_dark")
        for y in (-1.5, 0.5):
            p.beam((-side * 0.9, y, CH - 0.32), (-side * 0.9, y, CH - 0.27), 0.02, "metal_dark")
        for k in range(3):
            p.beam((-side * 0.9 - 0.1 + k * 0.1, -CL / 2, CH - 0.3), (-side * 0.9 - 0.1 + k * 0.1, CL / 2, CH - 0.3),
                   0.025, "black", segs=4)
    if lamp:
        p.box((1.25, 0.32, 0.08), (0, 0.4, CH - 0.29), "metal", bevel=0.01)
        p.box((1.15, 0.24, 0.02), (0, 0.4, CH - 0.34), "fluorescent")
        for x in (-0.5, 0.5):
            p.beam((x, 0.4, CH - 0.25), (x, 0.4, CH - 0.06), 0.01, "metal_dark")
    # пятна и лужи на полу, трещины на стене
    rng = p.rng
    for _ in range(2):
        x, y = rng.uniform(-1.4, 1.4), rng.uniform(-1.6, 1.6)
        p.cyl(rng.uniform(0.2, 0.5), 0.004, (x, y, 0.006), "water_dark", segs=8, jitter=0.06)
    p.cyl(0.18, 0.008, (0.6, -1.3, 0.004), "metal_dark", segs=8)  # трап
    for k in range(4):
        p.box((0.3, 0.02, 0.01), (0.6, -1.3 - 0.09 + k * 0.06, 0.01), "black")


def corridor_straight():
    """Прямой модуль коридора: окрашенные стены, трубы, лоток с кабелями, лампа, трап, лужи."""
    p = Prop("corridor_straight")
    _shell(p)
    p.text("37", (CW / 2 + 0.005 - 0.01, 1.2, 1.9), 0.35, "whitewash", depth=0.01, rot=(90, 0, 90))
    p.box((0.01, 0.4, 0.3), (-CW / 2 - 0.005 + 0.01 - 0.0, -0.6, 1.0), "metal_dark")  # электрощиток
    p.box((0.02, 0.3, 0.2), (-CW / 2 + 0.02, -0.6, 1.0), "paint_yellow")
    p.cable((-CW / 2 + 0.03, -0.6, 1.15), (-CW / 2 + 0.03, -0.6, CH - 0.35), 0.0)
    return p


def corridor_dead_end():
    """Тупик: торцевая стена с замурованным проёмом и стрелкой назад."""
    p = Prop("corridor_dead_end")
    _shell(p, end=True)
    y = CL / 2 - T - 0.01
    p.box((1.1, 0.02, 2.1), (0, y, 1.05), "brick")
    p.box((1.3, 0.03, 0.1), (0, y, 2.15), "concrete_dark")
    p.box((0.8, 0.005, 0.08), (0.9, y - 0.015, 1.7), "chalk", rot=(0, 0, 0))
    p.beam((0.5, y - 0.015, 1.7), (0.65, y - 0.015, 1.82), 0.06, "chalk")
    p.beam((0.5, y - 0.015, 1.7), (0.65, y - 0.015, 1.58), 0.06, "chalk")
    return p


def corridor_door_side():
    """Модуль с дверным проёмом в правой стене (под Смотрителя, сек. 36)."""
    p = Prop("corridor_door_side")
    _shell(p, right=False)
    x = CW / 2 + T / 2
    _wall(p, x, -CL / 2, -0.5, 1)
    _wall(p, x, 0.5, CL / 2, 1)
    p.box_floor((T, 1.0, 0.8), (x, 0, 2.2), "concrete")
    for yy in (-0.52, 0.52):
        p.box_floor((T + 0.04, 0.06, 2.2), (x, yy, 0), "metal_dark")
    p.box((T + 0.04, 1.1, 0.06), (x, 0, 2.2), "metal_dark")
    p.box((0.02, 0.4, 0.15), (CW / 2 - 0.01, 0, 2.45), "paper")
    p.text("№ 36", (CW / 2 - 0.025, 0, 2.45), 0.08, "black", depth=0.006, rot=(90, 0, -90))
    p.box((0.12, 0.08, 0.06), (CW / 2 - 0.06, 0.75, 2.4), "led_red")
    return p


def corridor_t_junction():
    p = Prop("corridor_t_junction")
    _shell(p, left=False)
    x = -CW / 2 - T / 2
    for y0, y1 in ((-CL / 2, -CL / 2 + 0.5), (CL / 2 - 0.5, CL / 2)):
        _wall(p, x, y0, y1, -1)
    p.box_floor((T, CL - 1.0, 0.6), (x, 0, CH - 0.6), "concrete")
    p.text("← 38", (-CW / 2 + 0.3, CL / 2 - 0.251, 2.0), 0.25, "whitewash", depth=0.005, rot=(90, 0, 180))
    return p


def corridor_corner():
    p = Prop("corridor_corner")
    _shell(p, left=False, end=True)
    p.box_floor((T, T, CH), (-CW / 2 - T / 2, -CL / 2 + T / 2, 0), "concrete")
    p.box_floor((0.2, 0.2, CH), (CW / 2 - 0.1, CL / 2 - T - 0.1, 0), "concrete")  # колонна в углу
    return p


def threshold_seam():
    """Порог (сек. 30): фасад панельки со светом в окнах перетекает в гладкий бетон Гигадома без шва."""
    p = Prop("threshold_seam")
    _shell(p, left=False, pipes=False)
    x = -CW / 2 - T / 2
    p.box_floor((T, CL / 2, CH), (x, -CL / 4, 0), "panel_wall")
    p.box_floor((T, CL / 2, CH), (x, CL / 4, 0), "concrete")
    p.collider((T, CL, CH), (x, 0, CH / 2))
    xi = x + T / 2 + 0.01
    for i in range(3):
        y = -CL / 2 + 0.35 + i * 0.55
        p.box((0.02, 0.4, 0.45), (xi, y, 1.6), "window_lit")
        p.box((0.03, 0.44, 0.04), (xi, y, 1.36), "whitewash")
        p.box((0.03, 0.03, 0.45), (xi, y, 1.6), "whitewash")
    p.box((0.02, 0.5, 0.6), (xi, -0.2, 0.3), "paper_old")  # отклеенное объявление
    for k in range(5):  # переходная полоса — плитки панели «растворяются» в бетоне
        p.box((0.02, 0.12, 0.12), (xi, 0.1 + k * 0.18, 0.4 + (k * 37 % 5) * 0.4), "panel_wall")
    return p


def fluorescent_lamp():
    """Потолочная люминесцентная лампа на подвесах с решёткой. Опора — потолок."""
    p = Prop("fluorescent_lamp")
    for x in (-0.5, 0.5):
        p.beam((x, 0, 0), (x, 0, -0.25), 0.01, "metal_dark")
    p.box((1.25, 0.32, 0.08), (0, 0, -0.29), "metal", bevel=0.01)
    p.box((1.15, 0.24, 0.02), (0, 0, -0.34), "fluorescent")
    for k in range(5):
        p.box((0.01, 0.26, 0.01), (-0.45 + k * 0.225, 0, -0.355), "metal_dark")
    return p


def steel_door():
    """Глухая металлическая дверь Гигадома: рёбра жёсткости, ржавчина, засов, номер."""
    p = Prop("steel_door")
    p.box((1.25, 0.26, 0.12), (0, 0, 2.16), "metal_dark", bevel=0.01)
    for x in (-0.57, 0.57):
        p.box((0.12, 0.26, 2.22), (x, 0, 1.11), "metal_dark", bevel=0.01)
    p.box((1.02, 0.07, 2.1), (0, 0, 1.05), "rust")
    for z in (0.35, 1.05, 1.75):
        p.box((0.95, 0.04, 0.06), (0, -0.05, z), "metal_dark")
    p.beam((-0.4, -0.05, 0.4), (0.4, -0.05, 1.7), 0.05, "metal_dark")
    for z in (0.3, 1.9):
        p.cyl(0.03, 0.14, (-0.58, -0.08, z - 0.07), "metal", segs=6)
    p.box((0.35, 0.05, 0.05), (0.25, -0.09, 1.0), "metal")
    p.box((0.05, 0.08, 0.15), (0.43, -0.09, 1.0), "metal_dark")
    p.box((0.25, 0.01, 0.15), (0, -0.075, 1.85), "paper")
    p.text("Д-14", (0, -0.082, 1.85), 0.08, "black", depth=0.004)
    return p.collider((1.25, 0.26, 2.22), (0, 0, 1.11))


def bunk_bed():
    """Казармы (сек. 33): двухъярусная армейская койка, матрасы, скатки, лестница, тумбочка."""
    p = Prop("bunk_bed")
    L, W = 1.95, 0.85
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.box_floor((0.05, 0.05, 1.75), (sx * L / 2, sy * W / 2, 0), "metal_dark")
    for z in (0.4, 1.3):
        for sy in (-1, 1):
            p.box((L, 0.04, 0.06), (0, sy * W / 2, z), "metal_dark")
        for k in range(8):
            p.box((0.02, W, 0.01), (-L / 2 + 0.12 + k * 0.24, 0, z), "metal")
        p.box((L - 0.1, W - 0.1, 0.12), (0, 0, z + 0.08), "cloth_blue", bevel=0.03)
        p.box((0.35, W - 0.2, 0.1), (L / 2 - 0.3, 0, z + 0.18), "cloth_white", bevel=0.03)
        p.cyl(0.08, W - 0.2, (-L / 2 + 0.25, 0, z + 0.22), "paint_army", segs=6, rot=(90, 0, 0))
    for sx in (-1, 1):
        p.box((0.04, W, 0.04), (sx * L / 2, 0, 1.72), "metal_dark")
    for k in range(4):  # лестница
        p.box((0.02, 0.3, 0.02), (-L / 2 - 0.03, -0.2 + 0.0, 0.5 + k * 0.28), "metal")
    p.box_floor((0.45, 0.4, 0.6), (L / 2 + 0.3, 0, 0), "wood_old", bevel=0.01)
    p.box((0.4, 0.01, 0.2), (L / 2 + 0.3, -0.205, 0.4), "wood")
    p.tube(0.04, 0.035, 0.09, (L / 2 + 0.25, 0.05, 0.6), "enamel", segs=8)
    return p.collider((L + 0.05, W + 0.05, 1.75), (0, 0, 0.875))


def loudspeaker_horn():
    """Радиоузел: рупорный громкоговоритель на кронштейне, с проводом. Опора — стена (Y=0)."""
    p = Prop("loudspeaker_horn")
    p.box((0.2, 0.02, 0.3), (0, 0.01, 0), "metal_dark")
    p.beam((0, 0.0, 0.1), (0, -0.3, 0.0), 0.04, "metal_dark")
    p.beam((0, 0.0, -0.1), (0, -0.3, 0.0), 0.04, "metal_dark")
    p.cyl(0.11, 0.16, (0, -0.3, 0), "paint_army", segs=10, rot=(90, 0, 0))
    p.cyl(0.08, 0.5, (0, -0.46, 0), "paint_army", segs=10, rot=(90, 0, 0), r2=0.33)
    p.cyl(0.3, 0.02, (0, -0.94, 0), "metal_dark", segs=10, rot=(90, 0, 0), r2=0.34)
    p.cyl(0.05, 0.3, (0, -0.6, 0), "black", segs=8, rot=(90, 0, 0))
    p.cable((0, 0.0, -0.15), (0.1, 0.0, -1.0), 0.05)
    return p


def meat_hook_rail():
    """Мясник (сек. 37): подвесной рельс с роликами, крюками и неровными тушами. Модуль 4 м, опора — потолок."""
    p = Prop("meat_hook_rail")
    for x in (-1.8, 0, 1.8):
        p.beam((x, 0, 0), (x, 0, -0.1), 0.05, "metal_dark")
    p.box((4.0, 0.06, 0.1), (0, 0, -0.14), "metal_dark")
    p.box((4.0, 0.12, 0.02), (0, 0, -0.19), "rust")
    for i, x in enumerate((-1.6, -0.8, 0.0, 0.8, 1.6)):
        p.cyl(0.04, 0.03, (x, 0.0, -0.21), "metal", segs=8, rot=(90, 0, 0))
        p.beam((x, 0, -0.22), (x, 0, -0.42), 0.02, "metal")
        p.arc_tube((x - 0.045, 0, -0.45), 0.045, 0, -200, 0.015, "metal", steps=5)
        if i == 2:
            continue
        top = -0.5
        p.blob(0.22, (x, 0, top - 0.45), "meat", scale=(0.9, 0.6, 2.3), jitter=0.2)
        p.blob(0.12, (x + 0.05, 0.02, top - 0.12), "porcelain", scale=(1.0, 0.8, 1.2), jitter=0.2)  # жир
        for s in (-1, 1):  # рёбра
            for k in range(4):
                p.beam((x + s * 0.05, -0.12, top - 0.35 - k * 0.12), (x + s * 0.18, -0.08, top - 0.42 - k * 0.12), 0.02,
                       "sinew")
        p.cyl(0.03, 0.12, (x, 0, top - 1.1), "porcelain", segs=5, rot=(180, 0, 0))
    # капли на полу ниже? — нет: модель потолочная. Свисающая цепь
    for k in range(6):
        p.box((0.02, 0.04, 0.06), (-1.2, 0, -0.25 - k * 0.07), "metal", rot=(0, 0, 90 * (k % 2)))
    return p


def butcher_table():
    """Разделочный стол: толстая колода с выщерблинами, тесак, крюки, ведро."""
    p = Prop("butcher_table")
    p.box_floor((1.6, 0.8, 0.14), (0, 0, 0.76), "wood_old", bevel=0.02, jitter=0.005)
    p.box((0.6, 0.35, 0.004), (-0.3, 0.05, 0.902), "crimson")
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.box_floor((0.08, 0.08, 0.76), (sx * 0.7, sy * 0.32, 0), "metal_dark")
        p.box((0.06, 0.6, 0.04), (sx * 0.7, 0, 0.2), "metal_dark")
    p.box((1.4, 0.04, 0.04), (0, 0, 0.2), "metal_dark")
    p.box((0.28, 0.1, 0.008), (0.35, 0.1, 0.906), "metal")      # тесак
    p.box((0.14, 0.03, 0.025), (0.13, 0.1, 0.912), "wood_dark")
    p.blob(0.08, (0.05, -0.2, 0.93), "meat", scale=(1.4, 1, 0.6), jitter=0.3)
    p.tube(0.17, 0.155, 0.32, (0.9, -0.5, 0), "metal", segs=10)
    p.cyl(0.155, 0.005, (0.9, -0.5, 0.25), "crimson", segs=10)
    p.arc_tube((0.9, -0.5, 0.32), 0.16, 0, 180, 0.012, "metal", steps=6)
    return p.collider((1.6, 0.8, 0.9), (0, 0, 0.45))


def sign_weapon_sheath():
    """Табличка «ОРУЖИЕ В ЧЕХОЛ» (сек. 37): эмалированная, со сколами и шурупами. Крепление к стене."""
    p = Prop("sign_weapon_sheath")
    p.box((0.9, 0.025, 0.42), (0, 0, 0.21), "calendar_red", bevel=0.01)
    p.box((0.84, 0.03, 0.36), (0, -0.002, 0.21), "enamel")
    p.text("ОРУЖИЕ", (0, -0.02, 0.28), 0.1, "calendar_red", depth=0.006)
    p.text("В ЧЕХОЛ", (0, -0.02, 0.14), 0.1, "calendar_red", depth=0.006)
    for x in (-0.41, 0.41):
        for z in (0.03, 0.39):
            p.cyl(0.012, 0.01, (x, -0.015, z), "metal", segs=6, rot=(90, 0, 0))
    for x, z in ((0.3, 0.05), (-0.25, 0.37), (0.38, 0.3)):  # сколы эмали
        p.cyl(0.02, 0.032, (x, -0.0, z), "black", segs=5, rot=(90, 0, 0), jitter=0.006)
    return p


def sinew_ceiling():
    """Ткач (сек. 34): паутина сухожилий под потолком 4×4 м — свежие (блестят), старые (тёмные), узлы. Опора — потолок."""
    p = Prop("sinew_ceiling")
    rng = p.rng
    anchors = [(rng.uniform(-1.9, 1.9), rng.choice((-1.95, 1.95)), 0) for _ in range(6)] + \
              [(rng.choice((-1.95, 1.95)), rng.uniform(-1.9, 1.9), -rng.uniform(0, 0.8)) for _ in range(6)]
    for i in range(18):
        a = anchors[i % len(anchors)]
        b = anchors[(i * 5 + 3) % len(anchors)]
        if a == b:
            continue
        m = "sinew" if i % 3 == 0 else "sinew_old"
        p.curve_tube(p.sag(a, b, rng.uniform(0.3, 1.0), 9), 0.035 if m == "sinew" else 0.025, m, segs=5)
    for _ in range(5):  # узлы-сплетения
        p.blob(0.08, (rng.uniform(-1, 1), rng.uniform(-1, 1), -rng.uniform(0.3, 0.7)), "sinew_old", jitter=0.4)
    for _ in range(7):  # свисающие нити
        x, y = rng.uniform(-1.6, 1.6), rng.uniform(-1.6, 1.6)
        p.curve_tube([(x, y, 0), (x + 0.05, y, -0.8), (x - 0.03, y + 0.04, -rng.uniform(1.2, 1.8))], 0.02, "sinew", segs=4)
    return p


def cocoon():
    """Свёрток Ткача на нити: под оплёткой угадывается силуэт. Опора — потолок."""
    p = Prop("cocoon")
    for dx in (-0.06, 0, 0.07):
        p.curve_tube([(dx * 3, 0, 0), (dx, 0, -0.4), (0, 0, -0.75)], 0.02, "sinew", segs=4)
    p.blob(0.25, (0, 0, -1.4), "sinew_old", scale=(0.9, 0.8, 2.5), jitter=0.12, subdiv=2)
    p.blob(0.14, (0, -0.02, -0.85), "sinew_old", scale=(1, 0.9, 1.1), jitter=0.15)
    for k in range(9):  # обмотка — витки по спирали
        z = -0.85 - k * 0.14
        r = 0.22 * math.sin(math.pi * (k + 1) / 10) + 0.08
        p.arc_tube((0, 0, z), r, k * 40, k * 40 + 250, 0.025, "sinew", steps=6, plane="xy")
    p.box((0.04, 0.15, 0.03), (0.2, -0.05, -1.6), "skin", rot=(0, 30, 0))  # рука
    return p


def vent_duct():
    """Точильщик (сек. 39): вентиляционный короб с фланцами, заклёпками, решётками и подвесами. Модуль 4 м."""
    p = Prop("vent_duct")
    p.box_floor((1.2, 4.0, 0.9), (0, 0, 0), "metal")
    p.box_floor((1.12, 3.98, 0.82), (0, 0, 0.04), "black")
    for y in (-2, -1, 0, 1, 2):
        p.box_floor((1.28, 0.05, 0.98), (0, y if abs(y) < 2 else y * 0.9875, -0.04), "metal_dark")
        for x in (-0.6, 0.6):
            for z in (0.1, 0.45, 0.8):
                p.sphere(0.012, (x * 1.06, y, z), "metal", segs=5, rings=3)
    for y in (-1.5, 0.5):
        p.box((0.5, 0.02, 0.3), (0, y, 0.45), "metal_dark")
        for k in range(6):
            p.box((0.02, 1.22, 0.02), (0, y, 0.33 + k * 0.045), "metal_dark")
        p.box((0.02, 0.5, 0.35), (0.61, y, 0.45), "metal_dark")
    for y in (-1.5, 1.5):  # подвесы к потолку
        for x in (-0.65, 0.65):
            p.beam((x, y, 0.9), (x, y, 1.6), 0.02, "metal_dark")
        p.box((1.4, 0.05, 0.04), (0, y, 0.92), "metal_dark")
    p.box((0.03, 0.3, 0.12), (0.62, 1.0, 0.3), "paper_old")  # бирка
    return p


def grate_walkway():
    """Решётчатый металлический настил 2×4 м с поручнем (по нему — только шагом)."""
    p = Prop("grate_walkway")
    for y in range(-19, 20):
        p.box((2.0, 0.025, 0.04), (0, y * 0.1, 0), "metal")
    for x in (-0.95, -0.3, 0.3, 0.95):
        p.box((0.04, 4.0, 0.1), (x, 0, -0.04), "metal_dark")
    for x in (-1.0, 1.0):
        p.box((0.04, 4.0, 0.12), (x, 0, 0.0), "rust")
        for y in (-1.9, -0.6, 0.6, 1.9):
            p.beam((x, y, 0.06), (x, y, 1.0), 0.04, "metal_dark")
        p.beam((x, -2, 1.0), (x, 2, 1.0), 0.05, "metal_dark", segs=6)
        p.beam((x, -2, 0.5), (x, 2, 0.5), 0.03, "metal_dark", segs=6)
    return p.collider((2.0, 4.0, 0.08), (0, 0, -0.02)).collider((0.05, 4.0, 1.0), (-1, 0, 0.5)).collider(
        (0.05, 4.0, 1.0), (1, 0, 0.5))


def elevator_shaft():
    """Смотрящий из шахты (сек. 49): открытая лифтовая шахта, тросы, направляющие, сорванные двери, на дне — глаз."""
    p = Prop("elevator_shaft")
    S, Dp = 2.4, 8.0
    for sx in (-1, 1):
        p.box_floor((0.3, S + 0.6, Dp), (sx * (S / 2 + 0.15), 0, -Dp), "concrete")
        p.box_floor((S, 0.3, Dp), (0, sx * (S / 2 + 0.15), -Dp), "concrete")
        p.box_floor((0.08, 0.12, Dp), (sx * (S / 2 - 0.04), 0.3, -Dp), "rust")  # направляющие
        p.collider((0.3, S + 0.6, Dp), (sx * (S / 2 + 0.15), 0, -Dp / 2))
        p.collider((S, 0.3, Dp), (0, sx * (S / 2 + 0.15), -Dp / 2))
    for k in range(1, 4):  # отметки этажей
        p.box((S, 0.02, 0.2), (0, S / 2 - 0.01, -k * 2.4), "concrete_dark")
        p.text(str(49 - k), (0.8, S / 2 - 0.02, -k * 2.4 + 0.4), 0.25, "paint_yellow", depth=0.01, rot=(90, 0, 180))
    p.box_floor((S, S, 0.2), (0, 0, -Dp - 0.2), "black")
    p.cyl(1.05, 0.05, (0, 0, -Dp - 0.02), "crimson", segs=14, jitter=0.05)
    p.sphere(0.9, (0, 0, -Dp + 0.1), "eye_white", segs=14, rings=7, scale=(1, 0.62, 0.35))
    p.cyl(0.42, 0.34, (0, 0, -Dp), "eye_iris", segs=14)
    p.cyl(0.32, 0.345, (0, 0, -Dp), "rust", segs=14)
    p.cyl(0.16, 0.35, (0, 0, -Dp), "black", segs=12)
    for k in range(10):  # прожилки
        a = k * math.tau / 10
        p.beam((0.45 * math.cos(a), 0.3 * math.sin(a), -Dp + 0.3), (0.85 * math.cos(a), 0.55 * math.sin(a), -Dp + 0.15),
               0.02, "crimson")
    for x in (-0.3, 0.3):  # тросы
        p.beam((x, 0, 0.8), (x * 0.8, 0.1, -Dp + 2.0), 0.025, "metal_dark", segs=4)
    p.beam((-0.6, 0, 0.8), (0.6, 0, 0.8), 0.15, "metal_dark")
    for sx in (-1, 1):  # бортик и сорванная створка
        p.box_floor((S + 0.6, 0.1, 0.15), (0, sx * (S / 2 + 0.25), 0), "paint_yellow")
    p.box((0.9, 0.05, 2.0), (0.5, -S / 2 + 0.2, -Dp + 0.8), "metal", rot=(70, 10, 20))
    return p


def key_wall():
    """Хозяин ключей (сек. 40): доска с сотнями ключей на гвоздях и бирках. 4×2 м, к стене."""
    p = Prop("key_wall")
    p.box_floor((4.1, 0.06, 2.3), (0, 0.03, 0.55), "wood_dark", bevel=0.01)
    rng = p.rng
    for r in range(7):
        p.box((4.0, 0.02, 0.03), (0, -0.005, 0.72 + r * 0.3), "wood")
        for c in range(16):
            if rng.random() < 0.08:
                continue  # пустые гвозди — чьи-то ключи забрали
            x, z = -1.85 + c * 0.247, 0.7 + r * 0.3
            p.cyl(0.006, 0.03, (x, -0.01, z), "metal", segs=4, rot=(90, 0, 0))
            m = "gold" if rng.random() < 0.7 else "metal"
            ang = rng.uniform(-12, 12)
            p.cyl(0.03, 0.006, (x, -0.02, z - 0.04), m, segs=6, rot=(90, ang, 0))
            p.box((0.012, 0.006, 0.1), (x + 0.0, -0.02, z - 0.12), m, rot=(0, ang, 0))
            if rng.random() < 0.35:
                p.box((0.04, 0.004, 0.06), (x + 0.03, -0.024, z - 0.08), "paper_old", rot=(0, ang + 10, 0))
    return p


def key_counter():
    """Стойка Хозяина: деревянная конторка с журналом, лампой и звонком."""
    p = Prop("key_counter")
    p.box_floor((2.4, 0.8, 1.05), (0, 0, 0), "wood", bevel=0.01)
    for x in (-0.8, 0, 0.8):
        p.box((0.7, 0.02, 0.8), (x, -0.405, 0.55), "wood_dark")
    p.box_floor((2.5, 0.9, 0.05), (0, 0, 1.05), "wood_dark", bevel=0.01)
    p.box((0.4, 0.3, 0.03), (-0.5, 0, 1.115), "paper_old", rot=(0, 0, 6))
    p.box((0.4, 0.3, 0.01), (-0.5, 0, 1.135), "paper", rot=(0, 0, 6))
    p.cyl(0.08, 0.02, (0.6, 0.15, 1.1), "metal_dark", segs=8)
    p.beam((0.6, 0.15, 1.12), (0.6, 0.1, 1.45), 0.015, "metal_dark")
    p.cyl(0.1, 0.12, (0.6, 0.0, 1.38), "paint_green", segs=8, r2=0.05, rot=(-30, 0, 0))
    p.sphere(0.04, (0.2, -0.2, 1.12), "gold", segs=8, rings=4, scale=(1, 1, 0.7))
    return p.collider((2.5, 0.9, 1.1), (0, 0, 0.55))


def golden_key():
    """Ключ, «не подходящий ни к чему полезному»: витая головка, бородка, бирка на кольце."""
    p = Prop("golden_key")
    p.arc_tube((0, 0, 0.006), 0.035, 0, 360, 0.012, "gold", steps=10, plane="xy")
    p.cyl(0.012, 0.012, (0, 0, 0), "gold", segs=6)
    p.cyl(0.008, 0.16, (0.035, 0, 0.006), "gold", segs=6, rot=(0, 90, 0))
    for k, h in enumerate((0.04, 0.025, 0.035)):
        p.box((0.014, 0.006, h), (0.16 + k * 0.016, 0, 0.006 - h / 2), "gold")
    p.arc_tube((-0.05, 0, 0.004), 0.018, 0, 360, 0.004, "metal", steps=8, plane="xy")
    p.box((0.05, 0.03, 0.002), (-0.09, 0, 0.002), "paper_old")
    return p


def junk_pile():
    """Сборщик (сек. 44): куча обронённого снаряжения: рюкзаки, ящики, фонари, каски, ботинки."""
    p = Prop("junk_pile")
    p.blob(1.3, (0, 0, 0), "concrete_dark", scale=(1.1, 0.8, 0.5), jitter=0.15, subdiv=2)
    rng = p.rng
    for _ in range(4):  # рюкзаки
        x, y = rng.uniform(-0.8, 0.8), rng.uniform(-0.5, 0.4)
        z = 0.6 * (1 - (x / 1.4) ** 2) * (1 - (y / 1.0) ** 2) + 0.05
        rot = (rng.uniform(-30, 30), rng.uniform(-30, 30), rng.uniform(0, 360))
        p.box((0.4, 0.25, 0.5), (x, y, z), "paint_army", rot=rot, bevel=0.06)
        p.box((0.3, 0.06, 0.2), (x, y - 0.15, z - 0.05), "paint_army", rot=rot, bevel=0.02)
    for _ in range(3):
        x, y = rng.uniform(-1, 1), rng.uniform(-0.6, 0.5)
        p.box((0.45, 0.3, 0.3), (x, y, 0.35), "wood_old", rot=(rng.uniform(-20, 20), 0, rng.uniform(0, 90)), bevel=0.01)
    for _ in range(3):  # каски
        x, y = rng.uniform(-1.1, 1.1), rng.uniform(-0.7, 0.6)
        p.sphere(0.15, (x, y, 0.35), "paint_army", segs=8, rings=4, scale=(1, 1.1, 0.7), rot=(rng.uniform(-60, 60), 0, 0))
    for _ in range(3):  # фонари
        x, y = rng.uniform(-1.0, 1.0), rng.uniform(-0.7, 0.6)
        p.cyl(0.025, 0.22, (x, y, 0.45), "black", segs=6, rot=(rng.uniform(60, 120), 0, rng.uniform(0, 360)))
    for _ in range(4):  # ботинки
        x, y = rng.uniform(-1.3, 1.3), rng.uniform(-0.9, 0.7)
        p.box((0.28, 0.11, 0.1), (x, y, 0.1), "black", rot=(0, 0, rng.uniform(0, 360)), bevel=0.03)
    p.beam((-1.2, -0.5, 0.05), (0.4, 0.3, 0.9), 0.04, "wood")  # шест
    p.blob(0.25, (0.5, 0.4, 0.75), "cloth_gray", scale=(1.5, 1, 0.4), jitter=0.3)
    return p.collider((2.8, 2.0, 0.8), (0, 0, 0.4))


def chalk_mark():
    """Эхо (сек. 43): метка мелом — стрелка, галочка, крестик и число. Плоская, на стену."""
    p = Prop("chalk_mark")
    p.beam((-0.25, 0, 0.3), (0.25, 0, 0.3), 0.035, "chalk")
    p.beam((0.25, 0, 0.3), (0.1, 0, 0.42), 0.035, "chalk")
    p.beam((0.25, 0, 0.3), (0.1, 0, 0.18), 0.035, "chalk")
    p.beam((-0.2, 0, 0.12), (-0.12, 0, 0.04), 0.03, "chalk")
    p.beam((-0.12, 0, 0.04), (0.04, 0, 0.2), 0.03, "chalk")
    p.text("43", (0.2, -0.004, 0.08), 0.1, "chalk", depth=0.003)
    return p


def flashlight_cold():
    """Холодный свет (сек. 41): армейский угловой фонарь с ребристым корпусом, линзой, ремешком."""
    p = Prop("flashlight")
    p.box_floor((0.07, 0.04, 0.13), (0, 0, 0), "paint_army", bevel=0.008)
    for k in range(5):
        p.box((0.075, 0.042, 0.006), (0, 0, 0.02 + k * 0.02), "black")
    p.cyl(0.03, 0.03, (0, -0.02, 0.1), "paint_army", segs=10, rot=(90, 0, 0))
    p.cyl(0.024, 0.004, (0, -0.05, 0.1), "floodlight", segs=10, rot=(90, 0, 0))
    p.box((0.02, 0.01, 0.03), (0.03, 0, 0.135), "black")
    p.box((0.05, 0.008, 0.1), (0, 0.024, 0.06), "black")
    return p


def threshold_two_end():
    """Порог второй (сек. 50): коридор обрывается во тьму и стоячую воду, ступени вниз, табличка «→ 51»."""
    p = Prop("threshold_two_end")
    _shell(p, lamp=False)
    p.box((CW, 0.02, CH), (0, CL / 2, CH / 2), "black")
    p.box((CW, CL / 2, 0.02), (0, CL / 4, -0.05), "water_dark")
    for k in range(3):
        p.box_floor((CW, 0.3, 0.12), (0, -0.15 - k * 0.3 + 0.3, -0.36 + (2 - k) * 0.12 - 0.0), "concrete_dark")
    p.box((1.0, 0.03, 0.25), (0, CL / 2 - 0.05, CH - 0.45), "enamel")
    p.text("→ 51", (0, CL / 2 - 0.07, CH - 0.45), 0.15, "black", depth=0.005)
    p.box((0.4, 0.2, 0.06), (-1.0, 0.6, CH - 0.29), "metal")  # погасшая лампа
    p.box((0.36, 0.14, 0.02), (-1.0, 0.6, CH - 0.33), "window_dark")
    p.cable((-1.0, 0.6, CH - 0.3), (-1.1, 0.9, CH - 1.2), 0.0)
    return p


# --- новые объекты Гигадома
def concrete_stairs():
    """Бетонная лестница между уровнями секций: 12 ступеней, площадка, трубчатые перила. Подъём 2 м."""
    p = Prop("concrete_stairs")
    for i in range(12):
        p.box_floor((1.6, 0.28, (i + 1) * 0.166), (0, -1.54 + i * 0.28, 0), "concrete")
        p.box((1.6, 0.03, 0.02), (0, -1.54 + i * 0.28 - 0.13, (i + 1) * 0.166), "metal_dark")
    p.box_floor((1.6, 1.4, 2.0), (0, 2.22, 0), "concrete")
    for x in (-0.78, 0.78):
        p.beam((x, -1.7, 0.95), (x, 1.6, 2.95), 0.05, "paint_yellow", segs=6)
        for i in range(0, 12, 3):
            y = -1.54 + i * 0.28
            p.beam((x, y, (i + 1) * 0.166), (x, y, (i + 1) * 0.166 + 0.9), 0.03, "metal_dark", segs=5)
    p.collider((1.6, 3.4, 1.0), (0, 0.0, 0.5), 0).collider((1.6, 1.4, 2.0), (0, 2.22, 1.0))
    return p


def barrel_rusty():
    """Ржавая бочка с потёками: для захламления коридоров."""
    p = Prop("barrel_rusty")
    p.cyl(0.29, 0.88, (0, 0, 0), "rust", segs=12)
    for z in (0.05, 0.3, 0.58, 0.83):
        p.cyl(0.3, 0.035, (0, 0, z), "metal_dark", segs=12)
    p.cyl(0.04, 0.02, (0.15, 0.05, 0.88), "metal_dark", segs=6)
    p.cyl(0.4, 0.003, (0.1, -0.1, 0.0), "water_dark", segs=8, jitter=0.05)
    return p.collider((0.6, 0.6, 0.9), (0, 0, 0.45))


def metal_cabinet():
    """Металлический шкаф-локер на 3 секции с вентиляционными прорезями, одна дверца приоткрыта."""
    p = Prop("metal_cabinet")
    p.box_floor((1.2, 0.5, 1.9), (0, 0, 0), "paint_army", bevel=0.01)
    for i, x in enumerate((-0.4, 0, 0.4)):
        rot = -35 if i == 2 else 0
        cx = x + (0.0 if i != 2 else 0.08)
        cy = -0.26 if i != 2 else -0.37
        p.box((0.38, 0.02, 1.8), (cx, cy, 0.95), "paint_army", rot=(0, 0, rot))
        for k in range(4):
            p.box((0.2, 0.025, 0.012), (cx, cy - 0.003, 1.65 + k * 0.04), "black", rot=(0, 0, rot))
        p.box((0.02, 0.03, 0.08), (cx + 0.15, cy - 0.02, 1.0), "metal", rot=(0, 0, rot))
        p.box((0.1, 0.025, 0.05), (cx, cy - 0.003, 1.45), "paper", rot=(0, 0, rot))
    p.box((0.38, 0.45, 0.02), (0.4, 0.0, 1.4), "metal")
    p.box((0.25, 0.2, 0.3), (0.35, 0.0, 1.56), "paint_army")
    return p.collider((1.2, 0.5, 1.9), (0, 0, 0.95))


PROPS = [
    corridor_straight, corridor_dead_end, corridor_door_side, corridor_t_junction, corridor_corner,
    threshold_seam, fluorescent_lamp, steel_door, bunk_bed, loudspeaker_horn, meat_hook_rail,
    butcher_table, sign_weapon_sheath, sinew_ceiling, cocoon, vent_duct, grate_walkway,
    elevator_shaft, key_wall, key_counter, golden_key, junk_pile, chalk_mark, flashlight_cold,
    threshold_two_end, concrete_stairs, barrel_rusty, metal_cabinet,
]
