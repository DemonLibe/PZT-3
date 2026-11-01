import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District24Voices", "Район 24", beige=True)
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 241)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 242)
sc.node("RadioVoicesZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/voices/radio_voices_zone.gd"),
        data=sc.ext_res("Resource", "res://data/voices.tres"))
zone_shape(sc, "RadioVoicesZone", (18, 6, 44), (0, 3, 0))
survey(sc, 1, (-6.0, 0.1, -5.0))
survey(sc, 2, (6.0, 0.1, -12.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_24_voices.tscn")
