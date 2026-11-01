class_name Level
extends Node3D
## Общий скрипт уровня: запускает сессию, строит навигацию и выпускает
## участников экспедиции через MultiplayerSpawner (одинаково в соло и по сети).

const PLAYER_SCENE: PackedScene = preload("res://expedition/player.tscn")
const NPC_SCENE: PackedScene = preload("res://expedition/npc.tscn")
const HOST_NAME: String = "Руководитель"
const NPC_NAMES: PackedStringArray = ["Сато", "Кимура", "Огава"]

## Сколько напарников-NPC выходит в экспедицию.
@export var npc_count: int = 3

@onready var members_root: Node3D = $Members
@onready var _spawner: MultiplayerSpawner = $MemberSpawner
@onready var _spawn_points: Node3D = $SpawnPoints
@onready var _navigation: NavigationRegion3D = get_node_or_null("NavigationRegion3D")


func _ready() -> void:
	_spawner.spawn_function = _spawn_member
	if _navigation:
		# CSG собирает геометрию отложенно — строим навигацию после этого.
		_navigation.bake_navigation_mesh.call_deferred(false)
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
	for i in npc_count:
		var spawn: Transform3D = _spawn_transform("Npc%d" % (i + 1))
		_spawner.spawn({"kind": "npc", "peer": 1, "id": "npc_%d" % (i + 1),
			"name": NPC_NAMES[i % NPC_NAMES.size()], "transform": spawn})


func _spawn_player(peer_id: int) -> void:
	if members_root.has_node(str(peer_id)):
		return
	var index: int = members_root.get_children().filter(func(n: Node) -> bool: return not n.name.begins_with("npc")).size()
	var spawn: Transform3D = _spawn_transform("Player").translated(Vector3(1.2 * index, 0.0, 0.0))
	var display: String = HOST_NAME if peer_id == 1 else "Участник %d" % (index + 1)
	_spawner.spawn({"kind": "player", "peer": peer_id, "name": display, "transform": spawn})


## Вызывается на всех машинах: собирает тело участника по данным от хоста.
func _spawn_member(data: Dictionary) -> Node:
	var is_npc: bool = data["kind"] == "npc"
	var body: Node3D = (NPC_SCENE if is_npc else PLAYER_SCENE).instantiate()
	body.name = String(data["id"]) if is_npc else str(data["peer"])
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
