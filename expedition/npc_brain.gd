class_name NPCBrain
extends Node
## Поведение напарника: FOLLOW, HOLD, LOOK_AROUND, PANIC.
## Действует только через API ExpeditionMember (через NPCNavigator) — как игрок.

enum State { FOLLOW, HOLD, LOOK_AROUND, PANIC }

## С этими статусами напарник больше не слушает приказов и остаётся на месте.
const DISOBEY_STATUSES: Array[StringName] = [&"lost_purpose", &"nameless"]

@export var member: ExpeditionMember
@export var navigator: NPCNavigator
@export var instincts: NPCInstincts
@export var follow_distance: float = 2.5
@export var run_distance: float = 8.0
@export var panic_enter: float = 0.75
@export var panic_exit: float = 0.5
@export var look_min: float = 1.5
@export var look_max: float = 4.0
## Паника 1.0 удлиняет взгляд на интересное в (1 + это число) раз.
@export var panic_stare_multiplier: float = 5.0
@export var attention_radius: float = 15.0
@export var attention_chance: float = 0.5
@export var repath_interval: float = 0.5

var state: State = State.LOOK_AROUND
var command: StringName = Squad.COMMAND_FOLLOW
var hold_position: Vector3

var _squad: Squad
var _look_point: Vector3
var _look_timer: float = 0.0
var _repath_timer: float = 0.0
var _home_set: bool = false


func _ready() -> void:
	member.auto_doors = true


func _physics_process(delta: float) -> void:
	if not NetAuthority.is_authority():
		return
	if _squad == null:
		_connect_squad()
	if not member.can_act() or member.is_eating:
		navigator.stop()
		return
	_update_state()
	if state != State.PANIC and not _disobeys() and instincts and instincts.act(delta):
		return
	match state:
		State.FOLLOW:
			_do_follow(delta)
		State.HOLD:
			_do_hold(delta)
		State.LOOK_AROUND:
			navigator.stop()
			_do_look_around(delta, 1.0)
		State.PANIC:
			_do_panic(delta)


func _update_state() -> void:
	if _disobeys():
		# Потерял цель или имя: остаётся там, где это случилось, и не слушает приказы.
		if not _home_set:
			_home_set = true
			hold_position = member.body.global_position
		state = State.HOLD if _distance_to(hold_position) > 1.0 else State.LOOK_AROUND
		return
	if member.panic >= panic_enter or (state == State.PANIC and member.panic > panic_exit):
		state = State.PANIC
		return
	var leader: ExpeditionMember = _squad.leader if _squad else null
	if command == Squad.COMMAND_FOLLOW and leader and leader.is_active() and leader != member \
			and _distance_to(leader.body.global_position) > follow_distance:
		state = State.FOLLOW
	elif command == Squad.COMMAND_HOLD and _distance_to(hold_position) > 1.0:
		state = State.HOLD
	else:
		state = State.LOOK_AROUND


func _do_follow(delta: float) -> void:
	_repath_timer -= delta
	if _repath_timer <= 0.0 or not navigator.is_moving():
		_repath_timer = repath_interval
		var target: Vector3 = _squad.leader.body.global_position
		navigator.move_to(target, _distance_to(target) > run_distance)


func _do_hold(delta: float) -> void:
	_repath_timer -= delta
	if _repath_timer <= 0.0 or not navigator.is_moving():
		_repath_timer = repath_interval
		navigator.move_to(hold_position)


func _do_look_around(delta: float, speed_scale: float) -> void:
	_look_timer -= delta
	if _look_timer <= 0.0:
		_pick_look_point()
	navigator.face(_look_point, delta, speed_scale)


func _do_panic(delta: float) -> void:
	# Паника: дёрганые взгляды по сторонам и короткие перебежки.
	if _look_timer <= 0.0 and GameState.rng.randf() < 0.3:
		var offset: Vector3 = Vector3(GameState.rng.randf_range(-4, 4), 0, GameState.rng.randf_range(-4, 4))
		navigator.move_to(member.body.global_position + offset, true)
	if not navigator.is_moving():
		_do_look_around(delta, 3.0)
		_look_timer = minf(_look_timer, GameState.rng.randf_range(0.3, 1.0))


func _pick_look_point() -> void:
	var point: Node3D = _random_attention_point()
	if point and GameState.rng.randf() < attention_chance:
		_look_point = point.global_position
		_look_timer = GameState.rng.randf_range(look_min, look_max) * (1.0 + member.panic * panic_stare_multiplier)
		return
	var yaw: float = member.body.global_rotation.y + GameState.rng.randf_range(-2.0, 2.0)
	var dir: Vector3 = Vector3(-sin(yaw), 0, -cos(yaw))
	_look_point = member.get_gaze_origin() + dir * 5.0 + Vector3(0, GameState.rng.randf_range(-0.8, 0.8), 0)
	_look_timer = GameState.rng.randf_range(look_min, look_max)


func _random_attention_point() -> Node3D:
	var near: Array[Node3D] = []
	for node in get_tree().get_nodes_in_group(&"attention_point"):
		var point: Node3D = node as Node3D
		if point and point.is_visible_in_tree() and _distance_to(point.global_position) < attention_radius:
			near.append(point)
	if near.is_empty():
		return null
	return near[GameState.rng.randi_range(0, near.size() - 1)]


func _distance_to(point: Vector3) -> float:
	return member.body.global_position.distance_to(point)


func _connect_squad() -> void:
	_squad = get_tree().get_first_node_in_group(&"squad") as Squad
	if _squad:
		_squad.command_issued.connect(_on_command)
		command = _squad.last_command


func _on_command(new_command: StringName, _issuer: ExpeditionMember) -> void:
	if _disobeys():
		return
	command = new_command
	if command == Squad.COMMAND_HOLD:
		hold_position = member.body.global_position


func _disobeys() -> bool:
	return DISOBEY_STATUSES.any(func(id: StringName) -> bool: return member.has_status(id))
