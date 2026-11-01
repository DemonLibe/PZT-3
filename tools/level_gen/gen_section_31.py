import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section31Shatun", "Гигадом, секция 31")
sc.node("Waypoints", "Node3D", ".")
points = [(0, z) for z in (10, 2, -6, -14, -21)] + list(ROOMS)
for i, (x, z) in enumerate(points):
    sc.node(f"Point{i+1}", "Marker3D", "Waypoints", transform=T(x, 0, z))
sc.node("Shatun", None, ".", instance=sc.ext_res("PackedScene", "res://creatures/shatun/shatun.tscn"),
        transform=T(0, 0, -18), waypoints_root=NP("../Waypoints"))
for i, (x, z) in enumerate(((-6.5, 10.0), (6.5, -10.0), (-6.5, -10.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_31_shatun.tscn")
