import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District13Clocks", "Район 13", beige=True)
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 131)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 132)
sc.node("WallClocks", "Node3D", ".")
for i, (x, z, yaw) in enumerate(((left + 0.06, -7.0, 90), (left + 0.06, 4.0, 90), (right - 0.06, -4.0, -90), (right - 0.06, 7.0, -90), (0.0, -16.9, 0))):
    sc.node(f"Clock{i+1}", "Label3D", "WallClocks", transform=T(x, 2.3, z, yaw=yaw), text="22:00", font_size=64,
            modulate=C(0.9, 0.9, 0.8), outline_size=8)
sc.node("ClocksZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/clocks/clocks_zone.gd"),
        data=sc.ext_res("Resource", "res://data/clocks.tres"), wall_clocks_root=NP("../WallClocks"))
zone_shape(sc, "ClocksZone", (18, 6, 34), (0, 3, -4))
survey(sc, 1, (-6.0, 0.1, -7.0))
survey(sc, 2, (6.0, 0.1, -12.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_13_clocks.tscn")
