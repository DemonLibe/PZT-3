import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District21Door", "Район 21", room=(6.0, 6.0), entrances_left=(-10.5, -1.5))
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 211, count=6)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 212, count=6)
apartment(sc, lamp_energy=0.8)
dark = sc.sub_res("StandardMaterial3D", shading_mode=0, albedo_color=C(0, 0, 0))
box(sc, "DoorFrame", (-14.35, 1.1, 6.0), (0.12, 2.3, 1.3), material(sc, (0.6, 0.5, 0.4), tex="wood_door", scale=1.0), collision=False)
sc.node("Darkness", "MeshInstance3D", ".", transform=T(-14.6, 1.1, 6.0), mesh=sc.sub_res("BoxMesh", material=dark, size=V3(0.4, 2.2, 1.1)))
leaf_mesh = sc.sub_res("BoxMesh", material=material(sc, (0.7, 0.55, 0.42), tex="wood_door", scale=1.0), size=V3(0.05, 2.1, 1.0))
sc.node("GapDoor", "StaticBody3D", ".", transform=T(-14.3, 0, 6.0), leaf=NP("Hinge"),
        script=sc.ext_res("Script", "res://anomalies/districts/door/gap_door.gd"))
sc.node("Hinge", "Node3D", "GapDoor", transform=T(0, 0, -0.5))
sc.node("Leaf", "MeshInstance3D", "GapDoor/Hinge", transform=T(0, 1.05, 0.5), mesh=leaf_mesh)
sc.node("CollisionShape3D", "CollisionShape3D", "GapDoor", transform=T(0, 1.05, 0), shape=sc.sub_res("BoxShape3D", size=V3(0.1, 2.1, 1.0)))
sc.node("DoorGapZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/door/door_gap_zone.gd"),
        data=sc.ext_res("Resource", "res://data/door.tres"), door=NP("../GapDoor"))
zone_shape(sc, "DoorGapZone", (5.8, 2.8, 5.8), (-11.4, 1.45, 6.0))
survey(sc, 1, (-9.6, 0.11, 8.3))
survey(sc, 2, (6.0, 0.1, -8.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_21_door.tscn")
