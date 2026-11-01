import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section39Grinder", "Гигадом, секция 39")
sc.node("Gratings", "Node3D", ".")
for i, z in enumerate((8.0, -2.0, -14.0)):
    g = f"Grating{i+1}"
    sc.node(g, "MeshInstance3D", "Gratings", transform=T(0, 0.02, z), mesh=sc.sub_res("BoxMesh", material=m.grating, size=V3(4.0, 0.04, 4.0)),
            **{"metadata/half_size": Raw("Vector3(2.0, 0.0, 2.0)")})
sc.node("GrinderZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/grinder/grinder_zone.gd"),
        data=sc.ext_res("Resource", "res://data/grinder.tres"), gratings_root=NP("../Gratings"))
zone_shape(sc, "GrinderZone", (4, 3.5, 44), (0, 1.75, -2))
for i, (x, z) in enumerate(((-6.5, 0.0), (6.5, -10.0), (0.0, -21.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_39_grinder.tscn")
