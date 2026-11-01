import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from tscn import *
from level_common import *


def houses_street(sc, length=44.0, house_z=(-12, 0, 12), wall_tex="plaster", wall_color=(1.0, 0.97, 0.92)):
    """Улица спального района вдоль Z: двухэтажные дома, заборы, столбы, автомат.
    Возвращает позиции окон первого этажа (x, z, yaw, имя дома)."""
    asphalt = material(sc, (0.5, 0.5, 0.53), tex="asphalt", scale=0.3)
    walk = material(sc, (0.8, 0.8, 0.78), tex="sidewalk", scale=0.6)
    wall = material(sc, wall_color, tex=wall_tex, scale=0.35)
    wall_alt = material(sc, (0.95, 0.95, 0.95), tex="plaster_grey", scale=0.35)
    roof = material(sc, (0.75, 0.8, 0.88), tex="roof", scale=0.5)
    door = material(sc, (0.9, 0.85, 0.8), tex="wood_door", scale=0.9)
    block = material(sc, (0.85, 0.85, 0.83), tex="block_wall", scale=0.7)
    metal = material(sc, (0.75, 0.75, 0.75), tex="metal_rust", scale=1.0)
    pole_mat = material(sc, (0.7, 0.7, 0.68), tex="concrete", scale=1.0)
    glass = material(sc, (0.06, 0.07, 0.09), rough=0.3)
    wire = material(sc, (0.05, 0.05, 0.05))
    vend = material(sc, (0.85, 0.15, 0.12), tex="metal_clean", scale=1.0)
    vend_light = material(sc, (0.9, 0.95, 1.0), emission=(0.8, 0.9, 1.0), energy=1.5)
    box(sc, "Ground", (0, -0.25, 0), (30, 0.5, length + 4), asphalt)
    box(sc, "WalkLeft", (-4.6, 0.05, 0), (1.2, 0.1, length), walk)
    box(sc, "WalkRight", (4.6, 0.05, 0), (1.2, 0.1, length), walk)
    box(sc, "EndNorth", (0, 1.0, -length / 2 - 1), (30, 2, 0.3), block)
    box(sc, "EndSouth", (0, 1.0, length / 2 + 1), (30, 2, 0.3), block)
    windows = []
    k = 0
    for side, sx in (("L", -1), ("R", 1)):
        for i, z in enumerate(house_z):
            k += 1
            n = f"House{side}{i+1}"
            box(sc, n, (sx * 8.7, 3.0, z), (7, 6, 7), wall if k % 2 else wall_alt)
            box(sc, n + "Roof", (sx * 8.7, 6.15, z), (7.8, 0.3, 7.8), roof)
            box(sc, n + "Eave", (sx * 5.0, 3.1, z), (0.6, 0.12, 7.4), roof, collision=False)
            box(sc, n + "Door", (sx * 5.17, 1.0, z + 2.0), (0.06, 2.0, 1.0), door)
            for j, dz in enumerate((-1.8, 1.2)):
                box(sc, f"{n}Upper{j}", (sx * 5.17, 4.4, z + dz), (0.05, 1.0, 1.3), glass, collision=False)
            box(sc, n + "AC", (sx * 5.35, 3.7, z + 2.9), (0.3, 0.55, 0.8), metal, collision=False)
            # бетонный забор в промежутке до следующего дома
            box(sc, n + "Wall", (sx * 5.45, 0.6, z + 6.0), (0.18, 1.2, 4.8), block)
            windows.append((sx * 5.14, z - 1.0, 90.0 if sx < 0 else -90.0, n))
    for i, z in enumerate((-18, -6, 6, 18)):
        for side, x in (("L", -4.05), ("R", 4.05)):
            cylinder(sc, f"Pole{side}{i+1}", (x, 4.0, z), 0.14, 8.0, pole_mat)
            box(sc, f"PoleBar{side}{i+1}", (x, 7.4, z), (1.4, 0.1, 0.1), pole_mat, collision=False)
        x = 4.05 if i % 2 else -4.05
        lamp(sc, f"StreetLamp{i+1}", (x * 0.85, 5.0, z), energy=1.4, rng=11.0)
    for side, x in (("L", -4.05), ("R", 4.05)):
        for dx in (-0.5, 0.5):
            box(sc, f"Wire{side}{dx}", (x + dx, 7.35, 0), (0.02, 0.02, 36.0), wire, collision=False)
    box(sc, "VendingMachine", (4.6, 0.95, -3.0), (0.7, 1.9, 0.9), vend)
    box(sc, "VendingFront", (4.24, 1.2, -3.0), (0.02, 1.0, 0.7), vend_light, collision=False)
    lamp(sc, "VendingGlow", (3.6, 1.3, -3.0), color=(0.8, 0.9, 1.0), energy=0.8, rng=4.0)
    return windows


def build():
    sc = Scene()
    base_level(sc, "District05Mirror", title="Район 5", fog=0.045)
    exit_door(sc, (0, 0, 21.8), 180)
    windows = houses_street(sc)
    standard_spawns(sc)
    sc.node("Windows", "Node3D", ".")
    quad = sc.sub_res("QuadMesh", size=V2(1.6, 1.2))
    glass_shape = sc.sub_res("BoxShape3D", size=V3(1.6, 1.2, 0.05))
    frame = material(sc, (0.8, 0.75, 0.7), tex="wood_door", scale=1.5)
    for i, (x, z, yaw, house) in enumerate(windows):
        w = f"MirrorWindow{i+1}"
        sc.node(w, "MeshInstance3D", "Windows", transform=T(x, 1.7, z, yaw=yaw), mesh=quad,
                script=sc.ext_res("Script", "res://anomalies/districts/mirror/mirror_window.gd"))
        sc.node("Glass", "StaticBody3D", f"Windows/{w}")
        sc.node("CollisionShape3D", "CollisionShape3D", f"Windows/{w}/Glass", shape=glass_shape)
        box(sc, f"Frame{i+1}", (x + (0.04 if x > 0 else -0.04), 1.7, z), (0.04, 1.4, 1.8), frame, collision=False)
    sc.node("MirrorView", "Node3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/mirror/mirror_view.gd"),
            viewport=NP("SubViewport"), camera=NP("SubViewport/Camera3D"))
    sc.node("SubViewport", "SubViewport", "MirrorView", size=Raw("Vector2i(320, 240)"), render_target_update_mode=4)
    sc.node("Camera3D", "Camera3D", "MirrorView/SubViewport", transform=T(1.8, 2.4, -19.5, yaw=180, pitch=-7), current=True, fov=70.0)
    sc.node("MirrorZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/mirror/mirror_zone.gd"),
            data=sc.ext_res("Resource", "res://data/mirror.tres"), view=NP("../MirrorView"), windows_root=NP("../Windows"))
    zone_shape(sc, "MirrorZone", (26, 6, 46), (0, 3, 0))
    survey(sc, 1, (-3.3, 0.1, 6.0))
    survey(sc, 2, (3.3, 0.1, -9.0))
    survey(sc, 3, (-1.0, 0, -20.0))
    ui(sc)
    sc.save(ROOT + "/levels/district_05_mirror.tscn")


if __name__ == "__main__":
    build()
