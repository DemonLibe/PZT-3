class_name MirrorView
extends Node3D
## Картинка «Зеркала»: SubViewport с камерой в фиксированной точке района.
## В фазе мимикрии камера повторяет движения наблюдателя с задержкой.

@export var viewport: SubViewport
@export var camera: Camera3D

## За кем повторяет камера (null — стоит на месте).
var mimic_member: ExpeditionMember
var mimic_delay: float = 0.5

var _base_transform: Transform3D
var _start_position: Vector3
var _start_yaw: float = 0.0
var _buffer: Array[Dictionary] = []
var _clock: float = 0.0


func _ready() -> void:
	_base_transform = camera.global_transform


func _process(delta: float) -> void:
	_clock += delta
	if mimic_member == null or not is_instance_valid(mimic_member):
		camera.global_transform = _base_transform
		return
	var body: Node3D = mimic_member.get_parent() as Node3D
	_buffer.append({"t": _clock, "pos": body.global_position, "yaw": body.global_rotation.y})
	var delayed: Dictionary = _buffer[0]
	while _buffer.size() > 1 and _buffer[1]["t"] <= _clock - mimic_delay:
		_buffer.pop_front()
		delayed = _buffer[0]
	var offset: Vector3 = delayed["pos"] - _start_position
	var yaw: float = float(delayed["yaw"]) - _start_yaw
	var moved: Transform3D = _base_transform.translated(offset)
	camera.global_transform = Transform3D(moved.basis.rotated(Vector3.UP, yaw), moved.origin)


func get_texture() -> Texture2D:
	return viewport.get_texture()


func set_mimic(member: ExpeditionMember, delay: float) -> void:
	if member == mimic_member:
		return
	mimic_member = member
	mimic_delay = delay
	_buffer.clear()
	if member:
		var body: Node3D = member.get_parent() as Node3D
		_start_position = body.global_position
		_start_yaw = body.global_rotation.y
