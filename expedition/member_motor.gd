class_name MemberMotor
extends Node
## Двигает тело участника по его намерениям (move_intent, wants_sprint, wants_crouch).
## Работает у владельца тела: у игрока — на его машине, у NPC — на хосте.

@export var member: ExpeditionMember
@export var walk_speed: float = 3.0
@export var run_speed: float = 6.0
@export var crouch_speed: float = 1.5
@export var acceleration: float = 14.0
@export var stand_head_height: float = 1.6
@export var crouch_head_height: float = 1.0
@export var crouch_lerp_speed: float = 8.0
## Ниже этой скорости участник считается стоящим.
@export var idle_speed: float = 0.3

var _gravity: float = 9.8


func _ready() -> void:
	_gravity = ProjectSettings.get_setting("physics/3d/default_gravity", 9.8)


func _physics_process(delta: float) -> void:
	var body: CharacterBody3D = member.get_parent() as CharacterBody3D
	if body == null or not body.is_multiplayer_authority():
		return
	if not body.is_on_floor():
		body.velocity.y -= _gravity * delta
	var active: bool = member.can_act()
	var input: Vector2 = member.move_intent.limit_length(1.0) if active else Vector2.ZERO
	var crouching: bool = active and member.wants_crouch
	var running: bool = active and member.wants_sprint and not crouching and input.length() > 0.1
	var speed: float = walk_speed
	if crouching:
		speed = crouch_speed
	elif running:
		speed = run_speed
	var dir: Vector3 = body.global_basis * Vector3(input.x, 0.0, input.y)
	dir.y = 0.0
	var target: Vector3 = dir.normalized() * input.length() * speed
	var horizontal: Vector3 = Vector3(body.velocity.x, 0.0, body.velocity.z)
	horizontal = horizontal.move_toward(target, acceleration * delta)
	body.velocity.x = horizontal.x
	body.velocity.z = horizontal.z
	body.move_and_slide()
	_update_head(crouching, delta)
	member.motion = _motion_for(horizontal.length(), crouching, running)


func _update_head(crouching: bool, delta: float) -> void:
	if member.head == null:
		return
	var target_y: float = crouch_head_height if crouching else stand_head_height
	member.head.position.y = lerpf(member.head.position.y, target_y, minf(1.0, crouch_lerp_speed * delta))


func _motion_for(speed: float, crouching: bool, running: bool) -> ExpeditionMember.Motion:
	if speed < idle_speed:
		return ExpeditionMember.Motion.IDLE
	if crouching:
		return ExpeditionMember.Motion.CROUCH
	if running:
		return ExpeditionMember.Motion.RUN
	return ExpeditionMember.Motion.WALK
