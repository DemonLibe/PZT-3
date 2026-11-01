import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section34Weaver", "Гигадом, секция 34")
fresh = sc.sub_res("StandardMaterial3D", albedo_color=C(0.95, 0.85, 0.8), emission_enabled=True, emission=C(0.6, 0.5, 0.45),
                   emission_energy_multiplier=0.8, roughness=0.2)
dark = sc.sub_res("StandardMaterial3D", albedo_color=C(0.25, 0.15, 0.12))
strand = sc.sub_res("CylinderMesh", top_radius=0.015, bottom_radius=0.008, height=1.1)
sc.node("Threads", "Node3D", ".")
k = 0
for z in range(14, -22, -3):
    for x in (-1.2, 0.0, 1.2):
        if (z + int(x * 10)) % 2:
            continue
        k += 1
        sc.node(f"Thread{k}", "MeshInstance3D", "Threads", transform=T(x, 2.95, z), mesh=strand)
sc.node("WeaverZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/weaver/weaver_zone.gd"),
        data=sc.ext_res("Resource", "res://data/weaver.tres"), threads_root=NP("../Threads"), fresh_material=fresh, dark_material=dark)
zone_shape(sc, "WeaverZone", (4, 3.5, 44), (0, 1.75, -2))
for i, (x, z) in enumerate(((-6.5, 0.0), (6.5, -10.0), (0.0, -21.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_34_weaver.tscn")
