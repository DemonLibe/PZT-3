import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District02Windows", "Район 2", fog=0.04)
sc.node("Windows", "Node3D", ".")
n = 0
for front, facing, zs in ((left, 1, (-13.5, -7.5, 4.5, 10.5)), (right, -1, (-10.5, -1.5, 7.5, 13.5))):
    for j, wz in enumerate(zs):
        n += 1
        x, y, z, yaw = window_slot(front, facing, wz, floor=1 + (j % 3))
        w = f"LitWindow{n}"
        sc.node(w, "Node3D", "Windows", transform=T(x, y, z, yaw=yaw),
                script=sc.ext_res("Script", "res://anomalies/districts/windows/lit_window.gd"),
                light=NP("Light"), glow=NP("Glow"))
        sc.node("Glow", "MeshInstance3D", f"Windows/{w}", mesh=m.glow_quad)
        sc.node("Light", "OmniLight3D", f"Windows/{w}", transform=T(0, 0, 0.7),
                light_color=C(1.0, 0.8, 0.55), light_energy=0.9, omni_range=5.0)
sc.node("WindowsZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/windows/windows_zone.gd"),
        data=sc.ext_res("Resource", "res://data/windows.tres"), windows_root=NP("../Windows"))
zone_shape(sc, "WindowsZone", (18, 8, 44), (0, 4, 0))
survey(sc, 1, (-6.0, 0.1, -6.0))
survey(sc, 2, (6.0, 0.1, 6.0))
survey(sc, 3, (1.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_02_windows.tscn")
