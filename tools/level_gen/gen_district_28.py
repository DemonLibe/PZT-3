import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District28Walls", "Район 28")
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 281)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 282)
warm = sc.sub_res("StandardMaterial3D", albedo_color=C(0.8, 0.72, 0.65), emission_enabled=True,
                  emission=C(0.6, 0.25, 0.15), emission_energy_multiplier=0.3)
panel = sc.sub_res("BoxMesh", material=warm, size=V3(0.06, 1.6, 2.4))
sc.node("Walls", "Node3D", ".")
for i, (x, z) in enumerate(((left + 0.04, -6.0), (left + 0.04, 6.0), (right - 0.04, -4.0), (right - 0.04, 8.0))):
    w = f"Wall{i+1}"
    sc.node(w, "StaticBody3D", "Walls", transform=T(x, 1.3, z), script=sc.ext_res("Script", "res://anomalies/districts/walls/breathing_wall.gd"))
    sc.node("Mesh", "MeshInstance3D", f"Walls/{w}", mesh=panel)
    sc.node("CollisionShape3D", "CollisionShape3D", f"Walls/{w}", shape=sc.sub_res("BoxShape3D", size=V3(0.06, 1.6, 2.4)))
sc.node("BreathingWallsZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/walls/breathing_walls_zone.gd"),
        data=sc.ext_res("Resource", "res://data/walls.tres"), walls_root=NP("../Walls"), glow_material=warm)
zone_shape(sc, "BreathingWallsZone", (18, 6, 44), (0, 3, 0))
survey(sc, 1, (-6.0, 0.1, -9.0))
survey(sc, 2, (6.0, 0.1, 2.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_28_walls.tscn")
