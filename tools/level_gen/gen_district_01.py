import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District01Dinner", "Район 1", beige=True, room=(6.0, 6.0), fog=0.04,
                               entrances_left=(-10.5, -1.5))
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 11, floors=(1, 2, 3, 4))
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 12, floors=(0, 1, 2, 3, 4), skip=(-10.5, 1.5, 10.5))
# Квартира на первом этаже: накрытый стол
floor_mat = material(sc, (0.85, 0.75, 0.6), tex="wood_table", scale=0.8)
wood = material(sc, (0.9, 0.85, 0.8), tex="wood_table", scale=1.0)
cloth = material(sc, (1.0, 1.0, 1.0), tex="tablecloth", scale=1.2)
wallpaper = material(sc, (0.95, 0.88, 0.75), tex="plaster_warm", scale=0.6)
RX, RZ = -11.4, 6.0
box(sc, "DinnerFloor", (RX, 0.08, RZ), (5.8, 0.06, 5.8), floor_mat)
box(sc, "Wallpaper", (RX - 2.95, 1.45, RZ), (0.04, 2.7, 5.8), wallpaper, collision=False)
box(sc, "Table", (RX, 0.42, RZ - 0.5), (1.2, 0.74, 2.6), wood)
box(sc, "TableCloth", (RX, 0.8, RZ - 0.5), (1.3, 0.02, 2.7), cloth, collision=False)
lamp(sc, "DinnerLamp", (RX, 2.5, RZ - 0.5), color=(1.0, 0.78, 0.5), energy=1.6, rng=6.0, shadow=True)
sc.node("Plates", "Node3D", ".")
plate_mat = sc.sub_res("StandardMaterial3D", albedo_color=C(0.92, 0.9, 0.85))
food_mat = sc.sub_res("StandardMaterial3D", albedo_color=C(0.65, 0.38, 0.18), emission_enabled=True,
                      emission=C(0.35, 0.15, 0.05), emission_energy_multiplier=0.6)
plate_mesh = sc.sub_res("CylinderMesh", material=plate_mat, top_radius=0.16, bottom_radius=0.13, height=0.03)
food_mesh = sc.sub_res("SphereMesh", material=food_mat, radius=0.09, height=0.09)
plate_shape = sc.sub_res("BoxShape3D", size=V3(0.32, 0.14, 0.32))
k = 0
for dz in (-1.04, -0.52, 0.0, 0.52, 1.04):
    for dx in (-0.36, 0.36):
        k += 1
        p = f"Plate{k}"
        sc.node(p, "StaticBody3D", "Plates", transform=T(RX + dx, 0.83, RZ - 0.5 + dz),
                script=sc.ext_res("Script", "res://anomalies/districts/dinner/dinner_food.gd"))
        sc.node("PlateMesh", "MeshInstance3D", f"Plates/{p}", mesh=plate_mesh)
        sc.node("FoodMesh", "MeshInstance3D", f"Plates/{p}", transform=T(0, 0.05, 0), mesh=food_mesh)
        sc.node("CollisionShape3D", "CollisionShape3D", f"Plates/{p}", transform=T(0, 0.05, 0), shape=plate_shape)
sc.node("DinnerZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/dinner/dinner_zone.gd"),
        data=sc.ext_res("Resource", "res://data/dinner.tres"), plates_root=NP("../Plates"))
zone_shape(sc, "DinnerZone", (5.8, 2.8, 5.8), (RX, 1.45, RZ))
survey(sc, 1, (-13.4, 0.11, 8.0))
survey(sc, 2, (6.0, 0.1, -10.0))
survey(sc, 3, (-1.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_01_dinner.tscn")
