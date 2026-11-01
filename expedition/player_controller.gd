class_name PlayerController
extends Node
## Ввод игрока и камера. Только читает ввод и просит участника действовать.

signal pause_requested

@export var member: ExpeditionMember
@export var actions: MemberActions
@export var camera: Camera3D
@export var mouse_sensitivity: float = 0.0025

var _is_local: bool = false


func _ready() -> void:
	_is_local = member.get_parent().is_multiplayer_authority()
	set_physics_process(_is_local)
	set_process_unhandled_input(_is_local)
	if camera:
		camera.current = _is_local
	if _is_local:
		member.add_to_group(&"local_member")
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED


func _physics_process(_delta: float) -> void:
	member.move_intent = Input.get_vector(&"move_left", &"move_right", &"move_forward", &"move_back")
	member.wants_sprint = Input.is_action_pressed(&"sprint")
	member.wants_crouch = Input.is_action_pressed(&"crouch")


func _unhandled_input(event: InputEvent) -> void:
	var captured: bool = Input.mouse_mode == Input.MOUSE_MODE_CAPTURED
	if event is InputEventMouseMotion and captured:
		var motion: InputEventMouseMotion = event
		var sens: float = mouse_sensitivity * _sensitivity_scale()
		member.look(-motion.relative.x * sens, -motion.relative.y * sens)
	elif event is InputEventMouseButton and event.pressed and not captured:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	elif event.is_action_pressed(&"ui_cancel"):
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		pause_requested.emit()
	elif event.is_action_pressed(&"interact"):
		if member.is_sleeping:
			actions.wake_tap()
		else:
			actions.interact()
	elif event.is_action_pressed(&"flashlight"):
		actions.toggle_flashlight()
	elif event.is_action_pressed(&"rest"):
		actions.toggle_rest()
	elif event.is_action_pressed(&"squad_follow"):
		actions.squad_command(Squad.COMMAND_FOLLOW)
	elif event.is_action_pressed(&"squad_hold"):
		actions.squad_command(Squad.COMMAND_HOLD)


func _sensitivity_scale() -> float:
	return 1.0
