import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District30Nothing", "Район 30", garages=False, exit=False, fog=0.04)
sc.nodes[0][5]["radio_silent"] = True
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 301, count=12)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 302, count=12)
# В глубине двора застройка без шва переходит в бетонный коридор
conc = material(sc, (0.75, 0.75, 0.74), tex="concrete", scale=0.3)
sc.node("Corridor", "CSGCombiner3D", G, transform=T(0, 0, -30), use_collision=True)
sc.node("Shell", "CSGBox3D", f"{G}/Corridor", transform=T(0, 2.0, 0), size=V3(6, 4, 16), material=conc)
sc.node("Hole", "CSGBox3D", f"{G}/Corridor", operation=2, transform=T(0, 1.75, 0.5), size=V3(4, 3.5, 17), material=conc)
lamp(sc, "CorridorLamp", (0, 3.2, -30), color=(0.82, 0.9, 1.0), energy=0.8, rng=8.0)
sc.node("Threshold", "Area3D", ".", transform=T(0, 1.5, -34))
zone_shape(sc, "Threshold", (4, 3, 2))
sc.node("NothingZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/nothing/nothing_zone.gd"),
        data=sc.ext_res("Resource", "res://data/nothing.tres"), threshold=NP("../Threshold"))
zone_shape(sc, "NothingZone", (18, 6, 44), (0, 3, 0))
ui(sc)
sc.save(ROOT + "/levels/district_30_nothing.tscn")
