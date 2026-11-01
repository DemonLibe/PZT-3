class_name NPCNavigator
extends Node
## Ноги и шея напарника: идти к точке по навигации, смотреть на точку.
## Только переводит цели в намерения ExpeditionMember — так же, как игрок мышью и WASD.

@export var member: ExpeditionMember
@export var agent: NavigationAgent3D
## Скорость поворота головы и тела, рад/с.
@export var turn_speed: float = 4.0
@export var arrive_distance: float = 0.6

var _moving: bool = false


func move_to(point: Vector3, run: bool = false) -> void:
	member.wants_sprint = run
	# Не пересчитываем путь, если цель почти не сдвинулась.
	if _moving and agent.target_position.distance_to(point) < 0.3:
		return
	agent.target_position = point
	_moving = true


func stop() -> void:
	_moving = false
	member.move_intent = Vector2.ZERO
	member.wants_sprint = false


func is_moving() -> bool:
	return _moving


## Повернуть взгляд к точке на часть пути за кадр. Возвращает оставшийся угол (рад).
func face(point: Vector3, delta: float, speed_scale: float = 1.0) -> float:
	var to: Vector3 = point - member.get_gaze_origin()
	if to.length_squared() < 0.01:
		return 0.0
	var forward: Vector3 = -member.body.global_basis.z
	var yaw_error: float = forward.signed_angle_to(Vector3(to.x, 0.0, to.z).normalized(), Vector3.UP)
	var pitch_target: float = atan2(to.y, Vector2(to.x, to.z).length())
	var pitch_error: float = pitch_target - member.head.rotation.x
	var step: float = turn_speed * speed_scale * delta
	member.look(clampf(yaw_error, -step, step), clampf(pitch_error, -step, step))
	return absf(yaw_error) + absf(pitch_error)


func _physics_process(delta: float) -> void:
	if not _moving or not NetAuthority.is_authority():
		return
	var body: Node3D = member.body
	if agent.is_navigation_finished() or body.global_position.distance_to(agent.target_position) < arrive_distance:
		stop()
		return
	var next: Vector3 = agent.get_next_path_position()
	var dir: Vector3 = next - body.global_position
	dir.y = 0.0
	if dir.length_squared() < 0.0001:
		dir = agent.target_position - body.global_position
		dir.y = 0.0
	face(body.global_position + dir + Vector3(0, member.head.position.y, 0), delta, 1.5)
	var local: Vector3 = body.global_basis.inverse() * dir.normalized()
	member.move_intent = Vector2(local.x, local.z)
