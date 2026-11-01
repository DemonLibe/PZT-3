class_name ExpeditionMember
extends Node
## Участник экспедиции: состояние и API, через которые с ним работают аномалии.
## Висит на теле (CharacterBody3D). Не знает, кто им управляет: игрок, NPC или сеть.

signal died(cause: StringName)
signal vanished(cause: StringName)
signal sleeping_changed(value: bool)
signal status_changed(status_id: StringName, active: bool)

enum Motion { IDLE, CROUCH, WALK, RUN }

const PITCH_LIMIT_DEG: float = 85.0
## Если участника будит другой — засчитываем сразу «бесконечно много» нажатий.
const WAKE_BY_OTHER_TAPS: int = 1000000

@export var display_name: String = "Участник"
@export var head: Node3D
@export var flashlight: Light3D

var is_alive: bool = true: set = _set_is_alive
var is_vanished: bool = false: set = _set_is_vanished
var is_sleeping: bool = false: set = _set_is_sleeping
var is_eating: bool = false
var is_alone: bool = false
var gaze_target: Node = null
var gaze_time: float = 0.0
## Имя цели взгляда — для HUD (синхронизируется, в отличие от самого узла).
var gaze_label: String = ""
## Точка, куда упирается взгляд.
var gaze_point: Vector3 = Vector3.ZERO
## Сколько раз участник пытался проснуться (нажатия E во сне).
var wake_taps: int = 0
var noise_level: float = 0.0
var drowsiness: float = 0.0
var panic: float = 0.0
var flashlight_on: bool = false: set = _set_flashlight_on
## id статуса -> true. Скрытые статусы тоже здесь (например, ate_dinner).
var statuses: Dictionary = {}
## Что забрало участника: id аномалии.
var fate_cause: StringName = &""
## Состояние движения — выставляет MemberMotor на стороне владельца тела.
var motion: Motion = Motion.IDLE

# Намерения: заполняет PlayerController или NPCBrain, читает MemberMotor.
var move_intent: Vector2 = Vector2.ZERO
var wants_sprint: bool = false
var wants_crouch: bool = false

@onready var body: CharacterBody3D = get_parent() as CharacterBody3D


## Найти участника на теле (или вернуть null).
static func find_on(node: Node) -> ExpeditionMember:
	if node == null:
		return null
	if node is ExpeditionMember:
		return node
	for child in node.get_children():
		if child is ExpeditionMember:
			return child
	return null


func is_active() -> bool:
	return is_alive and not is_vanished


func can_act() -> bool:
	return is_active() and not is_sleeping


func get_gaze_origin() -> Vector3:
	return head.global_position if head else body.global_position


func get_gaze_direction() -> Vector3:
	var basis_node: Node3D = head if head else body
	return -basis_node.global_basis.z.normalized()


## Попадает ли точка в конус взгляда с полным углом раскрытия angle_deg.
func is_in_view_cone(point: Vector3, angle_deg: float) -> bool:
	var to_point: Vector3 = point - get_gaze_origin()
	if to_point.length_squared() < 0.0001:
		return true
	var angle: float = rad_to_deg(get_gaze_direction().angle_to(to_point.normalized()))
	return angle <= angle_deg * 0.5


## Поворот взгляда: yaw — тело, pitch — голова. Вызывает владелец тела.
func look(yaw_delta: float, pitch_delta: float) -> void:
	if not can_act():
		return
	body.rotate_y(yaw_delta)
	if head:
		var limit: float = deg_to_rad(PITCH_LIMIT_DEG)
		head.rotation.x = clampf(head.rotation.x + pitch_delta, -limit, limit)


func add_panic(amount: float) -> void:
	if NetAuthority.is_authority():
		panic = clampf(panic + amount, 0.0, 1.0)


func add_drowsiness(amount: float) -> void:
	if NetAuthority.is_authority():
		drowsiness = clampf(drowsiness + amount, 0.0, 1.0)


func has_status(status_id: StringName) -> bool:
	return statuses.has(status_id)


func add_status(status_id: StringName) -> void:
	if not NetAuthority.is_authority() or statuses.has(status_id):
		return
	var copy: Dictionary = statuses.duplicate()
	copy[status_id] = true
	statuses = copy
	status_changed.emit(status_id, true)


func remove_status(status_id: StringName) -> void:
	if not NetAuthority.is_authority() or not statuses.has(status_id):
		return
	var copy: Dictionary = statuses.duplicate()
	copy.erase(status_id)
	statuses = copy
	status_changed.emit(status_id, false)


func set_sleeping(value: bool) -> void:
	if NetAuthority.is_authority() and is_active():
		is_sleeping = value


func kill(cause: StringName) -> void:
	if not NetAuthority.is_authority() or not is_active():
		return
	fate_cause = cause
	is_alive = false
	EventBus.member_died.emit(self)


func vanish(cause: StringName) -> void:
	if not NetAuthority.is_authority() or not is_active():
		return
	fate_cause = cause
	is_vanished = true
	EventBus.member_vanished.emit(self)


func _set_is_alive(value: bool) -> void:
	is_alive = value
	if not value:
		_disable_body()
		died.emit(fate_cause)


func _set_is_vanished(value: bool) -> void:
	is_vanished = value
	if value:
		_disable_body()
		body.visible = false
		vanished.emit(fate_cause)


func _set_is_sleeping(value: bool) -> void:
	if is_sleeping == value:
		return
	is_sleeping = value
	wake_taps = 0
	sleeping_changed.emit(value)


func _set_flashlight_on(value: bool) -> void:
	flashlight_on = value
	if flashlight:
		flashlight.visible = value


func _disable_body() -> void:
	move_intent = Vector2.ZERO
	if body:
		body.velocity = Vector3.ZERO
		body.set_collision_layer_value(2, false)
