import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section44Collector", "Гигадом, секция 44")
for i, (x, z) in enumerate(((-6.8, -12.0), (6.8, 12.0))):
    box(sc, f"Pile{i+1}", (x, 0.3, z), (1.2, 0.6, 1.4), material(sc, (0.6, 0.55, 0.5), tex="cloth_plaid", scale=1.0), collision=False)
sc.node("Collector", "MeshInstance3D", ".", transform=T(0, 1.0, -30),
        mesh=sc.sub_res("CapsuleMesh", material=sc.sub_res("StandardMaterial3D", albedo_color=C(0.3, 0.28, 0.25)), radius=0.35, height=2.0))
sc.node("CollectorZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/collector/collector_zone.gd"),
        data=sc.ext_res("Resource", "res://data/collector.tres"), collector=NP("../Collector"))
zone_shape(sc, "CollectorZone", (18, 3.5, 44), (0, 1.75, -2))
for i, (x, z) in enumerate(((-6.5, 10.0), (6.5, -10.0), (0.0, -21.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_44_collector.tscn")
