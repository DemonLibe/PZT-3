extends CanvasLayer
## HUD экспедиции: метка цели (выход), подсказка [E] и короткие сообщения.
## Потерявший цель участник меток цели не видит.

const MESSAGES: Dictionary = {
	&"exit_refused": "Дверь не открывается.",
	&"survey_done": "Фиксация записана.",
	&"survey_interrupted": "Запись прервана.",
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
	var points: Array[Node] = get_tree().get_nodes_in_group(&"survey_point")
	var done: int = points.filter(func(p: Node) -> bool: return p.is_done).size()
	var task: String = "Фиксации: %d из %d" % [done, points.size()]
	if done == points.size():
		task = "Фиксации собраны — к КПП"
	var recording: String = ""
	for point in points:
		if point.recorder_path == _member.get_path():
			recording = "Запись фиксации… %d%%   ·   " % int(point.progress * 100.0)
	var watch: String = ""
	if _member.has_status(&"own_clock"):
		var minutes: float = fmod((ExpeditionJournal.START_HOUR + GameState.game_hours) * 60.0 + _member.watch_offset_min + 1440.0, 1440.0)
		watch = "Ваши часы: %02d:%02d   ·   " % [int(minutes / 60.0), int(fmod(minutes, 60.0))]
	_objective.text = "%s%s%s   ·   КПП: %d м   ·   [1] за мной  [2] стоять" % [watch, recording, task, int(distance)]


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
