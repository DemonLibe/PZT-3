import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District07Guests", "Район 7")
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 71, count=14)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 72, count=14)
sc.node("Entrances", "Node3D", ".")
for i, z in enumerate((-10.5, 1.5, 10.5)):
    sc.node(f"WestDoor{i+1}", "Marker3D", "Entrances", transform=T(left + 1.2, 0, z))
    sc.node(f"EastDoor{i+1}", "Marker3D", "Entrances", transform=T(right - 1.2, 0, z))
sc.node("GuestsZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/guests/guests_zone.gd"),
        data=sc.ext_res("Resource", "res://data/guests.tres"), entrances_root=NP("../Entrances"))
zone_shape(sc, "GuestsZone", (18, 6, 44), (0, 3, 0))
survey(sc, 1, (-6.0, 0.1, -4.0))
survey(sc, 2, (6.0, 0.1, 6.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_07_guests.tscn")
