import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section37Butcher", "Гигадом, секция 37")
RX, RZ = 5.5, -10.0
for i, dz in enumerate((-2.0, -0.7, 0.6, 1.9)):
    cylinder(sc, f"HookChain{i}", (RX + 1.2, 2.9, RZ + dz), 0.02, 1.2, m.metal, collision=False)
    box(sc, f"Hook{i}", (RX + 1.2, 2.25, RZ + dz), (0.05, 0.15, 0.12), m.metal, collision=False)
apron = sc.sub_res("StandardMaterial3D", albedo_color=C(0.5, 0.45, 0.4))
sc.node("Butcher", "Node3D", ".", transform=T(RX + 1.8, 0, RZ, yaw=90))
sc.node("Body", "MeshInstance3D", "Butcher", transform=T(0, 1.1, 0), mesh=sc.sub_res("CapsuleMesh", material=apron, radius=0.5, height=2.2))
sc.node("ButcherZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/butcher/butcher_zone.gd"),
        data=sc.ext_res("Resource", "res://data/butcher.tres"), butcher=NP("../Butcher"))
zone_shape(sc, "ButcherZone", (6, 3.5, 7), (RX, 1.75, RZ))
survey(sc, 1, (RX - 1.5, 0, RZ + 2.5))
survey(sc, 2, (-6.5, 0, 0.0))
survey(sc, 3, (0.0, 0, -21.0))
ui(sc)
sc.save(ROOT + "/levels/section_37_butcher.tscn")
