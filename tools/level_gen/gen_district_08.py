import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tscn import *
from level_common import *
from gen_district_05 import houses_street

sc = Scene()
base_level(sc, "District08Sleep", title="Район 8", fog=0.055, ambient=(0.22, 0.24, 0.3))
houses_street(sc, wall_tex="plaster_grey", wall_color=(0.8, 0.82, 0.9))
standard_spawns(sc)
exit_door(sc, (0, 0, 21.8), 180)
bench = material(sc, (0.8, 0.75, 0.7), tex="wood_fence", scale=1.0)
for i, z in enumerate((-8, 4)):
    box(sc, f"Bench{i+1}", (3.7, 0.25, z), (0.6, 0.5, 2.0), bench)
sc.node("SleepZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/sleep/sleep_zone.gd"),
        data=sc.ext_res("Resource", "res://data/sleep.tres"))
zone_shape(sc, "SleepZone", (26, 6, 46), (0, 3, 0))
survey(sc, 1, (-3.3, 0.1, -14.0))
survey(sc, 2, (3.3, 0.1, -2.0))
survey(sc, 3, (0.0, 0, -20.0))
ui(sc)
sc.save(ROOT + "/levels/district_08_sleep.tscn")
