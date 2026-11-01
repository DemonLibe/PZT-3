import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tscn import *
from level_common import *

def houses_street(sc, length=44.0, house_z=(-12, 0, 12), wall_color=(0.62, 0.6, 0.55)):
    """Улица вдоль Z с домами по обе стороны. Возвращает позиции окон (x, z, yaw)."""
    asphalt = material(sc, (0.18, 0.18, 0.19))
    walk = material(sc, (0.38, 0.37, 0.35))
    wall = material(sc, wall_color)
    roof = material(sc, (0.22, 0.2, 0.22))
    door = material(sc, (0.25, 0.17, 0.12))
    fence = material(sc, (0.3, 0.3, 0.3))
    pole = material(sc, (0.15, 0.15, 0.15))
    box(sc, "Ground", (0, -0.25, 0), (30, 0.5, length + 4), asphalt)
    box(sc, "WalkLeft", (-4.6, 0.05, 0), (1.2, 0.1, length), walk)
    box(sc, "WalkRight", (4.6, 0.05, 0), (1.2, 0.1, length), walk)
    box(sc, "EndNorth", (0, 1.5, -length / 2 - 1), (30, 3, 0.4), fence)
    box(sc, "EndSouth", (0, 1.5, length / 2 + 1), (30, 3, 0.4), fence)
    windows = []
    for side, sx in (("L", -1), ("R", 1)):
        for i, z in enumerate(house_z):
            n = f"House{side}{i+1}"
            box(sc, n, (sx * 8.7, 2.5, z), (7, 5, 7), wall)
            box(sc, n + "Roof", (sx * 8.7, 5.15, z), (7.6, 0.3, 7.6), roof)
            box(sc, n + "Door", (sx * 5.17, 1.0, z + 2.0), (0.06, 2.0, 1.0), door)
            box(sc, n + "Fence", (sx * 5.6, 0.5, z - 3.6), (1.2, 1.0, 0.1), fence)
            windows.append((sx * 5.14, z - 1.0, 90.0 if sx < 0 else -90.0, n))
    for i, (x, z) in enumerate(((-3.6, -15), (3.6, -5), (-3.6, 5), (3.6, 15))):
        street_lamp(sc, i + 1, x, z, pole)
    return windows

def build():
    sc = Scene()
    base_level(sc, "District05Mirror", title="Район 5", fog=0.045)
    exit_door(sc, (0, 0, 21.8), 180)
    windows = houses_street(sc)
    spawn(sc, "Player", (0, 0, 17), 0)
    for i in range(3):
        spawn(sc, f"Npc{i+1}", (-1.5 + 1.5 * i, 0, 19), 0)
    # Окна «Зеркала»
    sc.node("Windows", "Node3D", ".")
    quad = sc.sub_res("QuadMesh", size=V2(1.6, 1.2))
    glass_shape = sc.sub_res("BoxShape3D", size=V3(1.6, 1.2, 0.05))
    frame = material(sc, (0.12, 0.1, 0.09))
    for i, (x, z, yaw, house) in enumerate(windows):
        w = f"MirrorWindow{i+1}"
        sc.node(w, "MeshInstance3D", "Windows", transform=T(x, 1.7, z, yaw=yaw), mesh=quad,
                script=sc.ext_res("Script", "res://anomalies/districts/mirror/mirror_window.gd"))
        sc.node("Glass", "StaticBody3D", f"Windows/{w}")
        sc.node("CollisionShape3D", "CollisionShape3D", f"Windows/{w}/Glass", shape=glass_shape)
        box(sc, f"Frame{i+1}", (x + (0.04 if x > 0 else -0.04), 1.7, z), (0.04, 1.4, 1.8), frame, collision=False)
    # Картинка района с фиксированной точки
    sc.node("MirrorView", "Node3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/mirror/mirror_view.gd"),
            viewport=NP("SubViewport"), camera=NP("SubViewport/Camera3D"))
    sc.node("SubViewport", "SubViewport", "MirrorView", size=Raw("Vector2i(320, 240)"), render_target_update_mode=4)
    sc.node("Camera3D", "Camera3D", "MirrorView/SubViewport", transform=T(1.8, 2.4, -19.5, yaw=180, pitch=-7), current=True, fov=70.0)
    sc.node("MirrorZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/mirror/mirror_zone.gd"),
            data=sc.ext_res("Resource", "res://data/mirror.tres"), view=NP("../MirrorView"), windows_root=NP("../Windows"))
    zone_shape(sc, "MirrorZone", (26, 6, 46), (0, 3, 0))
    ui(sc)
    sc.save(ROOT + "/levels/district_05_mirror.tscn")

if __name__ == "__main__":
    build()
