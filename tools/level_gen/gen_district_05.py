import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District05Mirror", "Район 5")
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 5, floors=(1, 2, 3, 4))
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 55, floors=(1, 2, 3, 4))
sc.node("Windows", "Node3D", ".")
quad = sc.sub_res("QuadMesh", size=V2(WIN_W, WIN_H))
glass_shape = sc.sub_res("BoxShape3D", size=V3(WIN_W, WIN_H, 0.05))
slots = [(left, 1, z) for z in (-13.5, -4.5, 7.5)] + [(right, -1, z) for z in (-7.5, 4.5, 13.5)]
for i, (front, facing, wz) in enumerate(slots):
    x, y, z, yaw = window_slot(front, facing, wz)
    w = f"MirrorWindow{i+1}"
    sc.node(w, "MeshInstance3D", "Windows", transform=T(x, y, z, yaw=yaw), mesh=quad,
            script=sc.ext_res("Script", "res://anomalies/districts/mirror/mirror_window.gd"))
    sc.node("Glass", "StaticBody3D", f"Windows/{w}")
    sc.node("CollisionShape3D", "CollisionShape3D", f"Windows/{w}/Glass", shape=glass_shape)
sc.node("MirrorView", "Node3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/mirror/mirror_view.gd"),
        viewport=NP("SubViewport"), camera=NP("SubViewport/Camera3D"))
sc.node("SubViewport", "SubViewport", "MirrorView", size=Raw("Vector2i(320, 240)"), render_target_update_mode=4)
sc.node("Camera3D", "Camera3D", "MirrorView/SubViewport", transform=T(1.5, 3.2, -15.5, yaw=180, pitch=-8), current=True, fov=72.0)
sc.node("MirrorZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/mirror/mirror_zone.gd"),
        data=sc.ext_res("Resource", "res://data/mirror.tres"), view=NP("../MirrorView"), windows_root=NP("../Windows"))
zone_shape(sc, "MirrorZone", (18, 6, 44), (0, 3, 0))
survey(sc, 1, (-6.0, 0.1, -1.0))
survey(sc, 2, (6.0, 0.1, -10.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_05_mirror.tscn")
