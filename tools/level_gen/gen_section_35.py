import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section35Choir", "Гигадом, секция 35")
shade = sc.sub_res("StandardMaterial3D", albedo_color=C(0.12, 0.12, 0.14))
singer = sc.sub_res("CapsuleMesh", material=shade, radius=0.3, height=1.8)
sc.node("Circle", "Node3D", ".", transform=T(5.5, 0, -10.0))
import math
for i in range(5):
    a = i * 2 * math.pi / 5
    sc.node(f"Singer{i+1}", "MeshInstance3D", "Circle", transform=T(math.cos(a) * 1.5, 0.9, math.sin(a) * 1.5, yaw=-math.degrees(a) - 90), mesh=singer)
sc.node("Song", "AudioStreamPlayer3D", "Circle", transform=T(0, 1.5, 0), unit_size=5.0, volume_db=-4.0, pitch_scale=1.35,
        stream=sc.ext_res("AudioStream", "res://audio/sfx/lullaby.wav"),
        script=sc.ext_res("Script", "res://anomalies/districts/radio/radio_source.gd"))
sc.node("ChoirZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/choir/choir_zone.gd"),
        data=sc.ext_res("Resource", "res://data/choir.tres"), circle=NP("../Circle"))
zone_shape(sc, "ChoirZone", (18, 3.5, 44), (0, 1.75, -2))
for i, (x, z) in enumerate(((-6.5, 10.0), (-6.5, -10.0), (0.0, -21.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_35_choir.tscn")
