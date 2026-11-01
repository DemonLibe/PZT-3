import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section43Echo", "Гигадом, секция 43")
chalk = sc.sub_res("StandardMaterial3D", shading_mode=0, albedo_color=C(0.85, 0.85, 0.8))
mark = sc.sub_res("QuadMesh", material=chalk, size=V2(0.4, 0.4))
for i, z in enumerate(range(14, -22, -5)):
    sc.node(f"ChalkMark{i+1}", "MeshInstance3D", ".", transform=T(-1.4, 0.01, z, pitch=-90), mesh=mark)
sc.node("EchoSpots", "Node3D", ".")
for i, (x, z) in enumerate(ROOMS):
    sc.node(f"Spot{i+1}", "Marker3D", "EchoSpots", transform=T(x, 1.5, z))
sc.node("EchoStart", "Marker3D", ".", transform=T(0, 0, 16.5))
sc.node("EchoZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/echo/echo_zone.gd"),
        data=sc.ext_res("Resource", "res://data/echo.tres"), spots_root=NP("../EchoSpots"), start=NP("../EchoStart"))
zone_shape(sc, "EchoZone", (18, 3.5, 44), (0, 1.75, -2))
for i, (x, z) in enumerate(((0.0, 2.0), (0.0, -12.0), (0.0, -21.0))):
    survey(sc, i + 1, (x + 1.2, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_43_echo.tscn")
