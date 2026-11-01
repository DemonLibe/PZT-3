import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section47Judge", "Гигадом, секция 47")
sc.node("Judge", "MeshInstance3D", ".", transform=T(0, 1.2, -30),
        mesh=sc.sub_res("CapsuleMesh", material=sc.sub_res("StandardMaterial3D", albedo_color=C(0.05, 0.05, 0.06)), radius=0.4, height=2.4))
sc.node("JudgeZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/judge/judge_zone.gd"),
        data=sc.ext_res("Resource", "res://data/judge.tres"), judge=NP("../Judge"))
zone_shape(sc, "JudgeZone", (18, 3.5, 44), (0, 1.75, -2))
for i, (x, z) in enumerate(((6.5, 10.0), (-6.5, 0.0), (6.5, -10.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_47_judge.tscn")
