import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section41Firemen", "Гигадом, секция 41")
char = sc.sub_res("StandardMaterial3D", albedo_color=C(0.08, 0.06, 0.05), emission_enabled=True, emission=C(0.4, 0.1, 0.02),
                  emission_energy_multiplier=0.4)
sc.node("FigureTemplate", "Node3D", ".", transform=T(0, -10, 0))
sc.node("Body", "MeshInstance3D", "FigureTemplate", transform=T(0, 0.9, 0), mesh=sc.sub_res("CapsuleMesh", material=char, radius=0.3, height=1.8))
sc.node("FireSpawns", "Node3D", ".")
for i, (x, z) in enumerate(((-5.5, 10.0), (5.5, 0.0), (-5.5, -10.0))):
    sc.node(f"Spot{i+1}", "Marker3D", "FireSpawns", transform=T(x, 0, z))
sc.node("FiremenZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/firemen/firemen_zone.gd"),
        data=sc.ext_res("Resource", "res://data/firemen.tres"), spawns_root=NP("../FireSpawns"), figure_template=NP("../FigureTemplate"))
zone_shape(sc, "FiremenZone", (18, 3.5, 44), (0, 1.75, -2))
for i, (x, z) in enumerate(((6.5, 10.0), (-6.5, 0.0), (0.0, -21.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_41_firemen.tscn")
