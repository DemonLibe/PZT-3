extends CanvasLayer
## HUD экспедиции: метка цели (выход), подсказка [E] и короткие сообщения.
## Потерявший цель участник меток цели не видит.

const MESSAGES: Dictionary = {
	&"exit_refused": "Дверь не открывается.",
}

@export var message_time: float = 2.5

var _member: ExpeditionMember
var _message_left: float = 0.0

@onready var _objective: Label = %Objective
@onready var _hint: Label = %Hint
@onready var _message: Label = %Message


func _process(delta: float) -> void:
	if _member == null or not is_instance_valid(_member):
		_member = get_tree().get_first_node_in_group(&"local_member") as ExpeditionMember
		if _member:
			_member.event_received.connect(_on_event)
		return
	_update_objective()
	_hint.text = "[E]" if _member.can_act() and _looks_at_interactable() else ""
	_message_left -= delta
	_message.visible = _message_left > 0.0


func _update_objective() -> void:
	var exit: Node3D = get_tree().get_first_node_in_group(&"exit_door") as Node3D
	if exit == null or not _member.is_active() or _member.has_status(&"lost_purpose"):
		_objective.text = ""
		return
	var distance: float = _member.body.global_position.distance_to(exit.global_position)
	_objective.text = "Выход: %d м   ·   [1] за мной   [2] стоять" % int(distance)


func _looks_at_interactable() -> bool:
	var target: Node = _member.gaze_target
	if target == null or _member.get_gaze_origin().distance_to(_member.gaze_point) > 2.5:
		return false
	return target.has_method(&"interact") or (target.get_parent() and target.get_parent().has_method(&"interact")) \
		or (ExpeditionMember.find_on(target) != null and ExpeditionMember.find_on(target).is_sleeping)


func _on_event(event_id: StringName) -> void:
	if MESSAGES.has(event_id):
		_message.text = MESSAGES[event_id]
		_message_left = message_time
