class_name Level
extends Node3D
## Общий скрипт уровня: строит навигацию и выпускает участников экспедиции.

@export var player_scene: PackedScene = preload("res://expedition/player.tscn")

@onready var members_root: Node3D = $Members
@onready var _spawn_points: Node3D = $SpawnPoints
@onready var _navigation: NavigationRegion3D = get_node_or_null("NavigationRegion3D")


func _ready() -> void:
	if _navigation:
		_navigation.bake_navigation_mesh(false)
	_spawn_player(1)


func _spawn_player(peer_id: int) -> void:
	var player: Node3D = player_scene.instantiate()
	player.name = str(peer_id)
	player.set_multiplayer_authority(peer_id)
	player.transform = _spawn_transform("Player")
	members_root.add_child(player)


func _spawn_transform(marker_name: String) -> Transform3D:
	var marker: Node3D = _spawn_points.get_node_or_null(marker_name)
	return marker.transform if marker else Transform3D.IDENTITY
