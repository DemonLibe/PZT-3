import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) and os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District06Shadow", "Район 6", fog=0.035)
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 61, count=6)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 62, count=6)
# Особый источник света: низкий холодный прожектор во дворе
sc.node("ShadowLight", "SpotLight3D", ".", transform=T(6.5, 1.3, 8, yaw=45, pitch=-6),
        light_color=C(0.72, 0.9, 0.78), light_energy=6.0, shadow_enabled=True, spot_range=26.0, spot_angle=40.0)
box(sc, "LightStand", (6.5, 0.6, 8), (0.4, 1.2, 0.4), m.metal)
sc.node("ShadowZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/shadow/shadow_zone.gd"),
        data=sc.ext_res("Resource", "res://data/shadow.tres"), light=NP("../ShadowLight"))
zone_shape(sc, "ShadowZone", (14, 4, 16), (0, 2, 0))
survey(sc, 1, (2.0, 0, -2.0))
survey(sc, 2, (5.0, 0, -9.0))
survey(sc, 3, (-5.0, 0, -1.0))
ui(sc)
sc.save(ROOT + "/levels/district_06_shadow.tscn")
