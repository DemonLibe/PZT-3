import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District20Steps", "Район 20", fog=0.05)
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 201, count=5)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 202, count=5)
sc.node("StepsZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/steps/steps_zone.gd"),
        data=sc.ext_res("Resource", "res://data/steps.tres"))
zone_shape(sc, "StepsZone", (18, 6, 44), (0, 3, 0))
survey(sc, 1, (-6.0, 0.1, -8.0))
survey(sc, 2, (6.0, 0.1, -2.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_20_steps.tscn")
