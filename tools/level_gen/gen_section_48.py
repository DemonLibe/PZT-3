import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section48Convoy", "Гигадом, секция 48")
uniform = sc.sub_res("StandardMaterial3D", albedo_color=C(0.3, 0.33, 0.25))
soldier = sc.sub_res("CapsuleMesh", material=uniform, radius=0.3, height=1.8)
sc.node("Column", "Node3D", ".", transform=T(0, 0, -23))
for i in range(6):
    sc.node(f"Soldier{i+1}", "MeshInstance3D", "Column", transform=T(-0.6 + 1.2 * (i % 2), 0.9, -1.2 * (i // 2)), mesh=soldier)
sc.node("PathStart", "Marker3D", ".", transform=T(0, 0, -23))
sc.node("PathEnd", "Marker3D", ".", transform=T(0, 0, 22))
sc.node("ConvoyZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/convoy/convoy_zone.gd"),
        data=sc.ext_res("Resource", "res://data/convoy.tres"), column=NP("../Column"), path_start=NP("../PathStart"), path_end=NP("../PathEnd"))
zone_shape(sc, "ConvoyZone", (18, 3.5, 44), (0, 1.75, -2))
for i, (x, z) in enumerate(((-6.5, 10.0), (6.5, -10.0), (-6.5, -10.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_48_convoy.tscn")
