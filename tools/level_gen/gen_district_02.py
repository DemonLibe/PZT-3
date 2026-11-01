import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tscn import *
from level_common import *
from gen_district_05 import houses_street

sc = Scene()
base_level(sc, "District02Windows", title="Район 2", fog=0.04)
exit_door(sc, (0, 0, 21.8), 180)
houses = houses_street(sc, wall_tex="plaster_grey", wall_color=(0.85, 0.88, 0.95))
standard_spawns(sc)
sc.node("Windows", "Node3D", ".")
glow_mat = sc.sub_res("StandardMaterial3D", shading_mode=0, albedo_color=C(1.0, 0.82, 0.5))
quad = sc.sub_res("QuadMesh", material=glow_mat, size=V2(1.1, 0.9))
n = 0
for (x, z, yaw, house) in houses:
    for dz in (-1.2, 1.6):
        n += 1
        w = f"LitWindow{n}"
        sc.node(w, "Node3D", "Windows", transform=T(x, 4.4, z + 1.0 + dz, yaw=yaw),
                script=sc.ext_res("Script", "res://anomalies/districts/windows/lit_window.gd"),
                light=NP("Light"), glow=NP("Glow"))
        sc.node("Glow", "MeshInstance3D", f"Windows/{w}", mesh=quad)
        sc.node("Light", "OmniLight3D", f"Windows/{w}", transform=T(0, 0, 0.6),
                light_color=C(1.0, 0.8, 0.55), light_energy=0.9, omni_range=5.0)
sc.node("WindowsZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/windows/windows_zone.gd"),
        data=sc.ext_res("Resource", "res://data/windows.tres"), windows_root=NP("../Windows"))
zone_shape(sc, "WindowsZone", (26, 8, 46), (0, 4, 0))
survey(sc, 1, (-3.3, 0.1, -6.0))
survey(sc, 2, (3.3, 0.1, 9.0))
survey(sc, 3, (1.0, 0, -20.0))
ui(sc)
sc.save(ROOT + "/levels/district_02_windows.tscn")
