import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District03Radio", "Район 3")
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 31)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 32)
radio_mat = material(sc, (0.55, 0.4, 0.3), tex="wood_table", scale=2.0)
radio_mesh = sc.sub_res("BoxMesh", material=radio_mat, size=V3(0.45, 0.28, 0.2))
static = sc.ext_res("AudioStream", "res://audio/sfx/radio_static.wav")
sc.node("Radios", "Node3D", ".")
for i, (x, z) in enumerate(((-6.4, -8.3), (6.4, 3.7), (-6.4, 3.7), (6.4, -8.3))):
    r = f"Radio{i+1}"
    sc.node(r, "Node3D", "Radios", transform=T(x, 0.64, z, yaw=90 if x < 0 else -90))
    sc.node("Mesh", "MeshInstance3D", f"Radios/{r}", mesh=radio_mesh)
    sc.node("Sound", "AudioStreamPlayer3D", f"Radios/{r}", stream=static, unit_size=2.5, volume_db=-6.0,
            script=sc.ext_res("Script", "res://anomalies/districts/radio/radio_source.gd"))
sc.node("RadioZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/radio/radio_zone.gd"),
        data=sc.ext_res("Resource", "res://data/radio.tres"), radios_root=NP("../Radios"))
zone_shape(sc, "RadioZone", (18, 6, 44), (0, 3, 0))
survey(sc, 1, (-6.0, 0.1, -3.0))
survey(sc, 2, (6.0, 0.1, -12.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_03_radio.tscn")
