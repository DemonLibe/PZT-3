import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tscn import *
from level_common import *

sc = Scene()
base_level(sc, "District06Shadow", title="Район 6", fog=0.035, ambient=(0.18, 0.18, 0.22), ambient_energy=0.25)
ground = material(sc, (0.75, 0.75, 0.73), tex="sidewalk", scale=0.5)
wall = material(sc, (0.9, 0.9, 0.9), tex="plaster_grey", scale=0.35)
pole = material(sc, (0.7, 0.7, 0.7), tex="metal_rust", scale=1.0)
box(sc, "Ground", (0, -0.25, 0), (40, 0.5, 40), ground)
for i, (x, z, sx, sz) in enumerate(((0, -16, 32, 6), (0, 16, 32, 6), (-16, 0, 6, 26), (16, 0, 6, 26))):
    box(sc, f"Block{i+1}", (x, 3, z), (sx, 6, sz), wall)
box(sc, "Kiosk", (-6, 1.2, -6), (2.0, 2.4, 1.6), material(sc, (0.6, 0.7, 0.6), tex="metal_clean", scale=1.0))
box(sc, "Bench", (5, 0.25, -7), (2.0, 0.5, 0.6), material(sc, (0.8, 0.75, 0.7), tex="wood_fence", scale=1.0))
for i, (x, z) in enumerate(((-11, -11), (11, 11))):
    street_lamp(sc, i + 1, x, z, pole, energy=0.8)
# Особый источник света: низкий холодный прожектор
sc.node("ShadowLight", "SpotLight3D", ".", transform=T(9, 1.3, 9, yaw=45, pitch=-6),
        light_color=C(0.72, 0.9, 0.78), light_energy=6.0, shadow_enabled=True, spot_range=26.0, spot_angle=40.0)
box(sc, "LightStand", (9, 0.6, 9), (0.4, 1.2, 0.4), pole)
spawn(sc, "Player", (-9, 0, 9), -135)
exit_door(sc, (-12.2, 0, 12.2), 135)
for i in range(3):
    spawn(sc, f"Npc{i+1}", (-11 + i * 1.2, 0, 11), -135)
sc.node("ShadowZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/shadow/shadow_zone.gd"),
        data=sc.ext_res("Resource", "res://data/shadow.tres"), light=NP("../ShadowLight"))
zone_shape(sc, "ShadowZone", (16, 4, 16), (0, 2, 0))
survey(sc, 1, (2.0, 0, -2.0))
survey(sc, 2, (6.0, 0, -9.0))
survey(sc, 3, (-9.0, 0, -4.0))
ui(sc)
sc.save(ROOT + "/levels/district_06_shadow.tscn")
