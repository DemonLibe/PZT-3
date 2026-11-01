"""Секция Гигадома: бетонный коридор вдоль Z, по три комнаты с каждой стороны."""
from tscn import *
from level_common import *

G = "NavigationRegion3D/Geometry"
COLD = (0.82, 0.9, 1.0)
ROOMS = [(-5.5, 10.0), (-5.5, 0.0), (-5.5, -10.0), (5.5, 10.0), (5.5, 0.0), (5.5, -10.0)]


class GMats:
    def __init__(self, sc):
        self.concrete = material(sc, (0.75, 0.75, 0.74), tex="concrete", scale=0.3)
        self.damp = material(sc, (0.7, 0.72, 0.7), tex="concrete_damp", scale=0.4)
        self.floor = material(sc, (0.6, 0.6, 0.6), tex="concrete_floor", scale=0.3)
        self.metal = material(sc, (0.7, 0.7, 0.7), tex="metal_rust", scale=1.0)
        self.grating = material(sc, (0.6, 0.62, 0.6), tex="metal_clean", scale=1.5)


def section_base(sc, name, title, rooms=ROOMS, fog=0.05, corridor_length=44.0):
    base_level(sc, name, title=title, sound="res://audio/sfx/ambient_gigadom.wav", fog=fog,
               bg=(0.015, 0.015, 0.018), ambient=(0.2, 0.21, 0.24), ambient_energy=0.3)
    m = GMats(sc)
    box(sc, "Floor", (0, -0.25, -2), (20, 0.5, 48), m.floor)
    sc.node("Structure", "CSGCombiner3D", G, use_collision=True)
    S = f"{G}/Structure"
    sc.node("Outer", "CSGBox3D", S, transform=T(0, 2, -2), size=V3(18, 4, 46), material=m.concrete)
    sc.node("Corridor", "CSGBox3D", S, operation=2, transform=T(0, 1.75, -2), size=V3(4, 3.5, corridor_length), material=m.concrete)
    for i, (x, z) in enumerate(rooms):
        sc.node(f"Room{i+1}", "CSGBox3D", S, operation=2, transform=T(x, 1.75, z), size=V3(6, 3.5, 7), material=m.damp)
        sc.node(f"Doorway{i+1}", "CSGBox3D", S, operation=2, transform=T(2.25 if x > 0 else -2.25, 1.15, z),
                size=V3(0.9, 2.3, 1.2), material=m.concrete)
        lamp(sc, f"RoomLamp{i+1}", (x, 3.0, z), color=COLD, energy=0.5, rng=6.0)
    for i, z in enumerate(range(16, -24, -8)):
        lamp(sc, f"CorridorLamp{i+1}", (0, 3.2, z), color=COLD, energy=0.8, rng=8.0)
    cylinder(sc, "Pipe", (1.7, 3.2, -2), 0.12, corridor_length, m.metal, collision=False, rot_x=90.0)
    exit_door(sc, (0, 0, 19.7), 180)
    spawn(sc, "Player", (0, 0, 17), 0)
    for i, (x, z) in enumerate(((-1.2, 15.0), (1.2, 15.0), (-1.2, 13.5), (1.2, 13.5), (-1.2, 12.0), (1.2, 12.0))):
        spawn(sc, f"Npc{i+1}", (x, 0, z), 0)
    return m


def observe_zone(sc, data_id, size=(4, 3.5, 44), pos=(0, 1.75, -2)):
    sc.node("ObserveZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/base/observe_zone.gd"),
            data=sc.ext_res("Resource", f"res://data/{data_id}.tres"))
    zone_shape(sc, "ObserveZone", size, pos)
