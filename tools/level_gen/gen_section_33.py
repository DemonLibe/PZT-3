import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section33Barracks", "Гигадом, секция 33")
box(sc, "RadioBox", (6.5, 1.2, 0.0), (0.6, 0.5, 0.4), m.metal, collision=False)
rot = sc.sub_res("StandardMaterial3D", albedo_color=C(0.35, 0.42, 0.3))
sc.node("Prapor", "Node3D", ".", transform=T(0, 0, -22))
sc.node("Body", "MeshInstance3D", "Prapor", transform=T(0, 0.95, 0), mesh=sc.sub_res("CapsuleMesh", material=rot, radius=0.32, height=1.9))
sc.node("Cap", "MeshInstance3D", "Prapor", transform=T(0, 1.95, 0), mesh=sc.sub_res("CylinderMesh", material=rot, top_radius=0.22, bottom_radius=0.18, height=0.1))
sc.node("PraporStart", "Marker3D", ".", transform=T(0, 0, -22))
sc.node("BarracksZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/barracks/barracks_zone.gd"),
        data=sc.ext_res("Resource", "res://data/barracks.tres"), prapor=NP("../Prapor"), prapor_start=NP("../PraporStart"))
zone_shape(sc, "BarracksZone", (18, 3.5, 44), (0, 1.75, -2))
for i, (x, z) in enumerate(((-6.5, 10.0), (6.5, 0.0), (-6.5, -10.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_33_barracks.tscn")
