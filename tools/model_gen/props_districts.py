"""Акт 1 — Районы (01–30): панельный спальный район, где опасна сама нормальность."""
import math
from mg_lib import Prop

CATEGORY = "districts"

SHIRT = [(-0.3, 0), (0.3, 0), (0.3, 0.42), (0.45, 0.32), (0.55, 0.45), (0.3, 0.6),
         (0.1, 0.6), (0, 0.55), (-0.1, 0.6), (-0.3, 0.6), (-0.55, 0.45), (-0.45, 0.32), (-0.3, 0.42)]
PANTS = [(-0.25, 0), (-0.05, 0), (0, 0.4), (0.05, 0), (0.25, 0), (0.22, 0.75), (-0.22, 0.75)]
DRESS = [(-0.4, 0), (0.4, 0), (0.18, 0.55), (0.3, 0.8), (0.12, 0.85), (0, 0.8), (-0.12, 0.85),
         (-0.3, 0.8), (-0.18, 0.55)]


def _window_unit(p, x, y, z, lit, facing=-1, w=1.4, h=1.4, curtain=None):
    """Окно панельки: стекло, рама с форточкой, отлив, иногда штора/занавеска."""
    fy = y + facing * 0.02
    p.box((w, 0.06, h), (x, fy, z), "window_lit" if lit else "window_dark")
    p.box((0.06, 0.08, h), (x - w * 0.18, fy + facing * 0.01, z), "whitewash")
    p.box((w, 0.08, 0.05), (x, fy + facing * 0.01, z + h * 0.2), "whitewash")
    p.box((w + 0.1, 0.09, 0.06), (x, fy + facing * 0.01, z + h / 2), "whitewash")
    p.box((w + 0.1, 0.09, 0.06), (x, fy + facing * 0.01, z - h / 2), "whitewash")
    p.box((w + 0.2, 0.16, 0.04), (x, y + facing * 0.08, z - h / 2 - 0.04), "metal", rot=(facing * -10, 0, 0))
    if curtain:
        cx = x + (w * 0.3 if curtain == "r" else -w * 0.3)
        p.box((w * 0.35, 0.02, h * 0.9), (cx, y + facing * 0.005, z), "cloth_check" if lit else "cloth_gray")


def panel_building_section():
    """Секция панельного дома 9 этажей: окна с рамами, балконы, водосток, кондиционеры, антенны.
    Модуль 12 м — ставить секции вплотную по X."""
    p = Prop("panel_building_section")
    w, d, fh, floors = 12.0, 12.0, 2.8, 9
    h = fh * floors
    p.box_floor((w, d, 0.6), (0, 0, 0), "concrete_dark")  # цоколь
    p.box_floor((w, d, h - 0.6), (0, 0, 0.6), "panel_wall")
    p.box_floor((w + 0.3, d + 0.3, 0.45), (0, 0, h), "concrete_dark")  # парапет
    p.box_floor((w - 0.2, d - 0.2, 0.2), (0, 0, h), "asphalt")
    p.box_floor((2.2, 2.6, 1.8), (2.5, 1.0, h + 0.2), "panel_wall")  # машинное помещение лифта
    p.box((0.9, 0.05, 1.6), (2.5, -0.32, h + 1.0), "rust")
    for ax in (-3.5, 4.4):  # телеантенны
        p.beam((ax, 2, h + 0.2), (ax, 2, h + 2.6), 0.04, "metal_dark")
        for k in range(3):
            p.beam((ax - 0.5 + k * 0.1, 2, h + 2.0 + k * 0.2), (ax + 0.5 - k * 0.1, 2, h + 2.0 + k * 0.2), 0.02, "metal_dark")
    p.cable((-3.5, 2, h + 2.4), (4.4, 2, h + 2.4), 0.8)
    for f in range(1, floors):
        p.box((w + 0.02, 0.05, 0.07), (0, -d / 2 - 0.01, f * fh + 0.3), "concrete_dark")
        p.box((w + 0.02, 0.05, 0.07), (0, d / 2 + 0.01, f * fh + 0.3), "concrete_dark")
    for xx in (-w / 2 + 3, 0, w / 2 - 3):
        p.box((0.05, 0.03, h - 0.6), (xx, -d / 2 - 0.01, h / 2 + 0.3), "concrete_dark")
    for f in range(floors):
        z = f * fh + 1.0 + 0.6
        for i in range(4):
            x = -w / 2 + 1.5 + i * 3.0
            lit = (f * 7 + i * 3) % 5 not in (0, 3)
            cur = ("l", "r", None)[(f + i) % 3]
            if i == 1 and f > 0:  # балкон-лоджия вместо окна
                p.box_floor((2.4, 1.1, 0.12), (x, -d / 2 - 0.55, z - 1.05), "concrete")
                p.box_floor((2.4, 0.08, 0.95), (x, -d / 2 - 1.06, z - 0.93), "concrete")
                p.box((2.4, 0.1, 0.05), (x, -d / 2 - 1.06, z + 0.04), "metal_dark")
                p.box((0.8, 0.05, 2.0), (x - 0.55, -d / 2 - 0.02, z - 0.05),
                      "window_lit" if lit else "window_dark")
                p.box((0.7, 0.06, 1.0), (x + 0.5, -d / 2 - 0.02, z + 0.1), "window_lit" if lit else "window_dark")
                if (f + i) % 2:  # бельё и хлам на балконах
                    p.beam((x - 1.1, -d / 2 - 0.9, z + 0.8), (x + 1.1, -d / 2 - 0.9, z + 0.8), 0.01, "black")
                    p.poly_prism(SHIRT, 0.02, (x + 0.4, -d / 2 - 0.9, z + 0.2), "cloth_white", rot=(90, 0, 0))
                else:
                    p.box_floor((0.5, 0.4, 0.5), (x + 0.8, -d / 2 - 0.4, z - 0.93), "wood_old")
            else:
                _window_unit(p, x, -d / 2, z, lit, -1, curtain=cur)
            if i == 2 and (f % 3) == 1:  # кондиционер
                p.box((0.8, 0.3, 0.55), (x + 0.2, -d / 2 - 0.2, z - 1.1), "enamel", bevel=0.02)
                p.box((0.5, 0.02, 0.4), (x + 0.2, -d / 2 - 0.36, z - 1.1), "metal_dark")
            _window_unit(p, x, d / 2, z, not lit, 1, curtain=None)
    # лестничный витраж: вертикальная лента окон над подъездом
    for f in range(floors - 1):
        p.box((0.9, 0.06, 1.0), (-w / 2 + 6, -d / 2 - 0.02, f * fh + 2.6 + 0.6), "window_lit")
    # водостоки
    for xx in (-w / 2 + 0.15, w / 2 - 0.15):
        p.pipe_run((xx, -d / 2 - 0.12, 0.2), (xx, -d / 2 - 0.12, h + 0.2), 0.06, "metal")
        p.box((0.2, 0.2, 0.25), (xx, -d / 2 - 0.12, h + 0.1), "metal")
    p.text("12", (-w / 2 + 0.6, -d / 2 - 0.03, 2.2), 0.4, "whitewash", depth=0.02)
    p.collider((w, d, h + 0.45), (0, 0, (h + 0.45) / 2))
    return p


def panel_entrance():
    """Подъезд: козырёк, металлическая дверь с домофоном, ступени, перила, урна, лампа."""
    p = Prop("panel_entrance")
    for i in range(2):  # две ступени к площадке
        p.box_floor((2.4, 0.32, 0.16 * (i + 1)), (0, -1.2 - 0.32 * (2 - i) + 0.16, 0), "concrete", bevel=0.01)
    p.box_floor((2.6, 1.2, 0.48), (0, -0.6, 0), "concrete")
    p.box_floor((1.3, 0.1, 2.2), (0, -0.05, 0.48), "concrete_dark")  # проём
    p.box_floor((1.1, 0.08, 2.05), (0, -0.1, 0.48), "paint_blue", bevel=0.01)
    p.box((0.9, 0.02, 0.05), (0, -0.145, 1.0), "metal")
    p.box((0.04, 0.05, 0.3), (0.42, -0.16, 1.5), "metal")
    p.box((0.14, 0.04, 0.22), (0.72, -0.14, 1.55), "metal_dark", bevel=0.005)  # домофон
    for k in range(3):
        for j in range(3):
            p.box((0.025, 0.01, 0.025), (0.68 + j * 0.04, -0.165, 1.5 + k * 0.04), "metal")
    p.box((0.05, 0.01, 0.03), (0.72, -0.165, 1.63), "led_red")
    p.box((3.0, 2.0, 0.14), (0, -1.0, 3.0), "concrete_dark", bevel=0.02)
    p.box((3.0, 0.1, 0.3), (0, -2.0, 2.92), "concrete_dark")
    for x in (-1.35, 1.35):
        p.box_floor((0.12, 0.12, 2.93), (x, -1.85, 0), "metal_dark")
    for x in (-1.25, 1.25):  # перила
        p.beam((x, -2.4, 0.9), (x, -1.3, 1.4), 0.05, "metal_dark", segs=6)
        p.beam((x, -2.4, 0), (x, -2.4, 0.9), 0.05, "metal_dark", segs=6)
    p.box((0.32, 0.12, 0.18), (0, -0.15, 2.82), "metal_dark")
    p.box((0.26, 0.04, 0.12), (0, -0.22, 2.8), "lamp_glow")
    p.cable((0, -0.1, 2.9), (1.3, -0.1, 3.2), 0.1)
    p.tube(0.2, 0.18, 0.6, (1.7, -1.2, 0), "concrete")  # урна
    p.box((0.4, 0.01, 0.25), (-0.75, -0.11, 1.4), "paper")  # объявления
    p.box((0.25, 0.01, 0.3), (-0.75, -0.11, 1.05), "paper_old", rot=(0, 6, 0))
    p.text("ПОДЪЕЗД 3", (0, -0.13, 2.65), 0.11, "whitewash", depth=0.01)
    p.collider((2.6, 1.2, 0.48), (0, -0.6, 0.24)).collider((3.0, 2.0, 0.3), (0, -1.0, 3.0))
    return p


def _chair_geom(p, x, y, rot, m_seat="wood", m_frame="wood_dark"):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))

    def T(lx, ly):
        return (x + lx * c - ly * s, y + lx * s + ly * c)
    p.box((0.44, 0.42, 0.04), (*T(0, 0), 0.45), m_seat, rot=(0, 0, rot), bevel=0.01)
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.box_floor((0.04, 0.04, 0.43), (*T(sx * 0.19, sy * 0.18), 0), m_frame, rot=(0, 0, rot))
        p.box_floor((0.04, 0.04, 0.5), (*T(sx * 0.19, 0.18), 0.47), m_frame, rot=(0, 0, rot))
    p.box((0.36, 0.02, 0.02), (*T(0, -0.18), 0.2), m_frame, rot=(0, 0, rot))
    p.box((0.42, 0.03, 0.14), (*T(0, 0.18), 0.88), m_seat, rot=(0, 0, rot), bevel=0.01)
    p.box((0.42, 0.03, 0.04), (*T(0, 0.18), 0.68), m_frame, rot=(0, 0, rot))


def _place_setting(p, x, y, H, k, toward):
    """Сервировка: тарелка с едой, миска риса, палочки/вилка, стакан."""
    p.cyl(0.13, 0.015, (x, y, H), "porcelain", segs=12)
    p.cyl(0.115, 0.01, (x, y, H + 0.015), "porcelain", segs=12, r2=0.13)
    food = ("food", "greens", "meat")[k % 3]
    p.blob(0.06, (x, y, H + 0.04), food, scale=(1.2, 1.0, 0.45), jitter=0.3)
    bx, by = x + 0.2, y + toward * 0.05
    p.tube(0.065, 0.058, 0.06, (bx, by, H), "porcelain")
    p.cyl(0.06, 0.005, (bx, by, H + 0.05), "rice" if k % 2 else "soup", segs=10)
    p.box((0.22, 0.008, 0.008), (x - 0.18, y - toward * 0.02, H + 0.006), "wood_light", rot=(0, 0, 80))
    p.box((0.22, 0.008, 0.008), (x - 0.16, y - toward * 0.02, H + 0.006), "wood_light", rot=(0, 0, 84))
    p.tube(0.035, 0.03, 0.1, (x + 0.05, y + toward * 0.2, H), "glass_green", segs=8)


def dinner_table_10():
    """Ужин (р-н 01): стол на десятерых, горячая еда на всех местах, стулья. Десятое место — торец у зрителя."""
    p = Prop("dinner_table_10")
    L, W, H = 4.0, 1.1, 0.75
    p.box((L, W, 0.05), (0, 0, H - 0.025), "wood", bevel=0.015)
    p.box((L - 0.2, W - 0.2, 0.08), (0, 0, H - 0.09), "wood_dark")  # царга
    p.box((L + 0.08, W + 0.08, 0.008), (0, 0, H + 0.004), "tablecloth")
    for sy in (-1, 1):  # свисающий край скатерти
        p.box((L + 0.08, 0.008, 0.18), (0, sy * (W / 2 + 0.04), H - 0.085), "tablecloth")
    for sx in (-1, 1):
        p.box((0.008, W + 0.08, 0.18), (sx * (L / 2 + 0.04), 0, H - 0.085), "tablecloth")
        for sy in (-1, 1):
            p.box_floor((0.07, 0.07, H - 0.05), (sx * (L / 2 - 0.15), sy * (W / 2 - 0.12), 0), "wood_dark", bevel=0.01)
    Ht = H + 0.008
    k = 0
    for i in range(4):
        for s in (-1, 1):
            x, y = -1.5 + i * 1.0, s * 0.33
            _place_setting(p, x, y, Ht, k, s)
            _chair_geom(p, x, s * 0.85, 0 if s > 0 else 180)
            k += 1
    _place_setting(p, L / 2 - 0.3, 0, Ht, k, 1)
    _chair_geom(p, L / 2 + 0.45, 0, -90)
    _place_setting(p, -L / 2 + 0.3, 0, Ht, k + 1, -1)  # пустое кресло у зрителя — стула нет
    # общие блюда в центре
    for x in (-0.9, 0.5):
        p.tube(0.2, 0.18, 0.1, (x, 0, Ht), "enamel", segs=12)
        p.cyl(0.18, 0.01, (x, 0, Ht + 0.08), "soup", segs=12)
        for j in range(4):
            p.blob(0.04, (x + 0.08 * math.cos(j * 1.6), 0.08 * math.sin(j * 1.6), Ht + 0.095), "meat", jitter=0.3)
    p.cyl(0.08, 0.2, (-0.2, 0.05, Ht), "metal", segs=8, r2=0.06)  # чайник
    p.beam((-0.12, 0.05, Ht + 0.12), (-0.02, 0.05, Ht + 0.2), 0.02, "metal", segs=5)
    p.cyl(0.03, 0.06, (-0.2, 0.05, Ht + 0.2), "black", segs=6)
    for x in (1.2, -1.4):  # бутылки
        p.cyl(0.04, 0.22, (x, 0.02, Ht), "glass_green", segs=8)
        p.cyl(0.015, 0.08, (x, 0.02, Ht + 0.22), "glass_green", segs=6)
    p.collider((L, W, H), (0, 0, H / 2))
    return p


def chair_wooden():
    p = Prop("chair_wooden")
    _chair_geom(p, 0, 0, 0)
    return p.collider((0.44, 0.42, 0.97), (0, 0, 0.485))


def pendant_lamp_red():
    """Абажур над столом. Опора — крепление к потолку (Z=0, висит вниз)."""
    p = Prop("pendant_lamp_red")
    p.cyl(0.06, 0.04, (0, 0, -0.04), "porcelain", segs=8)
    p.curve_tube([(0, 0, -0.04), (0.02, 0, -0.5), (-0.01, 0, -1.0)], 0.01, "black")
    p.cyl(0.03, 0.08, (0, 0, -1.08), "metal_dark", segs=6)
    p.cyl(0.38, 0.06, (0, 0, -1.28), "lamp_red", segs=12, r2=0.36)
    p.cyl(0.36, 0.14, (0, 0, -1.22), "lamp_red", segs=12, r2=0.14)
    p.cyl(0.1, 0.06, (0, 0, -1.2), "lamp_glow", segs=8)
    for i in range(24):  # бахрома
        a = i * math.tau / 24
        p.box((0.012, 0.012, 0.08), (0.375 * math.cos(a), 0.375 * math.sin(a), -1.32), "paint_yellow")
    return p


def plate_food():
    p = Prop("plate_food")
    p.cyl(0.13, 0.015, (0, 0, 0), "porcelain", segs=12)
    p.cyl(0.115, 0.01, (0, 0, 0.015), "porcelain", segs=12, r2=0.13)
    p.blob(0.06, (0.0, 0.01, 0.04), "food", scale=(1.3, 1.0, 0.45), jitter=0.3)
    p.blob(0.035, (-0.05, -0.04, 0.035), "greens", scale=(1, 1, 0.5), jitter=0.3)
    return p


def radio_vintage():
    """Радио (р-н 03): ламповый приёмник «Рига»: решётка, шкала, ручки, ножки, антенна."""
    p = Prop("radio_vintage")
    p.box_floor((0.58, 0.24, 0.3), (0, 0, 0.03), "wood", bevel=0.02)
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.cyl(0.015, 0.03, (sx * 0.25, sy * 0.08, 0), "black", segs=6)
    p.box((0.28, 0.02, 0.22), (-0.12, -0.115, 0.18), "cloth_gray")
    for i in range(6):
        p.box((0.27, 0.012, 0.012), (-0.12, -0.13, 0.08 + i * 0.038), "wood_light")
    p.box((0.2, 0.02, 0.09), (0.16, -0.115, 0.24), "radio_screen")
    for i in range(7):
        p.box((0.003, 0.022, 0.025), (0.08 + i * 0.026, -0.12, 0.26), "black")
    p.text("МОСКВА  РИГА  КИЕВ", (0.16, -0.127, 0.215), 0.008, "black", depth=0.002)
    p.box((0.004, 0.025, 0.08), (0.18, -0.127, 0.24), "led_red")
    for x in (0.09, 0.16, 0.23):
        p.cyl(0.022, 0.03, (x, -0.11, 0.1), "black", segs=8, rot=(90, 0, 0))
        p.box((0.004, 0.012, 0.018), (x, -0.142, 0.11), "whitewash")
    for i in range(4):  # клавиши диапазонов
        p.box((0.03, 0.03, 0.02), (0.07 + i * 0.04, -0.06, 0.335), "porcelain", bevel=0.003)
    p.beam((0.26, 0.1, 0.33), (0.4, 0.13, 0.75), 0.006, "metal", segs=4)
    p.cable((-0.25, 0.12, 0.08), (-0.45, 0.25, 0.0), 0.02)
    return p.collider_auto()


def tear_calendar():
    """Отрывной календарь «МАРТ 23 / ЗАВТРА» с пачкой листов и гвоздём."""
    p = Prop("tear_calendar")
    p.box((0.18, 0.025, 0.06), (0, 0, 0.225), "calendar_red", bevel=0.004)
    p.cyl(0.006, 0.03, (0, 0.0, 0.245), "metal", segs=6, rot=(90, 0, 0))
    p.box((0.16, 0.03, 0.19), (0, 0.003, 0.1), "paper")
    for i in range(4):  # торцы листов
        p.box((0.162, 0.004, 0.002), (0, -0.0, 0.006 + i * 0.002), "paper_old")
    p.box((0.16, 0.002, 0.03), (0.0, -0.016, 0.205), "paper_old", rot=(25, 0, 0))  # оборванный край
    p.text("МАРТ", (0, -0.014, 0.225), 0.03, "paper", depth=0.003)
    p.text("23", (0, -0.016, 0.115), 0.09, "black", depth=0.003)
    p.text("ПЯТНИЦА", (0, -0.016, 0.055), 0.014, "calendar_red", depth=0.002)
    p.text("ЗАВТРА", (0, -0.016, 0.028), 0.018, "black", depth=0.003)
    return p


def clothesline():
    """Стирка (р-н 04): Т-образные столбы, две провисающие верёвки, прищепки, бельё, таз. Модуль 8 м."""
    p = Prop("clothesline")
    for x in (-4, 4):
        p.cyl(0.05, 2.4, (x, 0, 0), "metal_dark", segs=6)
        p.cyl(0.12, 0.1, (x, 0, 0), "concrete", segs=8)
        p.beam((x, -0.35, 2.3), (x, 0.35, 2.3), 0.05, "metal_dark", segs=6)
        for y in (-0.28, 0.28):
            p.beam((x, y, 2.32), (x, y, 2.2), 0.015, "metal")
    for y in (-0.28, 0.28):
        p.curve_tube(p.sag((-4, y, 2.25), (4, y, 2.25), 0.25, 16), 0.01, "cloth_white")

    def line_z(x):
        return 2.25 - 0.25 * (1 - (x / 4) ** 2)
    items = [(-2.8, -0.28, SHIRT, "cloth_white", 0.6), (-1.6, 0.28, PANTS, "cloth_blue", 0.75),
             (-0.4, -0.28, None, "cloth_check", 0.9), (0.9, 0.28, DRESS, "cloth_white", 0.85),
             (2.2, -0.28, PANTS, "cloth_gray", 0.75), (3.0, 0.28, SHIRT, "cloth_blue", 0.6)]
    for x, y, shape, m, hgt in items:
        z = line_z(x)
        if shape is None:
            p.box((1.0, 0.015, hgt), (x, y, z - hgt / 2), m, rot=(0, 0, 3))  # простыня
            pins = (x - 0.45, x, x + 0.45)
        else:
            p.poly_prism(shape, 0.02, (x, y, z - hgt), m)
            pins = (x - 0.2, x + 0.2)
        for px in pins:
            p.box((0.015, 0.03, 0.06), (px, y, line_z(px)), "wood_light")
    # таз с бельём
    p.tube(0.32, 0.29, 0.18, (1.5, -1.0, 0), "enamel", segs=12)
    p.blob(0.22, (1.5, -1.0, 0.16), "cloth_white", scale=(1, 1, 0.4), jitter=0.3)
    p.collider((0.15, 0.7, 2.4), (-4, 0, 1.2)).collider((0.15, 0.7, 2.4), (4, 0, 1.2))
    return p


def clothes_single():
    """Отдельная рубашка — тот самый «по размеру смотрящего» предмет, с воротником и пуговицами."""
    p = Prop("clothes_shirt")
    p.poly_prism(SHIRT, 0.02, (0, 0, 0), "cloth_white")
    p.poly_prism([(-0.1, 0), (0, -0.08), (0.1, 0), (0.12, 0.04), (-0.12, 0.04)], 0.025, (0, 0, 0.56), "cloth_white")
    for i in range(5):
        p.cyl(0.008, 0.005, (0, -0.013, 0.08 + i * 0.1), "porcelain", segs=6, rot=(90, 0, 0))
    p.box((0.12, 0.004, 0.1), (0.15, -0.012, 0.42), "cloth_gray")  # карман
    return p


def window_frame():
    """Окно-«зеркало» (р-н 05): двойная деревянная рама, форточка, подоконник, отлив, шпингалеты."""
    p = Prop("window_frame")
    W, H = 1.2, 1.4
    p.box((W + 0.2, 0.18, 0.08), (0, 0, H + 0.04), "wood_light", bevel=0.01)
    p.box((W + 0.2, 0.18, 0.08), (0, 0, -0.04), "wood_light", bevel=0.01)
    for x in (-W / 2 - 0.06, W / 2 + 0.06):
        p.box((0.08, 0.18, H + 0.16), (x, 0, H / 2), "wood_light", bevel=0.01)
    for yy in (-0.05, 0.05):  # две рамы
        for x in (-W / 2 + 0.03, 0, W / 2 - 0.03):
            p.box((0.05, 0.04, H), (x, yy, H / 2), "wood_light")
        for z in (0.02, H * 0.72, H - 0.02):
            p.box((W, 0.04, 0.05), (0, yy, z), "wood_light")
    p.box((W - 0.06, 0.01, H - 0.06), (0, -0.05, H / 2), "window_dark")
    p.box((W - 0.06, 0.01, H - 0.06), (0, 0.05, H / 2), "window_dark")
    for x in (-0.04, 0.04):
        p.box((0.015, 0.02, 0.08), (x, -0.08, H * 0.4), "metal")
    p.box((W + 0.35, 0.32, 0.04), (0, -0.16, -0.1), "whitewash", bevel=0.01)
    p.tube(0.06, 0.05, 0.1, (0.35, -0.2, -0.08), "brick_roof", segs=8)  # горшок с цветком
    p.blob(0.08, (0.35, -0.2, 0.08), "foliage", jitter=0.35)
    return p


def street_lamp_sodium():
    """Тень (р-н 06): уличный фонарь с натриевой лампой, ревизионным лючком, проводом и объявлениями."""
    p = Prop("street_lamp_sodium")
    p.cyl(0.18, 0.35, (0, 0, 0), "concrete", segs=8, r2=0.14)
    p.cyl(0.08, 5.6, (0, 0, 0.35), "concrete", segs=8, r2=0.05)
    p.box((0.06, 0.01, 0.18), (0, -0.075, 1.0), "metal_dark")
    p.box((0.13, 0.005, 0.18), (0.0, -0.07, 1.6), "paper", rot=(0, 3, 0))
    p.box((0.12, 0.005, 0.15), (0.0, -0.068, 1.35), "paper_old", rot=(0, -4, 0))
    p.curve_tube([(0, 0, 5.85), (0.4, 0, 6.05), (1.0, 0, 6.1)], 0.07, "metal_dark", segs=6)
    p.box((0.6, 0.28, 0.12), (1.25, 0, 6.08), "metal_dark", bevel=0.02)
    p.box((0.5, 0.2, 0.06), (1.25, 0, 6.0), "sodium", bevel=0.01)
    p.cable((0.05, 0, 5.8), (-3.0, 0, 6.0), 0.4)
    p.cable((0.05, 0, 5.8), (3.0, 0.2, 5.9), 0.35)
    return p.collider((0.36, 0.36, 6.0), (0, 0, 3.0))


def apartment_door():
    """Гости (р-н 07): обитая дерматином квартирная дверь, приоткрыта на 60°, глазок, номер, звонок, коврик."""
    p = Prop("apartment_door")
    p.box((0.1, 0.18, 2.12), (-0.5, 0, 1.06), "wood_dark", bevel=0.01)
    p.box((0.1, 0.18, 2.12), (0.5, 0, 1.06), "wood_dark", bevel=0.01)
    p.box((1.1, 0.18, 0.1), (0, 0, 2.17), "wood_dark", bevel=0.01)
    a = -60
    ra = math.radians(a)

    def D(lx, ly, lz):
        return (-0.45 + lx * math.cos(ra) - ly * math.sin(ra), lx * math.sin(ra) + ly * math.cos(ra), lz)
    p.box((0.9, 0.06, 2.05), D(0.45, 0, 1.03), "velvet", rot=(0, 0, a), bevel=0.01)
    for i in range(4):  # стёжка дерматина
        for j in range(8):
            p.cyl(0.012, 0.01, D(0.15 + i * 0.2, -0.035, 0.2 + j * 0.24), "gold", segs=6, rot=(90, 0, a))
    p.text("47", D(0.45, -0.035, 1.75), 0.08, "gold", depth=0.01, rot=(90, 0, a))
    p.cyl(0.012, 0.02, D(0.45, -0.035, 1.55), "metal", segs=6, rot=(90, 0, a))  # глазок
    p.box((0.04, 0.05, 0.14), D(0.8, -0.04, 1.0), "gold", rot=(0, 0, a))
    p.box((0.12, 0.03, 0.02), D(0.76, -0.07, 1.04), "gold", rot=(0, 0, a))
    p.box((0.05, 0.03, 0.07), (0.65, -0.1, 1.5), "porcelain", bevel=0.005)  # звонок
    p.box((0.9, 0.55, 0.015), (0.1, -0.5, 0.008), "cloth_check")  # коврик
    p.box((0.5, 0.3, 0.008), (0, 0.6, 0.004), "black")  # тьма прихожей
    p.collider((1.1, 0.18, 2.22), (0, 0, 1.11))
    return p


def photo_frame_wall():
    """Улыбка (р-н 09) / Фотографии (р-н 18): рамка с профилем, паспарту, стекло; фото — под свою текстуру."""
    p = Prop("photo_frame")
    p.box((0.42, 0.03, 0.52), (0, 0, 0.26), "wood_dark", bevel=0.008)
    p.box((0.34, 0.033, 0.44), (0, -0.001, 0.26), "paper")
    p.box((0.24, 0.035, 0.32), (0, -0.002, 0.27), "porcelain")  # место для фото
    p.cable((-0.1, 0.02, 0.5), (0.1, 0.02, 0.5), -0.06, "black", 0.004)
    return p


def photo_frame_large():
    p = Prop("photo_frame_large")
    p.box((1.6, 0.05, 1.1), (0, 0, 0.55), "wood_dark", bevel=0.015)
    p.box((1.48, 0.052, 0.98), (0, -0.001, 0.55), "gold")
    p.box((1.4, 0.055, 0.9), (0, -0.002, 0.55), "porcelain")
    return p


def fridge_open():
    """Кухня (р-н 10): советский холодильник «ЗИЛ»: скруглённый корпус, морозилка, мясо на полках, дверь с полками."""
    p = Prop("fridge_open")
    W, D, H = 0.62, 0.62, 1.6
    p.box_floor((W, 0.04, H), (0, D / 2 - 0.02, 0.06), "enamel", bevel=0.03)
    for x in (-W / 2 + 0.02, W / 2 - 0.02):
        p.box_floor((0.04, D, H), (x, 0, 0.06), "enamel", bevel=0.02)
    p.box_floor((W, D, 0.06), (0, 0, 0.06), "enamel")
    p.box_floor((W, D, 0.1), (0, 0, H - 0.04), "enamel", bevel=0.04)
    p.box_floor((W - 0.04, D - 0.06, 0.06), (0, 0, 0), "metal_dark")  # цоколь
    p.box((W - 0.08, D - 0.08, 0.2), (0, 0.02, H - 0.2), "metal")   # морозилка
    p.box((W - 0.1, 0.01, 0.16), (0, -0.25, H - 0.2), "tile_white")
    p.box((W - 0.12, D - 0.12, 0.01), (0, 0.02, H - 0.31), "lamp_glow")
    for z in (0.45, 0.8, 1.12):
        for k in range(6):
            p.box((0.008, D - 0.08, 0.008), (-W / 2 + 0.06 + k * 0.1, 0.02, z), "metal")
        p.box((W - 0.06, 0.01, 0.01), (0, -D / 2 + 0.06, z), "metal")
    for z, x in ((0.47, -0.1), (0.82, 0.12), (1.14, -0.08), (0.82, -0.13)):
        p.blob(0.11, (x, 0.05, z + 0.05), "meat", scale=(1.3, 1.0, 0.55), jitter=0.25)
    p.tube(0.08, 0.075, 0.1, (0.12, 0.08, 0.465), "enamel")  # кастрюля
    p.box((0.2, 0.25, 0.08), (0.12, 0.05, 1.17), "paper_old")  # свёрток
    p.box_floor((0.46, 0.18, 0.12), (0, 0.02, 0.12), "cloth_white")  # ящик для овощей
    # дверь открыта на 100°
    hx, hy = W / 2, -D / 2
    a = math.radians(100)

    door_c = (hx + 0.03, hy - W / 2, H / 2 + 0.06)
    p.box((0.07, W, H - 0.02), door_c, "enamel", rot=(0, 0, 0), bevel=0.03)
    for z in (0.5, 0.9, 1.25):
        p.box((0.12, W - 0.1, 0.02), (hx - 0.05, hy - W / 2, z), "enamel")
        p.box((0.02, W - 0.1, 0.06), (hx - 0.1, hy - W / 2, z + 0.03), "enamel")
    for k in range(3):
        p.cyl(0.03, 0.2, (hx - 0.06, hy - 0.15 - k * 0.12, 0.52), "glass_green", segs=6)
    p.box((0.03, 0.05, 0.25), (hx + 0.08, hy - W + 0.06, 1.05), "metal")
    p.text("ЗИЛ", (hx + 0.07, hy - W / 2, H - 0.05), 0.06, "metal", depth=0.006, rot=(90, 0, 90))
    p.collider((W, D, H + 0.06), (0, 0, (H + 0.06) / 2))
    return p


def meat_chunk():
    """Кусок «свинины» — подбираемый ресурс (р-н 10), с жиром, костью и бумагой."""
    p = Prop("meat_chunk")
    p.box((0.32, 0.26, 0.004), (0, 0, 0.002), "paper_old", rot=(0, 0, 12))
    p.blob(0.12, (0, 0, 0.05), "meat", scale=(1.3, 0.9, 0.5), jitter=0.22)
    p.blob(0.05, (0.08, 0.03, 0.08), "porcelain", scale=(1.2, 0.8, 0.5), jitter=0.2)
    p.cyl(0.018, 0.12, (-0.1, -0.02, 0.05), "porcelain", segs=6, rot=(0, -90, 0))
    p.sphere(0.026, (-0.22, -0.02, 0.05), "porcelain", segs=6, rings=4)
    return p


def wall_clock():
    """Часы (р-н 13): круглые настенные с ободом, цифрами, маятником под ними."""
    p = Prop("wall_clock")
    p.cyl(0.19, 0.05, (0, 0.02, 0), "wood", segs=16, rot=(90, 0, 0))
    p.cyl(0.165, 0.052, (0, 0.021, 0), "porcelain", segs=16, rot=(90, 0, 0))
    for h in range(12):
        a = math.radians(h * 30)
        if h % 3 == 0:
            p.text(str(12 if h == 0 else h), (0.125 * math.sin(a), -0.034, 0.125 * math.cos(a)), 0.035, "black", depth=0.003)
        else:
            p.box((0.008, 0.004, 0.02), (0.135 * math.sin(a), -0.034, 0.135 * math.cos(a)), "black", rot=(0, h * 30, 0))
    p.box((0.012, 0.006, 0.12), (0, -0.04, 0.05), "black")
    p.box((0.09, 0.006, 0.014), (0.04, -0.042, 0.0), "black")
    p.box((0.003, 0.004, 0.13), (-0.03, -0.044, -0.04), "calendar_red", rot=(0, 40, 0))
    p.cyl(0.01, 0.01, (0, -0.046, 0), "black", segs=6, rot=(90, 0, 0))
    return p


def alarm_clock_digital():
    p = Prop("alarm_clock_digital")
    p.box_floor((0.19, 0.09, 0.085), (0, 0, 0.01), "plastic_red", bevel=0.012)
    p.box((0.15, 0.005, 0.05), (0, -0.046, 0.055), "black")
    p.text("04:17", (0, -0.05, 0.055), 0.04, "led_red", depth=0.004)
    for x in (-0.08, 0.08):
        p.box_floor((0.02, 0.07, 0.01), (x, 0, 0), "black")
    p.box((0.05, 0.02, 0.012), (0.04, 0, 0.1), "black", bevel=0.003)
    p.cable((0.0, 0.045, 0.02), (0.1, 0.25, 0.0), 0.01)
    return p


def mailbox_block():
    """Почта (р-н 14): блок почтовых ящиков 6×4 с номерами, замками, торчащими газетами. Опора — низ, задняя грань Y=0."""
    p = Prop("mailbox_block")
    cols, rows, cw, ch = 6, 4, 0.32, 0.26
    W, H = cols * cw, rows * ch
    p.box_floor((W + 0.06, 0.22, H + 0.06), (0, -0.11, 0), "paint_army", bevel=0.01)
    n = 1
    for r in reversed(range(rows)):
        for c in range(cols):
            x = -W / 2 + cw / 2 + c * cw
            z = 0.03 + ch / 2 + r * ch
            p.box((cw - 0.03, 0.02, ch - 0.03), (x, -0.225, z), "mailbox_green", bevel=0.004)
            p.box((cw * 0.6, 0.02, 0.02), (x - 0.02, -0.236, z + 0.075), "black")
            for k in range(3):
                p.cyl(0.006, 0.01, (x - 0.08 + k * 0.03, -0.238, z), "black", segs=5, rot=(90, 0, 0))
            p.cyl(0.012, 0.012, (x + cw * 0.36, -0.238, z - 0.02), "metal", segs=6, rot=(90, 0, 0))
            p.text(str(n), (x - 0.08, -0.238, z - 0.07), 0.03, "whitewash", depth=0.002)
            if n in (3, 10, 17, 22):  # газеты и письма торчат
                p.box((0.16, 0.06, 0.01), (x - 0.02, -0.26, z + 0.08), "paper", rot=(10, 0, 4))
            n += 1
    p.text("ПОЧТА", (0, -0.236, H + 0.12), 0.07, "paint_army", depth=0.01)
    p.box((0.4, 0.01, 0.1), (0, -0.224, H + 0.12), "paper")
    p.collider((W + 0.06, 0.22, H + 0.06), (0, -0.11, (H + 0.06) / 2))
    return p


def envelope():
    """Письмо «Лично. Тебе.» без марки — клапан, надпись."""
    p = Prop("envelope")
    p.box((0.22, 0.11, 0.004), (0, 0, 0.002), "paper_old")
    p.poly_prism([(-0.11, 0.055), (0.11, 0.055), (0, -0.01)], 0.001, (0, 0, 0.0045), "paper", rot=(0, 0, 0))
    p.text("Лично. Тебе.", (-0.02, -0.03, 0.0055), 0.014, "black", depth=0.001, rot=(0, 0, 0))
    p.box((0.03, 0.035, 0.001), (0.085, -0.03, 0.0045), "paper")  # пустое место для марки
    return p


def lullaby_window_block():
    """Колыбельная (р-н 16): тёмный 3-этажный блок с единственным светящимся окном (люстра и кроватка за стеклом)."""
    p = Prop("lullaby_window_block")
    p.box_floor((9, 6, 0.5), (0, 0, 0), "concrete_dark")
    p.box_floor((9, 6, 8.5), (0, 0, 0.5), "panel_wall")
    p.box_floor((9.3, 6.3, 0.35), (0, 0, 9), "concrete_dark")
    for f in range(3):
        for i in range(3):
            lit = (f, i) == (1, 1)
            x, z = -3 + i * 3, 2.0 + f * 3
            _window_unit(p, x, -3, z, lit, -1, w=1.3, h=1.5, curtain="l" if lit else None)
    # за светящимся окном — комната: стены, кроватка, люстра
    p.box_floor((1.4, 1.2, 1.7), (0, -2.4, 4.25), "wallpaper")
    p.box_floor((0.7, 0.4, 0.5), (0.1, -2.15, 4.3), "wood_light")
    for k in range(6):
        p.box((0.02, 0.02, 0.4), (-0.2 + k * 0.12, -2.36, 4.75), "wood_light")
    p.cyl(0.15, 0.1, (0, -2.4, 5.6), "lamp_glow", segs=8, r2=0.05)
    p.pipe_run((4.3, -3.12, 0.3), (4.3, -3.12, 9.2), 0.06, "metal")
    p.box((0.8, 0.05, 0.8), (-4.0, -3.03, 1.8), "rust")  # щиток
    p.collider((9, 6, 9), (0, 0, 4.5))
    return p


def interior_door_ajar():
    """Дверь (р-н 21): филёнчатая дверь со стеклом, приоткрыта щелью; за ней — чёрный объём, который не пробивает фонарь."""
    p = Prop("interior_door_ajar")
    p.box((1.2, 0.2, 0.1), (0, 0, 2.15), "wood_dark", bevel=0.01)
    for x in (-0.55, 0.55):
        p.box((0.1, 0.2, 2.2), (x, 0, 1.1), "wood_dark", bevel=0.01)
    p.box((1.3, 0.03, 0.12), (0, -0.11, 2.2), "wood_light")  # наличник
    for x in (-0.62, 0.62):
        p.box((0.08, 0.03, 2.25), (x, -0.11, 1.12), "wood_light")
    rot = -10
    p.box((0.9, 0.04, 2.05), (-0.05, 0.02, 1.03), "wood_light", rot=(0, 0, rot), bevel=0.008)
    p.box((0.6, 0.05, 0.75), (-0.05, 0.02, 0.5), "wood", rot=(0, 0, rot), bevel=0.02)
    p.box((0.6, 0.045, 0.75), (-0.05, 0.02, 1.5), "window_dark", rot=(0, 0, rot))
    for z in (1.25, 1.5, 1.75):
        p.box((0.62, 0.05, 0.02), (-0.05, 0.02, z), "wood", rot=(0, 0, rot))
    p.box((0.13, 0.03, 0.025), (0.3, -0.06, 1.0), "gold", rot=(0, 0, rot))
    p.box((0.04, 0.02, 0.12), (0.33, -0.04, 1.0), "gold", rot=(0, 0, rot))
    for z in (0.3, 1.8):
        p.box((0.02, 0.03, 0.1), (-0.5, 0.02, z), "metal")
    p.box((1.0, 0.02, 2.1), (0, 0.15, 1.05), "black")
    p.box((1.0, 0.6, 0.01), (0, 0.4, 0.005), "black")
    p.collider((1.2, 0.2, 2.2), (0, 0, 1.1))
    return p


def walkie_talkie():
    """Голоса в рации (р-н 24): армейская рация с антенной, клипсой, ручками и решёткой динамика."""
    p = Prop("walkie_talkie")
    p.box_floor((0.072, 0.038, 0.19), (0, 0, 0), "paint_army", bevel=0.008)
    p.box_floor((0.066, 0.04, 0.05), (0, 0, 0), "black", bevel=0.005)  # аккумулятор
    p.cyl(0.007, 0.16, (0.022, 0, 0.19), "black", segs=6, r2=0.004)
    p.cyl(0.01, 0.025, (0.022, 0, 0.19), "black", segs=6)
    p.cyl(0.009, 0.018, (-0.02, 0, 0.19), "black", segs=8)
    p.box((0.056, 0.005, 0.04), (0, -0.02, 0.15), "screen_green")
    p.sphere(0.005, (0.025, -0.012, 0.188), "led_red", segs=6, rings=3)
    for i in range(6):
        p.box((0.05, 0.004, 0.004), (0, -0.02, 0.065 + i * 0.011), "black")
    p.box((0.012, 0.01, 0.04), (-0.04, 0, 0.12), "black")  # тангента
    p.box((0.04, 0.01, 0.08), (0, 0.022, 0.12), "metal_dark")
    return p


def ceiling_stain():
    """Потолок (р-н 25): тёмное пятно с разводами и каплями. Крепится к потолку (Z=0, вниз)."""
    p = Prop("ceiling_stain")
    for i, (r, dx, dy) in enumerate(((0.55, 0, 0), (0.35, 0.3, 0.2), (0.25, -0.35, -0.1), (0.18, 0.1, -0.4))):
        p.cyl(r, 0.004, (dx, dy, -0.004 - i * 0.001), "crimson" if i else "sinew_old", segs=10, jitter=r * 0.12)
    for x, y, L in ((0.1, 0.05, 0.15), (0.3, 0.2, 0.08), (-0.2, -0.05, 0.11)):
        p.cyl(0.025, L, (x, y, -L), "crimson", segs=6, r2=0.0, rot=(180, 0, 0))
        p.sphere(0.02, (x, y, -L - 0.03), "crimson", segs=6, rings=4, scale=(1, 1, 1.4))
    return p


def bench_yard():
    """Скамейка у подъезда: чугунные боковины, рейки, урна рядом."""
    p = Prop("bench_yard")
    for y in (-0.15, -0.05, 0.05, 0.15):
        p.box((1.8, 0.085, 0.035), (0, y, 0.45), "wood_old", bevel=0.008)
    for z in (0.62, 0.76, 0.9):
        p.box((1.8, 0.03, 0.085), (0, 0.24 + (z - 0.62) * 0.15, z), "wood_old", rot=(-10, 0, 0), bevel=0.008)
    for x in (-0.72, 0.72):
        p.poly_prism([(-0.2, 0), (-0.14, 0), (0, 0.38), (0.14, 0), (0.2, 0), (0.22, 0.43), (0.3, 0.95), (0.24, 0.95),
                      (0.16, 0.45), (-0.2, 0.43)], 0.05, (x, 0.02, 0), "metal_dark", rot=(90, 0, 90))
    p.tube(0.17, 0.15, 0.55, (1.25, 0, 0), "metal_dark", segs=8)
    p.box((0.2, 0.15, 0.004), (0.3, -0.05, 0.47), "paper", rot=(0, 0, 20))  # газета
    return p.collider((1.9, 0.6, 0.95), (0, 0.05, 0.475))


def swing_set():
    """Качели: А-образные стойки, перекладина, цепи, сиденья, песок под ними."""
    p = Prop("swing_set")
    for x in (-1.3, 1.3):
        p.beam((x, -0.7, 0), (x, 0, 2.2), 0.07, "paint_blue", segs=6)
        p.beam((x, 0.7, 0), (x, 0, 2.2), 0.07, "paint_blue", segs=6)
        p.beam((x, -0.35, 0.9), (x, 0.35, 0.9), 0.04, "paint_blue", segs=6)
        for y in (-0.7, 0.7):
            p.cyl(0.1, 0.08, (x, y, 0), "concrete", segs=6)
    p.beam((-1.4, 0, 2.2), (1.4, 0, 2.2), 0.08, "paint_blue", segs=6)
    for x, m, tilt in ((-0.6, "rubber_red", 0.0), (0.6, "paint_yellow", 0.25)):
        for dx in (-0.2, 0.2):
            top = (x + dx, 0, 2.18)
            bot = (x + dx, tilt, 0.5)
            pts = [(top[0], top[1] * (1 - t / 6) + bot[1] * t / 6, top[2] + (bot[2] - top[2]) * t / 6) for t in range(7)]
            for a, b in zip(pts, pts[1:]):
                p.beam(a, b, 0.018, "metal")
        p.box((0.48, 0.2, 0.04), (x, tilt, 0.48), m, bevel=0.008)
    p.box_floor((2.0, 1.2, 0.04), (0, 0, 0), "sand_dark")
    return p.collider((2.8, 1.4, 2.3), (0, 0, 1.15))


def tree_lowpoly():
    """Дерево двора: изогнутый ствол, ветви, несколько неровных крон, побелка снизу."""
    p = Prop("tree_lowpoly")
    p.curve_tube([(0, 0, 0), (0.05, 0, 1.2), (-0.05, 0.05, 2.2)], 0.26, "bark", segs=6)
    p.cyl(0.14, 0.9, (0, 0, 0), "whitewash", segs=6, r2=0.135)
    for tip in ((0.9, 0.2, 2.9), (-0.8, -0.3, 2.8), (0.1, 0.7, 3.1)):
        p.beam((-0.05, 0.05, 2.0), tip, 0.1, "bark", segs=5, thick2=0.05)
    p.blob(0.95, (0, 0, 3.2), "foliage", scale=(1.1, 1.1, 0.9), jitter=0.22)
    p.blob(0.7, (0.8, 0.2, 2.9), "foliage", jitter=0.25)
    p.blob(0.65, (-0.75, -0.3, 2.85), "foliage", jitter=0.25)
    p.blob(0.6, (0.1, 0.75, 3.3), "foliage", jitter=0.25)
    return p.collider((0.35, 0.35, 2.2), (0, 0, 1.1))


def hand_cart_journal():
    """Журнал экспедиции на планшете (р-н 30): зажим, листы, карандаш, строка «19:42 — вход в р-н 30»."""
    p = Prop("expedition_clipboard")
    p.box((0.23, 0.32, 0.01), (0, 0, 0.005), "wood_light", bevel=0.004)
    p.box((0.21, 0.28, 0.003), (0, -0.01, 0.0115), "paper_old")
    p.box((0.205, 0.275, 0.003), (0.003, -0.008, 0.014), "paper", rot=(0, 0, 2))
    p.box((0.09, 0.03, 0.015), (0, 0.15, 0.017), "metal", bevel=0.003)
    p.text("ЖУРНАЛ", (0, 0.09, 0.0165), 0.02, "black", depth=0.001, rot=(0, 0, 0))
    p.text("19:42 — вход в р-н 30.", (0, 0.05, 0.0165), 0.011, "black", depth=0.001, rot=(0, 0, 0))
    for i in range(6):
        p.box((0.14 - (i % 3) * 0.02, 0.002, 0.0005), (-0.01, 0.02 - i * 0.03, 0.0165), "black")
    p.beam((0.06, -0.12, 0.02), (0.13, 0.05, 0.02), 0.008, "paint_yellow", segs=6)
    return p


# --- новые объекты района
def kitchen_stove():
    """Кухня (р-н 10): газовая плита «Electra» с четырьмя конфорками, кастрюлей и чайником."""
    p = Prop("kitchen_stove")
    p.box_floor((0.6, 0.6, 0.85), (0, 0, 0), "enamel", bevel=0.02)
    p.box((0.5, 0.02, 0.42), (0, -0.305, 0.4), "black")  # стекло духовки
    p.box((0.4, 0.03, 0.03), (0, -0.33, 0.66), "metal")
    for i in range(4):
        p.cyl(0.02, 0.03, (-0.2 + i * 0.13, -0.31, 0.77), "black", segs=8, rot=(90, 0, 0))
    for x in (-0.14, 0.14):
        for y in (-0.14, 0.14):
            p.cyl(0.08, 0.015, (x, y, 0.85), "black", segs=10)
            for k in range(4):
                p.box((0.16, 0.012, 0.012), (x, y, 0.87), "metal_dark", rot=(0, 0, k * 45))
    p.tube(0.11, 0.1, 0.16, (-0.14, 0.14, 0.875), "enamel", segs=10)
    p.cyl(0.115, 0.012, (-0.14, 0.14, 1.035), "enamel", segs=10)
    p.sphere(0.1, (0.14, -0.14, 0.95), "metal", segs=8, rings=5, scale=(1, 1, 0.8))
    p.beam((0.22, -0.14, 0.93), (0.3, -0.14, 1.0), 0.02, "metal", segs=5)
    p.arc_tube((0.14, -0.14, 1.04), 0.07, 0, 180, 0.012, "black", steps=5)
    p.box_floor((0.6, 0.04, 0.12), (0, 0.29, 0.85), "enamel")
    return p.collider((0.6, 0.6, 0.85), (0, 0, 0.425))


def crt_tv():
    """Телевизор на тумбе — экран «снег»; для квартир районов."""
    p = Prop("crt_tv")
    p.box_floor((0.8, 0.45, 0.5), (0, 0, 0), "wood_dark", bevel=0.015)
    p.box((0.7, 0.01, 0.2), (0, -0.226, 0.25), "wood")
    p.box_floor((0.62, 0.5, 0.5), (0, 0.02, 0.5), "wood", bevel=0.03)
    p.box((0.44, 0.02, 0.34), (-0.05, -0.23, 0.75), "tv_static")
    p.box((0.48, 0.02, 0.38), (-0.05, -0.226, 0.75), "black")
    for z in (0.85, 0.75):
        p.cyl(0.02, 0.02, (0.24, -0.24, z), "black", segs=8, rot=(90, 0, 0))
    p.box((0.08, 0.005, 0.1), (0.24, -0.235, 0.6), "metal_dark")
    for a in (-25, 25):  # рога антенны
        p.beam((0, 0.05, 1.0), (math.sin(math.radians(a)) * 0.45, 0.05, 1.0 + 0.4), 0.008, "metal", segs=4)
    p.cyl(0.05, 0.02, (0, 0.05, 1.0), "black", segs=8)
    p.box((0.22, 0.15, 0.006), (0.2, -0.05, 1.003), "cloth_white")  # салфетка
    return p.collider((0.8, 0.5, 1.0), (0, 0.01, 0.5))


def entrance_stairwell_flight():
    """Лестничный марш подъезда: 9 ступеней, перила с деревянным поручнем. Подъём 1.4 м на 2.7 м по Y."""
    p = Prop("stairwell_flight")
    for i in range(9):
        p.box_floor((1.2, 0.3, 0.155), (0, -1.2 + i * 0.3, i * 0.155), "tile_floor")
        p.box_floor((1.2, 0.3, i * 0.155 + 0.001), (0, -1.2 + i * 0.3, 0), "concrete")
    for i in range(0, 9, 2):
        p.beam((0.58, -1.2 + i * 0.3, (i + 1) * 0.155), (0.58, -1.2 + i * 0.3, (i + 1) * 0.155 + 0.9), 0.02, "metal_dark")
    p.beam((0.58, -1.35, 1.05), (0.58, 1.35, 1.05 + 1.4), 0.06, "wood_dark")
    p.box((0.05, 2.7, 0.2), (-0.62, 0, 0.7), "paint_green")
    p.collider((1.2, 2.7, 0.8), (0, 0, 0.4))
    return p


PROPS = [
    panel_building_section, panel_entrance, dinner_table_10, chair_wooden, pendant_lamp_red,
    plate_food, radio_vintage, tear_calendar, clothesline, clothes_single, window_frame,
    street_lamp_sodium, apartment_door, photo_frame_wall, photo_frame_large, fridge_open,
    meat_chunk, wall_clock, alarm_clock_digital, mailbox_block, envelope, lullaby_window_block,
    interior_door_ajar, walkie_talkie, ceiling_stain, bench_yard, swing_set, tree_lowpoly,
    hand_cart_journal, kitchen_stove, crt_tv, entrance_stairwell_flight,
]
