import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District16Lullaby", "Район 16")
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 161, count=6)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 162, count=6)
x, y, z, yaw = window_slot(right, -1, -4.5, floor=1)
sc.node("LullabyWindow", "MeshInstance3D", ".", transform=T(x, y, z, yaw=yaw), mesh=m.glow_quad)
sc.node("Lullaby", "AudioStreamPlayer3D", ".", transform=T(x - 0.5, y, z), unit_size=6.0, volume_db=-2.0,
        stream=sc.ext_res("AudioStream", "res://audio/sfx/lullaby.wav"),
        script=sc.ext_res("Script", "res://anomalies/districts/radio/radio_source.gd"))
sc.node("LullabyZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/lullaby/lullaby_zone.gd"),
        data=sc.ext_res("Resource", "res://data/lullaby.tres"), source=NP("../Lullaby"))
zone_shape(sc, "LullabyZone", (18, 6, 44), (0, 3, 0))
survey(sc, 1, (-6.0, 0.1, -12.0))
survey(sc, 2, (6.0, 0.1, 9.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_16_lullaby.tscn")
