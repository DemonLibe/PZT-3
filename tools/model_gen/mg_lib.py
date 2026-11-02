"""Библиотека для генерации low-poly моделей ПЗМ-3 в Blender (bpy).

Соглашения (важно для Godot):
- Метры, Z вверх в Blender -> при экспорте glTF Y вверх (как в Godot).
- Точка опоры объекта — центр основания (пол), объект стоит на Z=0.
- Плоское затенение (PS1). Материалы: процедурная текстура 64–128 px
  (nearest, повтор) в Base Color, цвет фактора белый -> RetroRender
  передаёт текстуру в ps1_surface.gdshader (albedo * texture).
- UV — кубическая проекция в метрах: плотность текселей одинакова на всех
  моделях, текстуры не растягиваются.
- Коллизии: отдельные боксы с суффиксом «-convcolonly».
"""
import math
import random
import zlib
import bpy
import bmesh
import numpy as np
from mathutils import Matrix, Vector, Euler

# ---------------------------------------------------------------- палитра
PALETTE = {
    "concrete": (0.42, 0.43, 0.40),
    "concrete_dark": (0.24, 0.25, 0.23),
    "panel_wall": (0.55, 0.55, 0.52),
    "tile_floor": (0.50, 0.47, 0.40),
    "tile_white": (0.78, 0.78, 0.74),
    "plaster": (0.72, 0.68, 0.60),
    "wallpaper": (0.55, 0.48, 0.36),
    "whitewash": (0.82, 0.78, 0.74),
    "asphalt": (0.16, 0.16, 0.16),
    "wood": (0.40, 0.25, 0.14),
    "wood_dark": (0.16, 0.10, 0.06),
    "wood_light": (0.62, 0.46, 0.30),
    "wood_old": (0.34, 0.30, 0.25),
    "metal": (0.45, 0.46, 0.47),
    "metal_dark": (0.15, 0.15, 0.16),
    "rust": (0.38, 0.20, 0.12),
    "black": (0.03, 0.03, 0.03),
    "cloth_white": (0.88, 0.86, 0.80),
    "cloth_gray": (0.70, 0.69, 0.65),
    "cloth_blue": (0.30, 0.36, 0.48),
    "cloth_check": (0.60, 0.30, 0.25),
    "tablecloth": (0.85, 0.83, 0.76),
    "porcelain": (0.90, 0.88, 0.82),
    "enamel": (0.86, 0.86, 0.80),
    "food": (0.45, 0.22, 0.10),
    "rice": (0.92, 0.90, 0.84),
    "soup": (0.62, 0.38, 0.14),
    "greens": (0.25, 0.42, 0.18),
    "glass_green": (0.20, 0.34, 0.24),
    "lamp_red": (0.48, 0.13, 0.10),
    "paint_green": (0.16, 0.33, 0.26),
    "paint_army": (0.26, 0.29, 0.20),
    "paint_blue": (0.22, 0.32, 0.44),
    "paint_yellow": (0.72, 0.58, 0.20),
    "mailbox_green": (0.42, 0.52, 0.38),
    "paper": (0.92, 0.90, 0.84),
    "paper_old": (0.78, 0.72, 0.58),
    "calendar_red": (0.66, 0.16, 0.12),
    "meat": (0.70, 0.22, 0.20),
    "sinew": (0.85, 0.55, 0.50),
    "sinew_old": (0.30, 0.16, 0.14),
    "grass": (0.18, 0.26, 0.14),
    "foliage": (0.17, 0.28, 0.15),
    "palm_leaf": (0.22, 0.36, 0.16),
    "bark": (0.20, 0.14, 0.10),
    "birch": (0.88, 0.88, 0.84),
    "sand_dark": (0.20, 0.13, 0.12),
    "rock": (0.30, 0.29, 0.27),
    "gold": (0.85, 0.66, 0.25),
    "crimson": (0.42, 0.10, 0.18),
    "velvet": (0.50, 0.08, 0.14),
    "marble": (0.90, 0.86, 0.80),
    "rubber_red": (0.75, 0.22, 0.16),
    "slide_blue": (0.30, 0.42, 0.62),
    "pink_flower": (0.90, 0.45, 0.52),
    "brick_roof": (0.60, 0.20, 0.14),
    "brick": (0.50, 0.24, 0.16),
    "radio_screen": (0.55, 0.92, 0.70),
    "book_a": (0.35, 0.22, 0.20),
    "book_b": (0.20, 0.26, 0.36),
    "book_c": (0.55, 0.45, 0.25),
    "eye_white": (0.85, 0.80, 0.70),
    "eye_iris": (0.55, 0.38, 0.10),
    "skin": (0.80, 0.62, 0.50),
    "chalk": (0.88, 0.88, 0.84),
    "plastic_red": (0.62, 0.15, 0.12),
    "chain_link": (0.40, 0.42, 0.43),
    "water_dark": (0.04, 0.05, 0.06),
}

EMISSIVE = {
    "window_lit": ((1.00, 0.70, 0.32), 2.0),
    "window_dark": ((0.05, 0.06, 0.09), 0.0),
    "lamp_glow": ((1.00, 0.85, 0.60), 3.0),
    "fluorescent": ((0.78, 0.90, 0.78), 3.0),
    "sodium": ((1.00, 0.65, 0.30), 4.0),
    "floodlight": ((0.95, 0.97, 1.00), 5.0),
    "bulb_yellow": ((1.00, 0.85, 0.30), 3.0),
    "bulb_pink": ((1.00, 0.35, 0.60), 3.0),
    "bulb_green": ((0.30, 1.00, 0.70), 3.0),
    "led_red": ((1.00, 0.20, 0.15), 4.0),
    "screen_green": ((0.45, 0.95, 0.60), 2.0),
    "halo": ((1.00, 0.95, 0.80), 4.0),
    "tv_static": ((0.60, 0.65, 0.70), 1.5),
}

# ---------------------------------------------------------------- текстуры
# материал -> (генератор, размер px, сколько метров на один повтор)
_rng_tex = np.random.default_rng(1337)


def _noise(n, scale, rng, octaves=3):
    """Плавный шум 0..1 (сумма октав, апскейл билинейно), бесшовный."""
    out = np.zeros((n, n))
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        cells = max(2, int(scale * 2 ** o))
        g = rng.random((cells, cells))
        g = np.pad(g, ((0, 1), (0, 1)), mode="wrap")
        xs = np.linspace(0, cells, n, endpoint=False)
        i = xs.astype(int)
        f = xs - i
        f = f * f * (3 - 2 * f)
        a = g[i][:, i]
        b = g[i][:, i + 1]
        c = g[i + 1][:, i]
        d = g[i + 1][:, i + 1]
        fx = f[None, :]
        fy = f[:, None]
        out += amp * ((a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy)
        tot += amp
        amp *= 0.5
    return out / tot


def _apply(base, lum):
    return np.clip(np.array(base)[None, None, :] * lum[:, :, None], 0, 1)


def tex_concrete(n, base, rng, seams=False, stains=True):
    lum = 0.82 + 0.3 * _noise(n, 3, rng, 4) + 0.12 * (rng.random((n, n)) - 0.5)
    if stains:  # вертикальные подтёки (по V — ось Z модели)
        cols = _noise(n, 6, rng, 1)[0]
        streak = (cols > 0.62) * (cols - 0.62) * 2.0
        fade = np.linspace(1.0, 0.2, n)[:, None]
        lum -= streak[None, :] * fade * 0.9
    pits = rng.random((n, n)) > 0.985
    lum[pits] *= 0.6
    if seams:
        lum[:, :2] *= 0.55
        lum[:2, :] *= 0.55
    return _apply(base, lum)


def tex_wood(n, base, rng):
    y = np.arange(n)[:, None]
    warp = _noise(n, 2, rng, 2) * 14
    rings = 0.5 + 0.5 * np.sin((y + warp) * 0.9)
    lum = 0.78 + 0.22 * rings + 0.12 * (_noise(n, 8, rng, 2) - 0.5)
    lum[(np.arange(n) % (n // 4)) == 0, :] *= 0.6  # стыки досок
    return _apply(base, lum)


def tex_metal(n, base, rng):
    lum = 0.88 + 0.16 * _noise(n, 4, rng, 3)
    for _ in range(18):  # царапины
        x, y = rng.integers(0, n, 2)
        L = rng.integers(4, n // 3)
        lum[y % n, np.arange(x, x + L) % n] += 0.25
    rust = _noise(n, 3, rng, 3)
    out = _apply(base, lum)
    m = np.clip((rust - 0.68) * 4, 0, 1)[:, :, None]
    return out * (1 - m) + np.array(PALETTE["rust"]) * m


def tex_rust(n, base, rng):
    lum = 0.7 + 0.5 * _noise(n, 5, rng, 4) + 0.15 * (rng.random((n, n)) - 0.5)
    return _apply(base, lum)


def tex_cloth(n, base, rng):
    x = np.arange(n)
    weave = 0.92 + 0.08 * ((x[None, :] + x[:, None]) % 2)
    lum = weave * (0.86 + 0.18 * _noise(n, 3, rng, 2))
    return _apply(base, lum)


def tex_check(n, base, rng):
    x = np.arange(n) // (n // 8)
    chk = ((x[None, :] + x[:, None]) % 2) * 0.5 + 0.5
    lum = chk * (0.9 + 0.1 * _noise(n, 4, rng, 2))
    out = _apply(base, lum)
    white = ((x[None, :] % 2) * (x[:, None] % 2)).astype(bool)
    out[white] = np.array(PALETTE["cloth_white"]) * 0.9
    return out


def tex_tiles(n, base, rng, cells=4):
    lum = 0.9 + 0.12 * _noise(n, 4, rng, 2)
    step = n // cells
    idx = np.arange(n)
    lum[idx % step < 1, :] *= 0.5
    lum[:, idx % step < 1] *= 0.5
    for cy in range(cells):
        for cx in range(cells):
            lum[cy * step + 1:(cy + 1) * step, cx * step + 1:(cx + 1) * step] *= 0.92 + 0.16 * rng.random()
    return _apply(base, lum)


def tex_brick(n, base, rng):
    lum = 0.85 + 0.2 * _noise(n, 6, rng, 2)
    rows = n // 8
    for r in range(8):
        lum[r * rows, :] *= 0.45
        off = (r % 2) * (n // 8)
        for c in range(4):
            lum[r * rows:(r + 1) * rows, (off + c * n // 4) % n] *= 0.45
            lum[r * rows + 1:(r + 1) * rows, (off + c * n // 4 + 1) % n:(off + (c + 1) * n // 4) % n or n] *= 0.9 + 0.2 * rng.random()
    return _apply(base, lum)


def tex_roof(n, base, rng):
    lum = 0.85 + 0.15 * _noise(n, 5, rng, 2)
    y = np.arange(n)
    wave = (y % (n // 8)) / (n // 8)
    lum *= (0.65 + 0.35 * wave)[:, None]
    return _apply(base, lum)


def tex_wallpaper(n, base, rng):
    x = np.arange(n)
    stripes = 0.88 + 0.12 * ((x // 4) % 2)
    lum = stripes[None, :] * (0.88 + 0.16 * _noise(n, 3, rng, 3))
    dots = ((x[None, :] % 16 == 8) & (x[:, None] % 16 == 8))
    lum[dots] *= 0.7
    return _apply(base, lum)


def tex_foliage(n, base, rng):
    lum = 0.55 + 0.7 * _noise(n, 8, rng, 3)
    lum += 0.25 * (rng.random((n, n)) - 0.5)
    return _apply(base, lum)


def tex_bark(n, base, rng):
    x = np.arange(n)
    warp = _noise(n, 3, rng, 2) * 8
    ridges = 0.5 + 0.5 * np.sin((x[None, :] + warp) * 1.2)
    lum = 0.6 + 0.5 * ridges * (0.7 + 0.3 * _noise(n, 6, rng, 2))
    return _apply(base, lum)


def tex_birch(n, base, rng):
    lum = 0.9 + 0.1 * _noise(n, 4, rng, 2)
    out = _apply(base, lum)
    marks = _noise(n, 6, rng, 1)
    m = (marks > 0.7)
    # чёрные горизонтальные чечевички берёзы
    m &= (np.arange(n)[:, None] % 6) < 2
    out[m] = (0.06, 0.06, 0.06)
    return out


def tex_rock(n, base, rng):
    lum = 0.65 + 0.6 * _noise(n, 4, rng, 5) + 0.12 * (rng.random((n, n)) - 0.5)
    return _apply(base, lum)


def tex_sand(n, base, rng):
    lum = 0.75 + 0.4 * _noise(n, 6, rng, 4) + 0.2 * (rng.random((n, n)) - 0.5)
    return _apply(base, lum)


def tex_meat(n, base, rng):
    out = _apply(base, 0.75 + 0.4 * _noise(n, 5, rng, 3))
    fat = _noise(n, 4, rng, 2)
    m = np.clip(1 - np.abs(fat - 0.5) * 14, 0, 1)[:, :, None]
    return out * (1 - m) + np.array((0.92, 0.80, 0.72)) * m


def tex_gold(n, base, rng):
    lum = 0.75 + 0.45 * _noise(n, 6, rng, 2) + 0.15 * (rng.random((n, n)) > 0.97)
    return _apply(base, lum)


def tex_marble(n, base, rng):
    out = _apply(base, 0.94 + 0.08 * _noise(n, 3, rng, 2))
    v = _noise(n, 3, rng, 4)
    m = np.clip(1 - np.abs(v - 0.5) * 22, 0, 1)[:, :, None] * 0.5
    return out * (1 - m) + np.array((0.45, 0.44, 0.42)) * m


def tex_plain(n, base, rng):
    return _apply(base, 0.88 + 0.16 * _noise(n, 3, rng, 3) + 0.05 * (rng.random((n, n)) - 0.5))


def tex_paper(n, base, rng):
    out = tex_plain(n, base, rng)
    y = np.arange(n)
    out[(y % 8) == 0, :] *= 0.85  # линовка
    return out


def tex_chainlink(n, base, rng):
    """Сетка-рабица: ромбы проволоки на тёмном фоне (непрозрачно — PS1 без альфы)."""
    x = np.arange(n)
    d1 = (x[None, :] + x[:, None]) % 16 < 2
    d2 = (x[None, :] - x[:, None]) % 16 < 2
    out = np.zeros((n, n, 3)) + np.array((0.06, 0.07, 0.07))
    out[d1 | d2] = np.array(base) * 1.2
    return np.clip(out, 0, 1)


def tex_velvet(n, base, rng):
    lum = 0.7 + 0.5 * _noise(n, 2, rng, 2)
    return _apply(base, lum)


def tex_water(n, base, rng):
    lum = 0.7 + 0.8 * _noise(n, 3, rng, 3)
    return _apply(base, lum)


TEXTURES = {
    "concrete": (lambda n, b, r: tex_concrete(n, b, r), 128, 3.0),
    "concrete_dark": (lambda n, b, r: tex_concrete(n, b, r), 128, 3.0),
    "panel_wall": (lambda n, b, r: tex_concrete(n, b, r, seams=True), 128, 3.0),
    "tile_floor": (lambda n, b, r: tex_tiles(n, b, r, 4), 64, 1.2),
    "tile_white": (lambda n, b, r: tex_tiles(n, b, r, 8), 64, 1.2),
    "plaster": (tex_plain, 64, 2.0),
    "whitewash": (tex_plain, 64, 2.0),
    "wallpaper": (tex_wallpaper, 64, 1.0),
    "asphalt": (tex_sand, 64, 2.0),
    "wood": (tex_wood, 64, 1.0),
    "wood_dark": (tex_wood, 64, 1.0),
    "wood_light": (tex_wood, 64, 1.0),
    "wood_old": (tex_wood, 64, 1.0),
    "metal": (tex_metal, 64, 1.0),
    "metal_dark": (tex_metal, 64, 1.0),
    "rust": (tex_rust, 64, 1.0),
    "paint_green": (tex_metal, 64, 1.5),
    "paint_army": (tex_metal, 64, 1.5),
    "paint_blue": (tex_metal, 64, 1.5),
    "paint_yellow": (tex_metal, 64, 1.5),
    "mailbox_green": (tex_metal, 64, 1.0),
    "cloth_white": (tex_cloth, 32, 0.5),
    "cloth_gray": (tex_cloth, 32, 0.5),
    "cloth_blue": (tex_cloth, 32, 0.5),
    "cloth_check": (tex_check, 64, 0.6),
    "tablecloth": (tex_check, 64, 0.8),
    "brick": (tex_brick, 64, 1.5),
    "brick_roof": (tex_roof, 64, 1.5),
    "foliage": (tex_foliage, 64, 1.5),
    "palm_leaf": (tex_foliage, 32, 1.0),
    "grass": (tex_foliage, 64, 1.5),
    "bark": (tex_bark, 64, 1.0),
    "birch": (tex_birch, 64, 1.0),
    "rock": (tex_rock, 64, 2.0),
    "sand_dark": (tex_sand, 128, 4.0),
    "meat": (tex_meat, 32, 0.4),
    "gold": (tex_gold, 32, 0.6),
    "marble": (tex_marble, 64, 2.0),
    "paper_old": (tex_paper, 32, 0.3),
    "chain_link": (tex_chainlink, 64, 0.5),
    "velvet": (tex_velvet, 32, 1.0),
    "crimson": (tex_velvet, 32, 1.0),
    "water_dark": (tex_water, 64, 4.0),
    "sinew": (tex_meat, 32, 0.3),
    "sinew_old": (tex_rust, 32, 0.5),
    "enamel": (tex_plain, 32, 1.0),
    "porcelain": (tex_plain, 32, 1.0),
}

_mats = {}
_tile = {}


def tile_size(material):
    t = TEXTURES.get(material)
    return t[2] if t else 1.0


def mat(name):
    """Материал по имени (кэш — одинаковые имена во всех моделях)."""
    if name in _mats:
        return _mats[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    bsdf.inputs["Roughness"].default_value = 1.0
    bsdf.inputs["Metallic"].default_value = 0.0
    if name in EMISSIVE:
        col, strength = EMISSIVE[name]
        bsdf.inputs["Base Color"].default_value = (*col, 1)
        if strength > 0:
            bsdf.inputs["Emission Color"].default_value = (*col, 1)
            bsdf.inputs["Emission Strength"].default_value = strength
    else:
        col = PALETTE[name]
        if name in TEXTURES:
            gen, size, _ = TEXTURES[name]
            rng = np.random.default_rng(zlib.crc32(name.encode()))
            px = gen(size, col, rng)                       # sRGB 0..1
            rgba = np.concatenate([px, np.ones((size, size, 1))], axis=2)
            img = bpy.data.images.new(f"T_{name}", size, size, alpha=False)
            img.colorspace_settings.name = "sRGB"
            img.pixels.foreach_set(rgba[::-1].astype(np.float32).ravel())  # Blender: строки снизу вверх
            img.pack()
            tn = nt.nodes.new("ShaderNodeTexImage")
            tn.image = img
            tn.interpolation = "Closest"
            nt.links.new(tn.outputs["Color"], bsdf.inputs["Base Color"])
        else:
            bsdf.inputs["Base Color"].default_value = (*_srgb_to_lin(col), 1)
    m.diffuse_color = (*col, 1)
    _mats[name] = m
    return m


def _srgb_to_lin(c):
    # палитра задумана как «линейные» значения — оставляем как есть (так было в v1)
    return c


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _mats.clear()


# ---------------------------------------------------------------- построение
class Prop:
    """Собирает части в один меш. Все размеры — метры."""

    def __init__(self, name, seed=None):
        self.name = name
        self.bm = bmesh.new()
        self.mat_index = {}
        self.colliders = []
        self.rng = random.Random(seed if seed is not None else name)

    def _mi(self, material):
        if material not in self.mat_index:
            self.mat_index[material] = len(self.mat_index)
        return self.mat_index[material]

    @staticmethod
    def _matrix(loc, rot, scale=(1, 1, 1)):
        r = Euler([math.radians(a) for a in rot]).to_matrix().to_4x4()
        s = Matrix.Diagonal((*scale, 1))
        return Matrix.Translation(Vector(loc)) @ r @ s

    def _snapshot(self):
        """Помечаем всё существующее: новые элементы получат метку 0 (надёжнее, чем сравнение
        ссылок — bmesh переиспользует память удалённых вершин)."""
        vl = self.bm.verts.layers.int.get("old") or self.bm.verts.layers.int.new("old")
        fl = self.bm.faces.layers.int.get("old") or self.bm.faces.layers.int.new("old")
        for v in self.bm.verts:
            v[vl] = 1
        for f in self.bm.faces:
            f[fl] = 1
        return vl, fl

    def _diff(self, snap):
        vl, fl = snap
        return [v for v in self.bm.verts if v[vl] == 0], [f for f in self.bm.faces if f[fl] == 0]

    def _finish(self, snap, matrix, material, jitter=0.0, bevel=0.0):
        v, f = self._diff(snap)
        bmesh.ops.transform(self.bm, matrix=matrix, verts=v)
        if jitter:
            for vert in v:
                vert.co += Vector((self.rng.uniform(-jitter, jitter), self.rng.uniform(-jitter, jitter),
                                   self.rng.uniform(-jitter, jitter)))
        if bevel:
            edges = list({e for vert in v for e in vert.link_edges})
            bmesh.ops.bevel(self.bm, geom=edges, offset=bevel, offset_type="OFFSET", segments=1,
                            profile=0.5, affect="EDGES", clamp_overlap=True)
            v, f = self._diff(snap)
        idx = self._mi(material)
        for face in f:
            face.material_index = idx
        return self

    # --- примитивы
    def box(self, size, loc, material, rot=(0, 0, 0), bevel=0.0, jitter=0.0):
        snap = self._snapshot()
        bmesh.ops.create_cube(self.bm, size=1.0)
        b = min(bevel, min(size) * 0.45) if bevel else 0.0
        return self._finish(snap, self._matrix(loc, rot, size), material, jitter, b)

    def box_floor(self, size, loc, material, rot=(0, 0, 0), bevel=0.0, jitter=0.0):
        return self.box(size, (loc[0], loc[1], loc[2] + size[2] / 2), material, rot, bevel, jitter)

    def cyl(self, r, h, loc, material, segs=8, rot=(0, 0, 0), r2=None, jitter=0.0):
        snap = self._snapshot()
        bmesh.ops.create_cone(self.bm, cap_ends=True, cap_tris=False, segments=segs,
                              radius1=r, radius2=r if r2 is None else r2, depth=h,
                              matrix=Matrix.Translation((0, 0, h / 2)))
        return self._finish(snap, self._matrix(loc, rot), material, jitter)

    def tube(self, r_out, r_in, h, loc, material, segs=10, rot=(0, 0, 0)):
        """Полый цилиндр (миска, ведро, чашка — с толщиной стенки и дном)."""
        snap = self._snapshot()
        outer = bmesh.ops.create_cone(self.bm, cap_ends=False, segments=segs, radius1=r_out, radius2=r_out,
                                      depth=h, matrix=Matrix.Translation((0, 0, h / 2)))["verts"]
        inner_v = bmesh.ops.create_cone(self.bm, cap_ends=False, segments=segs, radius1=r_in, radius2=r_in,
                                        depth=h * 0.9, matrix=Matrix.Translation((0, 0, h * 0.55)))["verts"]
        inner_f = list({f for v in inner_v for f in v.link_faces})
        bmesh.ops.reverse_faces(self.bm, faces=inner_f)
        # кольцо сверху и дно
        top_o = sorted([v for v in outer if v.co.z > h * 0.99], key=lambda v: math.atan2(v.co.y, v.co.x))
        top_i = sorted([v for v in inner_v if v.co.z > h * 0.99], key=lambda v: math.atan2(v.co.y, v.co.x))
        for k in range(segs):
            a, b = top_o[k], top_o[(k + 1) % segs]
            c, d = top_i[(k + 1) % segs], top_i[k]
            self.bm.faces.new((a, b, c, d))
        bot_o = [v for v in outer if v.co.z < 0.001]
        bot_i = [v for v in inner_v if v.co.z < h * 0.11]
        self.bm.faces.new(sorted(bot_o, key=lambda v: -math.atan2(v.co.y, v.co.x)))
        self.bm.faces.new(sorted(bot_i, key=lambda v: math.atan2(v.co.y, v.co.x)))
        return self._finish(snap, self._matrix(loc, rot), material)

    def sphere(self, r, loc, material, segs=8, rings=5, scale=(1, 1, 1), rot=(0, 0, 0), jitter=0.0):
        snap = self._snapshot()
        bmesh.ops.create_uvsphere(self.bm, u_segments=segs, v_segments=rings, radius=r)
        return self._finish(snap, self._matrix(loc, rot, scale), material, jitter)

    def blob(self, r, loc, material, scale=(1, 1, 1), jitter=0.25, subdiv=1):
        """Неровная органика: икосфера с шумом (кроны, камни, туши, груды)."""
        snap = self._snapshot()
        bmesh.ops.create_icosphere(self.bm, subdivisions=subdiv, radius=r)
        return self._finish(snap, self._matrix(loc, (0, 0, self.rng.uniform(0, 360)), scale), material,
                            jitter * r)

    def beam(self, a, b, thick, material, segs=None, thick2=None):
        a, b = Vector(a), Vector(b)
        d = b - a
        length = d.length
        snap = self._snapshot()
        if segs:
            bmesh.ops.create_cone(self.bm, cap_ends=True, segments=segs, radius1=thick / 2,
                                  radius2=(thick2 if thick2 is not None else thick) / 2, depth=length,
                                  matrix=Matrix.Translation((0, 0, length / 2)))
        else:
            bmesh.ops.create_cube(self.bm, size=1.0,
                                  matrix=Matrix.Translation((0, 0, length / 2)) @
                                  Matrix.Diagonal((thick, thick, length, 1)))
        q = Vector((0, 0, 1)).rotation_difference(d.normalized())
        return self._finish(snap, Matrix.Translation(a) @ q.to_matrix().to_4x4(), material)

    def poly_prism(self, pts2d, depth, loc, material, rot=(90, 0, 0)):
        snap = self._snapshot()
        verts = [self.bm.verts.new((x, y, 0)) for x, y in pts2d]
        face = self.bm.faces.new(verts)
        ext = bmesh.ops.extrude_face_region(self.bm, geom=[face])
        moved = [e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)]
        bmesh.ops.translate(self.bm, vec=(0, 0, depth), verts=moved)
        bmesh.ops.translate(self.bm, vec=(0, 0, -depth / 2), verts=self._diff(snap)[0])
        return self._finish(snap, self._matrix(loc, rot), material)

    def arc_tube(self, center, radius, a0, a1, thick, material, steps=8, plane="xz", segs=None):
        pts = []
        for i in range(steps + 1):
            t = math.radians(a0 + (a1 - a0) * i / steps)
            if plane == "xz":
                pts.append((center[0] + radius * math.cos(t), center[1], center[2] + radius * math.sin(t)))
            else:
                pts.append((center[0] + radius * math.cos(t), center[1] + radius * math.sin(t), center[2]))
        return self.curve_tube(pts, thick, material, segs)

    def curve_tube(self, pts, thick, material, segs=None):
        for p, q in zip(pts, pts[1:]):
            self.beam(p, q, thick, material, segs)
        return self

    def sag(self, a, b, drop, steps=10):
        """Точки провисающей верёвки/провода между a и b."""
        out = []
        for i in range(steps + 1):
            t = i / steps
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t,
                        a[2] + (b[2] - a[2]) * t - drop * 4 * t * (1 - t)))
        return out

    def text(self, body, loc, height, material, depth=0.01, rot=(90, 0, 0), align="CENTER"):
        cu = bpy.data.curves.new("txt", "FONT")
        cu.body = body
        cu.size = height
        cu.extrude = depth / 2
        cu.align_x = align
        cu.align_y = "CENTER"
        cu.resolution_u = 1 if height < 0.05 else 2
        ob = bpy.data.objects.new("txt", cu)
        bpy.context.scene.collection.objects.link(ob)
        dg = bpy.context.evaluated_depsgraph_get()
        me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
        snap = self._snapshot()
        self.bm.from_mesh(me)
        bpy.data.objects.remove(ob)
        bpy.data.meshes.remove(me)
        return self._finish(snap, self._matrix(loc, rot), material)

    # --- составные детали, которые часто повторяются
    def pipe_run(self, a, b, r, material="metal_dark", brackets=True):
        """Труба с хомутами (коридоры, фасады)."""
        self.beam(a, b, r * 2, material, segs=6)
        if brackets:
            a, b = Vector(a), Vector(b)
            n = max(1, int((b - a).length / 1.2))
            for i in range(n + 1):
                p = a + (b - a) * (i / n)
                self.cyl(r * 1.35, 0.05, (p.x, p.y, p.z - 0.025), material, segs=6,
                         rot=self._axis_rot(b - a))
        return self

    @staticmethod
    def _axis_rot(d):
        d = Vector(d).normalized()
        if abs(d.z) > 0.9:
            return (0, 0, 0)
        if abs(d.x) > abs(d.y):
            return (0, 90, 0)
        return (90, 0, 0)

    def cable(self, a, b, drop, material="black", thick=0.015):
        return self.curve_tube(self.sag(a, b, drop, 8), thick, material)

    def collider(self, size, center, rot_z=0.0):
        self.colliders.append((size, center, rot_z))
        return self

    def collider_auto(self):
        xs = [v.co.x for v in self.bm.verts]
        ys = [v.co.y for v in self.bm.verts]
        zs = [v.co.z for v in self.bm.verts]
        size = (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
        center = ((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, (max(zs) + min(zs)) / 2)
        return self.collider(size, center)

    # --- выход
    def _uv_box(self):
        """Кубическая проекция UV в метрах / размер тайла материала."""
        uv = self.bm.loops.layers.uv.verify()
        inv = {v: k for k, v in self.mat_index.items()}
        for f in self.bm.faces:
            n = f.normal
            ax = max(range(3), key=lambda i: abs(n[i]))
            ts = tile_size(inv.get(f.material_index, ""))
            for loop in f.loops:
                c = loop.vert.co
                if ax == 2:
                    u, v = c.x, c.y * (1 if n.z > 0 else -1)
                elif ax == 0:
                    u, v = c.y * (1 if n.x > 0 else -1), c.z
                else:
                    u, v = c.x * (-1 if n.y > 0 else 1), c.z
                loop[uv].uv = (u / ts, v / ts)

    def build(self):
        bmesh.ops.remove_doubles(self.bm, verts=self.bm.verts, dist=0.0001)
        bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces)
        self.bm.normal_update()
        self._uv_box()
        me = bpy.data.meshes.new(self.name)
        self.bm.to_mesh(me)
        self.bm.free()
        for m in sorted(self.mat_index, key=self.mat_index.get):
            me.materials.append(mat(m))
        for p in me.polygons:
            p.use_smooth = False
        ob = bpy.data.objects.new(self.name, me)
        bpy.context.scene.collection.objects.link(ob)
        out = [ob]
        for i, (size, center, rz) in enumerate(self.colliders):
            cbm = bmesh.new()
            bmesh.ops.create_cube(cbm, size=1.0)
            bmesh.ops.transform(cbm, verts=cbm.verts,
                                matrix=Matrix.Translation(Vector(center)) @
                                Matrix.Rotation(math.radians(rz), 4, "Z") @
                                Matrix.Diagonal((*size, 1)))
            cme = bpy.data.meshes.new(f"{self.name}_col{i}")
            cbm.to_mesh(cme)
            cbm.free()
            suffix = f"_{i}" if len(self.colliders) > 1 else ""
            cob = bpy.data.objects.new(f"{self.name}_col{suffix}-convcolonly", cme)
            bpy.context.scene.collection.objects.link(cob)
            cob.parent = ob
            out.append(cob)
        return out


def export_glb(objs, path):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.gltf(
        filepath=path, export_format="GLB", use_selection=True, export_apply=True,
        export_yup=True, export_materials="EXPORT", export_image_format="AUTO",
        export_texcoords=True, export_normals=True, export_cameras=False,
        export_lights=False, export_animations=False,
    )
