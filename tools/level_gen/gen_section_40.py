import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section40KeyMaster", "Гигадом, секция 40")
suit = sc.sub_res("StandardMaterial3D", albedo_color=C(0.2, 0.18, 0.16))
sc.node("KeyMaster", "StaticBody3D", ".", transform=T(-7.0, 0, 0.0, yaw=-90),
        script=sc.ext_res("Script", "res://anomalies/gigadom/keymaster/key_master.gd"))
sc.node("Body", "MeshInstance3D", "KeyMaster", transform=T(0, 0.95, 0), mesh=sc.sub_res("CapsuleMesh", material=suit, radius=0.32, height=1.9))
sc.node("Key", "MeshInstance3D", "KeyMaster", transform=T(0.3, 1.1, -0.3),
        mesh=sc.sub_res("BoxMesh", material=sc.sub_res("StandardMaterial3D", albedo_color=C(0.8, 0.7, 0.3), metallic=0.8), size=V3(0.04, 0.12, 0.02)))
sc.node("CollisionShape3D", "CollisionShape3D", "KeyMaster", transform=T(0, 0.95, 0), shape=sc.sub_res("CapsuleShape3D", radius=0.32, height=1.9))
sc.node("KeyMasterZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/keymaster/key_master_zone.gd"),
        data=sc.ext_res("Resource", "res://data/keymaster.tres"), master=NP("../KeyMaster"))
zone_shape(sc, "KeyMasterZone", (6, 3.5, 7), (-5.5, 1.75, 0.0))
for i, (x, z) in enumerate(((6.5, 10.0), (-6.5, -10.0), (0.0, -21.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_40_keymaster.tscn")
