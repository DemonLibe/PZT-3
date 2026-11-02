"""Общие куски уровней: окружение, улица, дома, фонари, точки появления."""
from tscn import *

def base_level(sc, name, title="Район", sound="res://audio/sfx/ambient_district.wav", fog=0.05, bg=(0.02, 0.02, 0.03), ambient=(0.25, 0.25, 0.3), ambient_energy=0.35):
    sc.node(name, "Node3D", script=sc.ext_res("Script", "res://levels/level.gd"), title=title)
    env = sc.sub_res("Environment", background_mode=1, background_color=C(*bg),
        ambient_light_source=2, ambient_light_color=C(*ambient), ambient_light_energy=ambient_energy,
        fog_enabled=True, fog_light_color=C(bg[0]*2, bg[1]*2, bg[2]*2.5), fog_density=fog)
    sc.node("WorldEnvironment", "WorldEnvironment", ".", environment=env)
    navmesh = sc.sub_res("NavigationMesh", geometry_parsed_geometry_type=1, geometry_collision_mask=1,
        agent_radius=0.25, agent_height=2.0, agent_max_climb=0.25, cell_size=0.25, cell_height=0.25)
    sc.node("NavigationRegion3D", "NavigationRegion3D", ".", navigation_mesh=navmesh)
    sc.node("Geometry", "Node3D", "NavigationRegion3D")
    sc.node("Ambience", "AudioStreamPlayer", ".", script=sc.ext_res("Script", "res://audio/ambience.gd"),
            stream=sc.ext_res("AudioStream", sound), volume_db=-8.0)
    sc.node("SpawnPoints", "Node3D", ".")
    sc.node("Members", "Node3D", ".")
    sc.node("MemberSpawner", "MultiplayerSpawner", ".", spawn_path=NP("../Members"))
    sc.node("Squad", "Node", ".", script=sc.ext_res("Script", "res://expedition/squad.gd"), members_root=NP("../Members"))

def material(sc, color, rough=1.0, emission=None, energy=1.0, tex=None, scale=0.5):
    """Материал; tex — имя текстуры из world/textures (накладывается по мировым координатам)."""
    props = dict(albedo_color=C(*color), roughness=rough)
    if tex:
        props.update(albedo_texture=sc.ext_res("Texture2D", f"res://world/textures/{tex}.png"),
                     texture_filter=2, uv1_scale=V3(scale, scale, scale), uv1_triplanar=True, uv1_world_triplanar=True)
    if emission:
        props.update(emission_enabled=True, emission=C(*emission), emission_energy_multiplier=energy)
    return sc.sub_res("StandardMaterial3D", **props)

def box(sc, name, pos, size, mat, parent="NavigationRegion3D/Geometry", yaw=0.0, collision=True):
    sc.node(name, "CSGBox3D", parent, transform=T(*pos, yaw=yaw), use_collision=collision,
            size=V3(*size), material=mat)

def spawn(sc, name, pos, yaw=0.0):
    sc.node(name, "Marker3D", "SpawnPoints", transform=T(*pos, yaw=yaw))

def lamp(sc, name, pos, color=(1.0, 0.85, 0.6), energy=1.2, rng=9.0, shadow=False, parent="."):
    props = dict(transform=T(*pos), light_color=C(*color), light_energy=energy, omni_range=rng)
    if shadow: props["shadow_enabled"] = True
    sc.node(name, "OmniLight3D", parent, **props)

def street_lamp(sc, idx, x, z, pole_mat, energy=1.4):
    box(sc, f"LampPole{idx}", (x, 2.0, z), (0.12, 4.0, 0.12), pole_mat)
    lamp(sc, f"StreetLamp{idx}", (x, 3.9, z), energy=energy, rng=10.0)

def exit_door(sc, pos, yaw):
    sc.node("ExitDoor", None, ".", instance=sc.ext_res("PackedScene", "res://world/exit_door.tscn"), transform=T(*pos, yaw=yaw))

def ui(sc):
    sc.node("HUD", None, ".", instance=sc.ext_res("PackedScene", "res://ui/hud.tscn"))
    sc.node("PauseMenu", None, ".", instance=sc.ext_res("PackedScene", "res://ui/pause_menu.tscn"))
    sc.node("FateOverlay", None, ".", instance=sc.ext_res("PackedScene", "res://ui/fate_overlay.tscn"))
    sc.node("SleepOverlay", None, ".", instance=sc.ext_res("PackedScene", "res://ui/sleep_overlay.tscn"))
    sc.node("DebugHUD", None, ".", instance=sc.ext_res("PackedScene", "res://debug/debug_hud.tscn"))

def zone_shape(sc, parent, size, pos=(0, 0, 0)):
    shape = sc.sub_res("BoxShape3D", size=V3(*size))
    sc.node("CollisionShape3D", "CollisionShape3D", parent, transform=T(*pos), shape=shape)

def standard_spawns(sc, z=17.0):
    spawn(sc, "Player", (0, 0, z), 0)
    for i in range(3):
        spawn(sc, f"Npc{i+1}", (-1.5 + 1.5 * i, 0, z + 2), 0)

def cylinder(sc, name, pos, radius, height, mat, parent="NavigationRegion3D/Geometry", collision=True, rot_x=0.0, yaw=0.0):
    sc.node(name, "CSGCylinder3D", parent, transform=T(*pos, yaw=yaw, pitch=rot_x), use_collision=collision,
            radius=radius, height=height, sides=8, material=mat)

def survey(sc, idx, pos, yaw=0.0):
    """Точка замера — цель вылазки."""
    if idx == 1:
        sc.node("SurveyPoints", "Node3D", ".")
    sc.node(f"SurveyPoint{idx}", None, "SurveyPoints",
            instance=sc.ext_res("PackedScene", "res://world/survey_point.tscn"), transform=T(*pos, yaw=yaw))
