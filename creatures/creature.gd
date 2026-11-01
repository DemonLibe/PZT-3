class_name Creature
extends CharacterBody3D
## База существ Гигадома: навигация, состояния, правило из AnomalyData.
## Видит мир только через ExpeditionMember.

signal state_changed(new_state: State)

enum State { IDLE, PATROL, INVESTIGATE, ATTACK }

@export var data: AnomalyData
@export var agent: NavigationAgent3D
@export var turn_speed: float = 5.0
## С какого расстояния участник может «заметить» существо (для Энциклопедии).
@export var observe_distance: float = 18.0

var state: State = State.IDLE: set = _set_state

var _speed: float = 0.0
var _moving: bool = false
var _gravity: float = 9.8
var _observed: Dictionary = {}
var _observe_timer: float = 0.0


func _ready() -> void:
	_gravity = ProjectSettings.get_setting("physics/3d/default_gravity", 9.8)
	add_to_group(&"debug_info")


func _physics_process(delta: float) -> void:
	if not NetAuthority.is_authority():
		return
	_think(delta)
	_move(delta)
	_observe_tick(delta)


## Поведение существа. Переопределяется в наследниках.
func _think(_delta: float) -> void:
	pass


func move_to(point: Vector3, speed: float) -> void:
	agent.target_position = point
	_speed = speed
	_moving = true


func stop() -> void:
	_moving = false


func is_moving() -> bool:
	return _moving


func param(key: String, default: Variant = null) -> Variant:
	return data.param(key, default) if data else default


func punish(member: ExpeditionMember) -> void:
	if data:
		data.punish(member)


## Все живые участники экспедиции на уровне.
func all_members() -> Array[ExpeditionMember]:
	var squad: Squad = get_tree().get_first_node_in_group(&"squad") as Squad
	return squad.active_members() if squad else []


func face_point(point: Vector3, delta: float) -> void:
	var to: Vector3 = point - global_position
	to.y = 0.0
	if to.length_squared() < 0.0001:
		return
	var target_yaw: float = atan2(-to.x, -to.z)
	rotation.y = rotate_toward(rotation.y, target_yaw, turn_speed * delta)


func get_debug_text(_member: ExpeditionMember) -> String:
	return "%s: %s" % [data.display_name if data else name, State.keys()[state]]


func _move(delta: float) -> void:
	if not is_on_floor():
		velocity.y -= _gravity * delta
	var horizontal: Vector3 = Vector3.ZERO
	if _moving:
		if agent.is_navigation_finished():
			_moving = false
		else:
			var next: Vector3 = agent.get_next_path_position()
			var dir: Vector3 = next - global_position
			dir.y = 0.0
			if dir.length_squared() > 0.0001:
				horizontal = dir.normalized() * _speed
				face_point(next, delta)
	velocity.x = horizontal.x
	velocity.z = horizontal.z
	move_and_slide()


## Кто увидел существо впервые — статья откроется частично.
func _observe_tick(delta: float) -> void:
	_observe_timer += delta
	if _observe_timer < 0.5 or data == null:
		return
	_observe_timer = 0.0
	var eye: Vector3 = global_position + Vector3(0, 1.5, 0)
	for member in all_members():
		if _observed.has(member) or not member.can_act():
			continue
		if member.get_gaze_origin().distance_to(eye) < observe_distance and member.is_in_view_cone(eye, 70.0) \
				and _line_of_sight(member.get_gaze_origin(), eye):
			_observed[member] = true
			EventBus.anomaly_observed.emit(member, data.id)


func _line_of_sight(from: Vector3, to: Vector3) -> bool:
	var query: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(from, to, 1 | 4)
	query.exclude = [get_rid()]
	return get_world_3d().direct_space_state.intersect_ray(query).is_empty()


func _set_state(value: State) -> void:
	if state == value:
		return
	state = value
	state_changed.emit(value)
