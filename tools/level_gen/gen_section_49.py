import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section49Shaft", "Гигадом, секция 49")
pit = sc.sub_res("StandardMaterial3D", shading_mode=0, albedo_color=C(0.0, 0.0, 0.0))
eye = sc.sub_res("StandardMaterial3D", shading_mode=0, albedo_color=C(0.75, 0.7, 0.55))
iris = sc.sub_res("StandardMaterial3D", shading_mode=0, albedo_color=C(0.05, 0.05, 0.05))
sc.node("Shafts", "Node3D", ".")
for i, (x, z) in enumerate(((0.0, 4.0), (-5.5, -10.0), (0.0, -16.0))):
    s = f"Shaft{i+1}"
    sc.node(s, "Node3D", "Shafts", transform=T(x, 0, z))
    sc.node("Pit", "MeshInstance3D", f"Shafts/{s}", transform=T(0, 0.012, 0, pitch=-90), mesh=sc.sub_res("QuadMesh", material=pit, size=V2(1.6, 1.6)))
    sc.node("Eye", "MeshInstance3D", f"Shafts/{s}", transform=T(0, 0.006, 0, pitch=-90), mesh=sc.sub_res("QuadMesh", material=eye, size=V2(0.7, 0.4)))
    sc.node("Iris", "MeshInstance3D", f"Shafts/{s}", transform=T(0, 0.009, 0, pitch=-90), mesh=sc.sub_res("QuadMesh", material=iris, size=V2(0.2, 0.2)))
    for j, (dx, dz) in enumerate(((-0.9, 0), (0.9, 0), (0, -0.9), (0, 0.9))):
        box(sc, f"Rail{i}{j}", (x + dx, 0.5, z + dz), (0.05 if dx else 1.8, 1.0, 1.8 if dx else 0.05), m.metal, collision=False)
sc.node("ShaftZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/shaft/shaft_zone.gd"),
        data=sc.ext_res("Resource", "res://data/shaft.tres"), shafts_root=NP("../Shafts"))
zone_shape(sc, "ShaftZone", (18, 3.5, 44), (0, 1.75, -2))
for i, (x, z) in enumerate(((6.5, 10.0), (6.5, -10.0), (1.0, -21.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_49_shaft.tscn")
