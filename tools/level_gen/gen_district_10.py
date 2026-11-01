import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District10Kitchen", "Район 10", room=(6.0, 6.0), entrances_left=(-10.5, -1.5))
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 101)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 102)
RX, RZ = -11.4, 6.0
box(sc, "KitchenFloor", (RX, 0.08, RZ), (5.8, 0.06, 5.8), material(sc, (0.7, 0.7, 0.7), tex="sidewalk", scale=1.2))
box(sc, "KitchenTable", (RX + 0.5, 0.4, RZ + 1.0), (1.0, 0.8, 0.8), material(sc, (0.9, 0.85, 0.8), tex="wood_table", scale=1.0))
lamp(sc, "KitchenLamp", (RX, 2.5, RZ), color=(0.9, 0.95, 1.0), energy=1.2, rng=6.0)
fridge_mat = material(sc, (0.95, 0.95, 0.95), tex="metal_clean", scale=0.8)
fridge_mesh = sc.sub_res("BoxMesh", material=fridge_mat, size=V3(0.7, 1.8, 0.7))
fridge_shape = sc.sub_res("BoxShape3D", size=V3(0.7, 1.8, 0.7))
sc.node("Fridges", "Node3D", ".")
for i, z in enumerate((RZ - 2.3, RZ - 1.4)):
    f = f"Fridge{i+1}"
    sc.node(f, "StaticBody3D", "Fridges", transform=T(RX - 2.4, 0.95, z),
            script=sc.ext_res("Script", "res://anomalies/districts/kitchen/fridge.gd"))
    sc.node("Mesh", "MeshInstance3D", f"Fridges/{f}", mesh=fridge_mesh)
    sc.node("CollisionShape3D", "CollisionShape3D", f"Fridges/{f}", shape=fridge_shape)
sc.node("Hum", "AudioStreamPlayer3D", ".", transform=T(RX - 2.4, 1.0, RZ - 1.8), unit_size=2.0, volume_db=-10.0,
        stream=sc.ext_res("AudioStream", "res://audio/sfx/ambient_gigadom.wav"),
        script=sc.ext_res("Script", "res://anomalies/districts/radio/radio_source.gd"))
sc.node("KitchenZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/kitchen/kitchen_zone.gd"),
        data=sc.ext_res("Resource", "res://data/kitchen.tres"), fridges_root=NP("../Fridges"))
zone_shape(sc, "KitchenZone", (5.8, 2.8, 5.8), (RX, 1.45, RZ))
survey(sc, 1, (-12.8, 0.11, 8.2))
survey(sc, 2, (6.0, 0.1, -8.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_10_kitchen.tscn")
