import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District27Companion", "Район 27", beige=True, room=(6.0, 6.0), entrances_left=(-10.5, -1.5))
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 271)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 272)
apartment(sc, lamp_energy=1.4)
box(sc, "Table", (-12.2, 0.42, 5.5), (1.2, 0.74, 1.8), material(sc, (0.9, 0.85, 0.8), tex="wood_table", scale=1.0))
box(sc, "Cloth", (-12.2, 0.8, 5.5), (1.3, 0.02, 1.9), material(sc, (1, 1, 1), tex="tablecloth", scale=1.2), collision=False)
body = sc.sub_res("CapsuleMesh", material=material(sc, (0.3, 0.3, 0.32), tex="uniform", scale=2.0), radius=0.3, height=1.3)
sc.node("Figure", "StaticBody3D", ".", transform=T(-11.2, 0, 5.5, yaw=-90),
        script=sc.ext_res("Script", "res://anomalies/districts/companion/seated_figure.gd"))
sc.node("Body", "MeshInstance3D", "Figure", transform=T(0, 0.95, 0), mesh=body)
sc.node("CollisionShape3D", "CollisionShape3D", "Figure", transform=T(0, 0.8, 0), shape=sc.sub_res("CapsuleShape3D", radius=0.3, height=1.4))
sc.node("CompanionZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/companion/companion_zone.gd"),
        data=sc.ext_res("Resource", "res://data/companion.tres"), figure=NP("../Figure"))
zone_shape(sc, "CompanionZone", (5.8, 2.8, 5.8), (-11.4, 1.45, 6.0))
survey(sc, 1, (-9.6, 0.11, 3.6))
survey(sc, 2, (6.0, 0.1, -8.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_27_companion.tscn")
