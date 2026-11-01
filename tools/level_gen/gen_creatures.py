import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tscn import *

def creature(name, script, data, height, radius, mask, parts, color, hum=None, step_interval=0.7):
    sc = Scene()
    sync = sc.sub_res("SceneReplicationConfig", **{
        "properties/0/path": NP(".:position"), "properties/0/spawn": True, "properties/0/replication_mode": 1,
        "properties/1/path": NP(".:rotation"), "properties/1/spawn": True, "properties/1/replication_mode": 1,
        "properties/2/path": NP(".:state"), "properties/2/spawn": True, "properties/2/replication_mode": 2})
    shape = sc.sub_res("CapsuleShape3D", radius=radius, height=height)
    mat = sc.sub_res("StandardMaterial3D", albedo_color=C(*color), roughness=0.9)
    sc.node(name, "CharacterBody3D", None, collision_layer=8, collision_mask=mask,
            script=sc.ext_res("Script", script), data=sc.ext_res("Resource", data), agent=NP("NavigationAgent3D"))
    sc.node("CollisionShape3D", "CollisionShape3D", ".", transform=T(0, height / 2, 0), shape=shape)
    sc.node("Visual", "Node3D", ".")
    for pname, mesh_type, props, pos in parts:
        mesh = sc.sub_res(mesh_type, material=mat, **props)
        sc.node(pname, "MeshInstance3D", "Visual", transform=T(*pos), mesh=mesh)
    sc.node("NavigationAgent3D", "NavigationAgent3D", ".", path_desired_distance=0.7, target_desired_distance=0.7,
            radius=0.5, height=height)
    sc.node("Sync", "MultiplayerSynchronizer", ".", root_path=NP(".."), replication_config=sync)
    props = dict(script=sc.ext_res("Script", "res://audio/creature_audio.gd"), creature=NP(".."), step_interval=step_interval)
    if hum: props["hum"] = sc.ext_res("AudioStream", hum)
    sc.node("CreatureAudio", "Node", ".", **props)
    return sc

fingers = []
for side in (-1, 1):
    for k in range(3):
        fingers.append((f"Finger{'L' if side < 0 else 'R'}{k}", "BoxMesh", {"size": V3(0.025, 0.5, 0.025)},
                        (side * (0.34 + 0.04 * (k - 1)), 0.05, 0.03 * (k - 1))))
cradle_parts = [
    ("Body", "CapsuleMesh", {"radius": 0.22, "height": 2.3}, (0, 1.45, 0)),
    ("Head", "SphereMesh", {"radius": 0.17, "height": 0.36}, (0, 2.75, 0.02)),
    ("ArmL", "BoxMesh", {"size": V3(0.07, 2.1, 0.07)}, (-0.34, 1.3, 0)),
    ("ArmR", "BoxMesh", {"size": V3(0.07, 2.1, 0.07)}, (0.34, 1.3, 0)),
] + fingers
creature("Cradle", "res://creatures/cradle/cradle.gd", "res://data/cradle.tres", 2.9, 0.35, 5,
         cradle_parts, (0.74, 0.71, 0.67), hum="res://audio/sfx/lullaby.wav", step_interval=0.9).save(ROOT + "/creatures/cradle/cradle.tscn")
warden_parts = [
    ("Coat", "CylinderMesh", {"top_radius": 0.24, "bottom_radius": 0.38, "height": 1.6}, (0, 0.8, 0)),
    ("Chest", "CapsuleMesh", {"radius": 0.24, "height": 0.8}, (0, 1.6, 0)),
    ("Head", "SphereMesh", {"radius": 0.15, "height": 0.34}, (0, 2.08, 0)),
]
creature("Warden", "res://creatures/warden/warden.gd", "res://data/warden.tres", 2.2, 0.35, 1,
         warden_parts, (0.28, 0.28, 0.3), step_interval=0.6).save(ROOT + "/creatures/warden/warden.tscn")
