import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section45Silent", "Гигадом, секция 45")
sc.node("Silent", "Node3D", ".", transform=T(0, 0, -22))
sc.node("SilentZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/silent/silent_zone.gd"),
        data=sc.ext_res("Resource", "res://data/silent.tres"), creature=NP("../Silent"))
zone_shape(sc, "SilentZone", (18, 3.5, 44), (0, 1.75, -2))
for i, (x, z) in enumerate(((-6.5, 10.0), (6.5, 0.0), (-6.5, -10.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_45_silent.tscn")
