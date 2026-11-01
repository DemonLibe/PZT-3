class_name Level
extends Node3D
## Общий скрипт уровня: запускает сессию, строит навигацию и выпускает
## участников экспедиции через MultiplayerSpawner (одинаково в соло и по сети).

const PLAYER_SCENE: PackedScene = preload("res://expedition/player.tscn")
const HOST_NAME: String = "Руководитель"

@onready var members_root: Node3D = $Members
@onready var _spawner: MultiplayerSpawner = $MemberSpawner
@onready var _spawn_points: Node3D = $SpawnPoints
@onready var _navigation: NavigationRegion3D = get_node_or_null("NavigationRegion3D")


func _ready() -> void:
	_spawner.spawn_function = _spawn_member
	if _navigation:
		_navigation.bake_navigation_mesh(false)
	NetAuthority.session_failed.connect(_on_session_failed)
	NetAuthority.begin_session()
	# Смена сетевого пира сбрасывает спавнер — заново указываем, куда выпускать.
	_spawner.spawn_path = NodePath()
	_spawner.spawn_path = NodePath("../Members")
	if not NetAuthority.is_authority():
		return
	multiplayer.peer_connected.connect(_on_peer_connected)
	multiplayer.peer_disconnected.connect(_on_peer_disconnected)
	_spawn_player(1)
	for peer_id in multiplayer.get_peers():
		_spawn_player(peer_id)


func _spawn_player(peer_id: int) -> void:
	if members_root.has_node(str(peer_id)):
		return
	var index: int = members_root.get_child_count()
	var spawn: Transform3D = _spawn_transform("Player").translated(Vector3(1.2 * index, 0.0, 0.0))
	var display: String = HOST_NAME if peer_id == 1 else "Участник %d" % (index + 1)
	_spawner.spawn({"kind": "player", "peer": peer_id, "name": display, "transform": spawn})


## Вызывается на всех машинах: собирает тело участника по данным от хоста.
func _spawn_member(data: Dictionary) -> Node:
	var body: Node3D = PLAYER_SCENE.instantiate()
	body.name = str(data["peer"])
	body.transform = data["transform"]
	body.set_multiplayer_authority(int(data["peer"]))
	var state_sync: Node = body.get_node_or_null("StateSync")
	if state_sync:
		state_sync.set_multiplayer_authority(1)
	var member: ExpeditionMember = ExpeditionMember.find_on(body)
	member.display_name = data["name"]
	return body


func _spawn_transform(marker_name: String) -> Transform3D:
	var marker: Node3D = _spawn_points.get_node_or_null(marker_name)
	return marker.transform if marker else Transform3D.IDENTITY


func _on_peer_connected(peer_id: int) -> void:
	_spawn_player(peer_id)


func _on_peer_disconnected(peer_id: int) -> void:
	var body: Node = members_root.get_node_or_null(str(peer_id))
	if body:
		body.queue_free()


func _on_session_failed(reason: String) -> void:
	print("[Level] сессия прервана: ", reason)
	get_tree().change_scene_to_file.call_deferred("res://debug/net_menu.tscn")
