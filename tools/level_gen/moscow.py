"""Московский спальный двор: пятиэтажки, подъезды, площадка, гаражи, деревья.
Окна фасада лежат в мировой сетке: столбцы z = 3k + 1.5, этажи y = 3n + 1.425."""
from tscn import *
from level_common import *

G = "NavigationRegion3D/Geometry"
FACADE_SCALE = 1.0 / 3.0
WIN_Y = 1.425
WIN_W, WIN_H = 1.7, 1.4


class Mats:
    """Общие материалы двора (создаются один раз на сцену)."""
    def __init__(self, sc, beige=False):
        self.facade = material(sc, (1, 1, 1), tex="facade_panel_beige" if beige else "facade_panel", scale=FACADE_SCALE)
        self.plinth = material(sc, (0.55, 0.55, 0.55), tex="concrete", scale=0.5)
        self.roof = material(sc, (0.35, 0.35, 0.37), tex="concrete_floor", scale=0.4)
        self.asphalt = material(sc, (0.5, 0.5, 0.52), tex="asphalt", scale=0.3)
        self.walk = material(sc, (0.75, 0.75, 0.72), tex="sidewalk", scale=0.6)
        self.door = material(sc, (0.55, 0.35, 0.25), tex="metal_rust", scale=1.0)
        self.metal = material(sc, (0.6, 0.62, 0.6), tex="metal_rust", scale=1.0)
        self.garage = material(sc, (0.55, 0.6, 0.55), tex="metal_clean", scale=0.6)
        self.wood = material(sc, (0.8, 0.75, 0.7), tex="wood_fence", scale=1.0)
        self.paint = material(sc, (0.3, 0.55, 0.35), tex="metal_clean", scale=1.0)
        self.trunk = material(sc, (0.35, 0.28, 0.22), tex="wood_door", scale=1.0)
        self.leaves = material(sc, (0.18, 0.28, 0.16))
        self.sand = material(sc, (0.8, 0.72, 0.55), tex="concrete_floor", scale=0.5)
        self.fence = material(sc, (0.75, 0.75, 0.73), tex="block_wall", scale=0.7)
        self.glow = sc.sub_res("StandardMaterial3D", shading_mode=0, albedo_color=C(1.0, 0.82, 0.5))
        self.glow_quad = sc.sub_res("QuadMesh", material=self.glow, size=V2(WIN_W - 0.15, WIN_H - 0.15))


def panel_block(sc, m, name, x, z, length=30.0, depth=12.0, floors=5, facing=1, entrances=(-10.5, 1.5, 10.5),
                room=None):
    """Пятиэтажка. facing=+1 — фасад с подъездами смотрит в +X. room=(z_центр, ширина) — квартира на 1-м этаже."""
    h = floors * 3.0
    front = x + facing * depth / 2
    if room is None:
        box(sc, name, (x, h / 2, z), (depth, h, length), m.facade)
    else:
        rz, rw = room
        sc.node(name, "CSGCombiner3D", G, transform=T(x, 0, z), use_collision=True)
        sc.node("Body", "CSGBox3D", f"{G}/{name}", transform=T(0, h / 2, 0), size=V3(depth, h, length), material=m.facade)
        sc.node("Room", "CSGBox3D", f"{G}/{name}", operation=2, transform=T(facing * (depth / 2 - 3.4), 1.45, rz - z),
                size=V3(6.0, 2.8, rw), material=m.plinth)
        sc.node("Doorway", "CSGBox3D", f"{G}/{name}", operation=2,
                transform=T(facing * (depth / 2 - 0.2), 1.1, rz - z + rw / 2 - 1.0), size=V3(0.8, 2.2, 1.2), material=m.plinth)
    box(sc, name + "Roof", (x, h + 0.25, z), (depth + 0.3, 0.5, length + 0.3), m.roof)
    box(sc, name + "Plinth", (front + facing * 0.05, 0.3, z), (0.12, 0.6, length), m.plinth, collision=False)
    for i, ez in enumerate(entrances):
        n = f"{name}Entrance{i+1}"
        box(sc, n + "Door", (front + facing * 0.04, 1.05, ez), (0.08, 2.1, 1.2), m.door)
        box(sc, n + "Canopy", (front + facing * 0.7, 2.6, ez), (1.4, 0.12, 2.0), m.plinth, collision=False)
        box(sc, n + "Step", (front + facing * 0.6, 0.1, ez), (1.2, 0.2, 2.0), m.plinth)
        lamp(sc, n + "Lamp", (front + facing * 0.5, 2.4, ez), color=(1.0, 0.8, 0.55), energy=0.9, rng=6.0)
        box(sc, n + "Bench", (front + facing * 1.6, 0.25, ez + 2.2), (0.5, 0.5, 1.6), m.wood)
    return front


def lit_windows(sc, m, name, front, facing, z_from, z_to, rng_seed, count=10, floors=(1, 2, 3, 4), skip=()):
    """Горящие окна на фасаде (светящиеся квады без источников света)."""
    import random
    r = random.Random(rng_seed)
    slots = [(3 * k + 1.5, fl) for k in range(int(z_from // 3), int(z_to // 3)) for fl in floors
             if z_from < 3 * k + 1.5 < z_to and (3 * k + 1.5) not in skip]
    r.shuffle(slots)
    sc.node(name, "Node3D", ".")
    yaw = 90.0 if facing > 0 else -90.0
    for i, (wz, fl) in enumerate(slots[:count]):
        sc.node(f"Glow{i+1}", "MeshInstance3D", name, transform=T(front + facing * 0.02, WIN_Y + 3 * fl, wz, yaw=yaw),
                mesh=m.glow_quad)


def window_slot(front, facing, wz, floor=0):
    """Позиция и поворот окна фасада (для окон-аномалий)."""
    return (front + facing * 0.03, WIN_Y + 3 * floor, wz, 90.0 if facing > 0 else -90.0)


def tree(sc, m, name, x, z, h=5.0):
    cylinder(sc, name + "Trunk", (x, h * 0.35, z), 0.15, h * 0.7, m.trunk)
    sc.node(name + "Crown", "CSGSphere3D", G, transform=T(x, h * 0.8, z), radius=1.6, radial_segments=8, rings=5,
            material=m.leaves)


def courtyard(sc, m, width=16.0, length=40.0, playground=True, garages=True):
    """Земля, тротуары, площадка, гаражи, фонари, деревья, баки."""
    box(sc, "Ground", (0, -0.25, 0), (60, 0.5, 60), m.asphalt)
    for side in (-1, 1):
        box(sc, f"Walk{side}", (side * (width / 2 - 0.8), 0.05, 0), (1.6, 0.1, 30), m.walk)
    if playground:
        box(sc, "Sandbox", (-1.5, 0.15, -4.0), (2.5, 0.3, 2.5), m.wood)
        box(sc, "Sand", (-1.5, 0.28, -4.0), (2.2, 0.06, 2.2), m.sand, collision=False)
        for i, dx in enumerate((-0.9, 0.9)):
            box(sc, f"SwingPost{i}", (2.5 + dx, 1.2, -4.0), (0.1, 2.4, 0.1), m.paint)
        box(sc, "SwingBar", (2.5, 2.4, -4.0), (2.0, 0.1, 0.1), m.paint)
        box(sc, "SwingSeat", (2.5, 0.6, -4.0), (0.6, 0.06, 0.3), m.wood, collision=False)
    if garages:
        for i in range(5):
            box(sc, f"Garage{i+1}", (-6.0 + i * 3.0, 1.2, -19.5), (2.9, 2.4, 5.0), m.garage)
    for i, (x, z) in enumerate(((-5.5, -12), (5.5, 0), (-5.5, 12))):
        cylinder(sc, f"LampPost{i+1}", (x, 2.5, z), 0.07, 5.0, m.metal)
        lamp(sc, f"YardLamp{i+1}", (x, 4.9, z), color=(1.0, 0.85, 0.6), energy=1.3, rng=10.0)
    for i, (x, z) in enumerate(((4.5, -12.5), (-4.5, 5.5), (4.5, 9.0))):
        tree(sc, m, f"Tree{i+1}", x, z)
    for i in range(2):
        box(sc, f"TrashBin{i+1}", (5.8, 0.6, 15.5 + i * 1.3), (1.0, 1.2, 1.1), m.paint)


def south_gate(sc, m, width=16.0, z=20.0):
    """Забор с выходом (КПП) на южной стороне двора."""
    for side in (-1, 1):
        box(sc, f"GateFence{side}", (side * (width / 4 + 0.4), 1.0, z), (width / 2 - 0.8, 2.0, 0.2), m.fence)
    exit_door(sc, (0, 0, z - 0.2), 180)


NPC_SPAWNS = [(-4, 15), (-2.5, 14), (2.5, 14), (4, 15), (-4, 12.5), (4, 12.5)]


def spawns(sc):
    spawn(sc, "Player", (0, 0, 16.5), 0)
    for i, (x, z) in enumerate(NPC_SPAWNS):
        spawn(sc, f"Npc{i+1}", (x, 0, z), 0)


def standard_yard(sc, name, title, beige=False, room=None, fog=0.045, entrances_left=(-10.5, 1.5, 10.5), garages=True):
    """Двор с двумя пятиэтажками по сторонам. Возвращает (материалы, фронт_слева, фронт_справа)."""
    base_level(sc, name, title=title, fog=fog)
    m = Mats(sc, beige)
    courtyard(sc, m, garages=garages)
    left = panel_block(sc, m, "BlockWest", -14, 0, facing=1, room=room, entrances=entrances_left)
    right = panel_block(sc, m, "BlockEast", 14, 0, facing=-1)
    south_gate(sc, m)
    spawns(sc)
    return m, left, right
