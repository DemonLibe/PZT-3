import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District08Sleep", "Район 8", beige=True, fog=0.055)
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 81, count=6)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 82, count=6)
sc.node("SleepZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/sleep/sleep_zone.gd"),
        data=sc.ext_res("Resource", "res://data/sleep.tres"))
zone_shape(sc, "SleepZone", (18, 6, 44), (0, 3, 0))
survey(sc, 1, (-6.0, 0.1, -14.0))
survey(sc, 2, (6.0, 0.1, -2.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_08_sleep.tscn")
