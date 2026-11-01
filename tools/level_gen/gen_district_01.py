import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tscn import *
from level_common import *
from gen_district_05 import houses_street

sc = Scene()
base_level(sc, "District01Dinner", title="Район 1", fog=0.04)
exit_door(sc, (0, 0, 21.8), 180)
houses_street(sc, house_z=(-12, 12), wall_tex="plaster_warm", wall_color=(1.0, 0.95, 0.9))
standard_spawns(sc)
# Открытый дом с накрытым столом (слева, z = 0)
wall = material(sc, (1.0, 0.95, 0.9), tex="plaster_warm", scale=0.35)
floor_mat = material(sc, (0.95, 0.9, 0.75), tex="tatami", scale=0.6)
wood = material(sc, (0.9, 0.85, 0.8), tex="wood_table", scale=1.0)
cloth = material(sc, (1.0, 1.0, 1.0), tex="tablecloth", scale=1.2)
G = "NavigationRegion3D/Geometry"
sc.node("DinnerHouse", "CSGCombiner3D", G, transform=T(-8.7, 2.0, 0), use_collision=True)
sc.node("Outer", "CSGBox3D", f"{G}/DinnerHouse", size=V3(7, 4, 7), material=wall)
sc.node("Inner", "CSGBox3D", f"{G}/DinnerHouse", operation=2, transform=T(0, 0.05, 0), size=V3(6.6, 3.7, 6.6), material=wall)
sc.node("Doorway", "CSGBox3D", f"{G}/DinnerHouse", operation=2, transform=T(3.4, -0.85, 1.5), size=V3(0.8, 2.3, 1.3), material=wall)
box(sc, "DinnerHouseRoof", (-8.7, 4.15, 0), (7.8, 0.3, 7.8), material(sc, (0.75, 0.8, 0.88), tex="roof", scale=0.5))
box(sc, "DinnerFloor", (-8.7, 0.03, 0), (6.6, 0.06, 6.6), floor_mat)
box(sc, "Table", (-8.7, 0.37, -0.5), (1.8, 0.74, 1.1), wood)
box(sc, "TableCloth", (-8.7, 0.75, -0.5), (1.9, 0.02, 1.2), cloth, collision=False)
lamp(sc, "DinnerLamp", (-8.7, 2.6, -0.5), color=(1.0, 0.78, 0.5), energy=1.6, rng=6.0, shadow=True)
sc.node("Plates", "Node3D", ".")
plate_mat = sc.sub_res("StandardMaterial3D", albedo_color=C(0.92, 0.9, 0.85))
food_mat = sc.sub_res("StandardMaterial3D", albedo_color=C(0.65, 0.38, 0.18), emission_enabled=True,
                      emission=C(0.35, 0.15, 0.05), emission_energy_multiplier=0.6)
plate_mesh = sc.sub_res("CylinderMesh", material=plate_mat, top_radius=0.16, bottom_radius=0.13, height=0.03)
food_mesh = sc.sub_res("SphereMesh", material=food_mat, radius=0.09, height=0.09)
plate_shape = sc.sub_res("BoxShape3D", size=V3(0.32, 0.14, 0.32))
k = 0
for dx in (-0.6, 0.0, 0.6):
    for dz in (-0.32, 0.32):
        k += 1
        p = f"Plate{k}"
        sc.node(p, "StaticBody3D", "Plates", transform=T(-8.7 + dx, 0.78, -0.5 + dz),
                script=sc.ext_res("Script", "res://anomalies/districts/dinner/dinner_food.gd"))
        sc.node("PlateMesh", "MeshInstance3D", f"Plates/{p}", mesh=plate_mesh)
        sc.node("FoodMesh", "MeshInstance3D", f"Plates/{p}", transform=T(0, 0.05, 0), mesh=food_mesh)
        sc.node("CollisionShape3D", "CollisionShape3D", f"Plates/{p}", transform=T(0, 0.05, 0), shape=plate_shape)
sc.node("DinnerZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/dinner/dinner_zone.gd"),
        data=sc.ext_res("Resource", "res://data/dinner.tres"), plates_root=NP("../Plates"))
zone_shape(sc, "DinnerZone", (6.6, 3.6, 6.6), (-8.7, 1.8, 0))
survey(sc, 1, (-11.2, 0.06, 2.4))
survey(sc, 2, (3.3, 0.1, -9.0))
survey(sc, 3, (-1.0, 0, -20.0))
ui(sc)
sc.save(ROOT + "/levels/district_01_dinner.tscn")
