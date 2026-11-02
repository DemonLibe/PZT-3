import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District12Reflection", "Район 12", fog=0.022, garages=False, north=False)
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 121)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 122)
# Пустырь на север: там видно «отражение»
box(sc, "NorthLot", (0, -0.25, -55), (60, 0.5, 50), material(sc, (0.55, 0.5, 0.42), tex="concrete_floor", scale=0.25))
for i, z in enumerate((-40, -60)):
    lamp(sc, f"LotLamp{i+1}", (0, 5.0, z), color=(1.0, 0.85, 0.6), energy=1.5, rng=18.0)
sc.node("ReflectionZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/reflection/reflection_zone.gd"),
        data=sc.ext_res("Resource", "res://data/reflection.tres"))
zone_shape(sc, "ReflectionZone", (18, 6, 44), (0, 3, 0))
survey(sc, 1, (-6.0, 0.1, -4.0))
survey(sc, 2, (6.0, 0.1, 4.0))
survey(sc, 3, (0.0, 0, -17.0))
ui(sc)
sc.save(ROOT + "/levels/district_12_reflection.tscn")
