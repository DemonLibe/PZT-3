import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District11Silence", "Район 11", fog=0.05)
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 111, count=6)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 112, count=6)
sc.node("SilenceZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/silence/silence_zone.gd"),
        data=sc.ext_res("Resource", "res://data/silence.tres"))
zone_shape(sc, "SilenceZone", (18, 6, 34), (0, 3, -4))
survey(sc, 1, (-6.0, 0.1, -6.0))
survey(sc, 2, (6.0, 0.1, -12.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_11_silence.tscn")
