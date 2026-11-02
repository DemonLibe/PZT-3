import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tscn import *
from level_common import *

COLD = (0.82, 0.9, 1.0)
G = "NavigationRegion3D/Geometry"

def section_32():
    sc = Scene()
    base_level(sc, "Section32Cradle", title="Гигадом, секция 32", sound="res://audio/sfx/ambient_gigadom.wav", fog=0.06, bg=(0.015, 0.015, 0.018), ambient=(0.2, 0.21, 0.24), ambient_energy=0.3)
    concrete = material(sc, (0.75, 0.75, 0.74), tex="concrete", scale=0.3)
    dark = material(sc, (0.7, 0.72, 0.7), tex="concrete_damp", scale=0.4)
    floor_mat = material(sc, (0.6, 0.6, 0.6), tex="concrete_floor", scale=0.3)
    pipe = material(sc, (0.7, 0.7, 0.7), tex="metal_rust", scale=1.0)
    box(sc, "Floor", (0, -0.25, 0), (40, 0.5, 40), floor_mat)
    box(sc, "Ceiling", (0, 6.25, 0), (40, 0.5, 40), dark)
    # Стены зала с проходами по центру юга и севера (туда примыкают лабиринты)
    for i, (x, z, sx, sz) in enumerate(((-11.0, -20.25, 18, 0.5), (11.0, -20.25, 18, 0.5), (-11.0, 20.25, 18, 0.5),
                                        (11.0, 20.25, 18, 0.5), (-20.25, 0, 0.5, 40), (20.25, 0, 0.5, 40))):
        box(sc, f"Wall{i+1}", (x, 3, z), (sx, 6, sz), concrete)
    for i, z in enumerate((-20.25, 20.25)):
        box(sc, f"Lintel{i+1}", (0, 4.75, z), (4, 2.5, 0.5), concrete)
    k = 0
    for x in (-12, -4, 4, 12):
        for z in (-12, -4, 4, 12):
            k += 1
            box(sc, f"Pillar{k}", (x, 3, z), (1.2, 6, 1.2), dark)
    box(sc, "Crate", (7, 0.4, 15), (1.4, 0.8, 1.0), material(sc, (0.85, 0.8, 0.7), tex="wood_fence", scale=1.0))
    for i, x in enumerate((-19.6, 19.6)):
        cylinder(sc, f"Pipe{i+1}", (x, 4.8, 0), 0.25, 40.0, pipe, collision=False, rot_x=90.0)
        cylinder(sc, f"PipeB{i+1}", (x, 5.4, 0), 0.12, 40.0, pipe, collision=False, rot_x=90.0)
    food = sc.ext_res("PackedScene", "res://world/food_item.tscn")
    for i, dx in enumerate((-0.35, 0.35)):
        sc.node(f"Food{i+1}", None, ".", instance=food, transform=T(7 + dx, 0.8, 15))
    for i, (x, z) in enumerate(((-8, 8), (8, 0), (-8, -8), (8, -14), (0, 16))):
        lamp(sc, f"Fluorescent{i+1}", (x, 5.6, z), color=COLD, energy=0.9, rng=11.0)
    from route import gigadom_maze, props_root
    props_root(sc)
    gigadom_maze(sc, None, "South", (0, 22.5), "S", 15, 3201, end="spawn")
    gigadom_maze(sc, None, "North", (0, -22.5), "N", 13, 3202, end="exit")
    survey(sc, 1, (-12.0, 0, -8.0))
    survey(sc, 2, (12.0, 0, -8.0))
    survey(sc, 3, (0.0, 0, -18.0))
    sc.node("Cradle", None, ".", instance=sc.ext_res("PackedScene", "res://creatures/cradle/cradle.tscn"), transform=T(0, 0, -15))
    ui(sc)
    sc.save(ROOT + "/levels/section_32_cradle.tscn")

def section_36():
    sc = Scene()
    base_level(sc, "Section36Warden", title="Гигадом, секция 36", sound="res://audio/sfx/ambient_gigadom.wav", fog=0.05, bg=(0.015, 0.015, 0.018), ambient=(0.2, 0.21, 0.24), ambient_energy=0.3)
    concrete = material(sc, (0.75, 0.75, 0.74), tex="concrete", scale=0.3)
    room_floor = material(sc, (0.7, 0.72, 0.7), tex="concrete_damp", scale=0.4)
    pipe = material(sc, (0.7, 0.7, 0.7), tex="metal_rust", scale=1.0)
    box(sc, "Floor", (0, -0.25, -3), (36, 0.5, 13), material(sc, (0.6, 0.6, 0.6), tex="concrete_floor", scale=0.3))
    cylinder(sc, "CorridorPipe", (0, 3.3, 1.2), 0.15, 33.0, pipe, collision=False, rot_x=90.0, yaw=90.0)
    sc.node("Structure", "CSGCombiner3D", G, use_collision=True)
    S = f"{G}/Structure"
    sc.node("Outer", "CSGBox3D", S, transform=T(0, 2, -3.25), size=V3(34, 4, 10.5), material=concrete)
    sc.node("Corridor", "CSGBox3D", S, operation=2, transform=T(0, 1.8, 0), size=V3(35, 3.6, 3), material=concrete)
    rooms_x = (-12, -4, 4, 12)
    for i, x in enumerate(rooms_x):
        sc.node(f"RoomHole{i+1}", "CSGBox3D", S, operation=2, transform=T(x, 1.8, -5), size=V3(7, 3.6, 6), material=room_floor)
        sc.node(f"Doorway{i+1}", "CSGBox3D", S, operation=2, transform=T(x, 1.15, -1.75), size=V3(1.2, 2.3, 0.8), material=concrete)
    door = sc.ext_res("PackedScene", "res://world/door.tscn")
    warden_data = sc.ext_res("Resource", "res://data/warden.tres")
    sc.node("Rooms", "Node3D", ".")
    for i, x in enumerate(rooms_x):
        r = f"Room{i+1}"
        sc.node(f"Door{i+1}", None, ".", instance=door, transform=T(x, 0, -1.75), forget_data=warden_data)
        sc.node(f"CheckPoint{i+1}", "Marker3D", ".", transform=T(x, 0, 0.5))
        sc.node(r, "Area3D", "Rooms", script=sc.ext_res("Script", "res://anomalies/gigadom/warden/warden_room.gd"),
                door=NP(f"../../Door{i+1}"), check_point=NP(f"../../CheckPoint{i+1}"))
        zone_shape(sc, f"Rooms/{r}", (7, 3.6, 6), (x, 1.8, -5))
        lamp(sc, f"RoomLamp{i+1}", (x, 3.2, -5), color=COLD, energy=0.6, rng=6.0)
    for i, x in enumerate((-14, -7, 0, 7, 14)):
        lamp(sc, f"CorridorLamp{i+1}", (x, 3.3, 0), color=COLD, energy=0.8, rng=7.0)
    curve = sc.sub_res("Curve3D", _data=Raw('{\n"points": PackedVector3Array(0, 0, 0, 0, 0, 0, -15.5, 0, 0.6, 0, 0, 0, 0, 0, 0, 15.5, 0, 0.6, 0, 0, 0, 0, 0, 0, -15.5, 0, 0.55),\n"tilts": PackedFloat32Array(0, 0, 0)\n}'), point_count=3)
    sc.node("WardenPath", "Path3D", ".", curve=curve)
    for i, x in enumerate((-12, -4, 4)):
        survey(sc, i + 1, (x - 2.5, 0, -6.8))
    sc.node("Warden", None, ".", instance=sc.ext_res("PackedScene", "res://creatures/warden/warden.tscn"),
            transform=T(-15.5, 0, 0.6), path=NP("../WardenPath"), rooms_root=NP("../Rooms"))
    from route import gigadom_maze, props_root
    props_root(sc)
    gigadom_maze(sc, None, "West", (-19.0, 0), "W", 14, 3601, end="spawn")
    gigadom_maze(sc, None, "East", (19.0, 0), "E", 12, 3602, end="exit")
    ui(sc)
    sc.save(ROOT + "/levels/section_36_warden.tscn")

section_32()
section_36()
