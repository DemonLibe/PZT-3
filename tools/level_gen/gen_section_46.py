import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section46Nurse", "Гигадом, секция 46")
sc.node("Nurse", "MeshInstance3D", ".", transform=T(0, 0.85, -30),
        mesh=sc.sub_res("CapsuleMesh", material=sc.sub_res("StandardMaterial3D", albedo_color=C(0.6, 0.5, 0.45)), radius=0.32, height=1.7))
sc.node("NurseZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/nurse/nurse_zone.gd"),
        data=sc.ext_res("Resource", "res://data/nurse.tres"), nurse=NP("../Nurse"))
zone_shape(sc, "NurseZone", (18, 3.5, 44), (0, 1.75, -2))
for i, (x, z) in enumerate(((-6.5, 10.0), (6.5, 0.0), (-6.5, -10.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_46_nurse.tscn")
