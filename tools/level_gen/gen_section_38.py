import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section38Mourners", "Гигадом, секция 38")
dress = sc.sub_res("StandardMaterial3D", albedo_color=C(0.12, 0.12, 0.14))
body = sc.sub_res("CapsuleMesh", material=dress, radius=0.28, height=1.7)
sc.node("Mourners", "Node3D", ".")
for i, (x, z) in enumerate(((-6.5, 10.0), (1.4, -6.0), (6.5, -10.0))):
    sc.node(f"Mourner{i+1}", "Node3D", "Mourners", transform=T(x, 0, z, yaw=180))
    sc.node("Body", "MeshInstance3D", f"Mourners/Mourner{i+1}", transform=T(0, 0.85, 0), mesh=body)
sc.node("Weeping", "AudioStreamPlayer3D", ".", transform=T(0, 1.5, -2), unit_size=6.0, volume_db=-10.0, pitch_scale=0.7,
        stream=sc.ext_res("AudioStream", "res://audio/sfx/lullaby.wav"),
        script=sc.ext_res("Script", "res://anomalies/districts/radio/radio_source.gd"))
sc.node("MournersZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/mourners/mourners_zone.gd"),
        data=sc.ext_res("Resource", "res://data/mourners.tres"), mourners_root=NP("../Mourners"))
zone_shape(sc, "MournersZone", (18, 3.5, 44), (0, 1.75, -2))
survey(sc, 1, (6.5, 0, 10.0))
survey(sc, 2, (-6.5, 0, -10.0))
survey(sc, 3, (0.0, 0, -21.0))
ui(sc)
sc.save(ROOT + "/levels/section_38_mourners.tscn")
