extends CanvasLayer
## HUD экспедиции: цель (следующая фиксация или КПП) со стрелкой и расстоянием,
## подсказка действия, уведомления о замеченных аномалиях и нарушениях.

const MESSAGES: Dictionary = {
	&"exit_refused": "Дверь не открывается.",
	&"survey_done": "Фиксация записана.",
	&"survey_interrupted": "Запись прервана — стойте рядом с диктофоном.",
	&"survey_out_of_order": "Сначала — предыдущая фиксация по маршруту.",
}

@export var toast_time: float = 3.5

var _member: ExpeditionMember
var _toasts: Array[Dictionary] = []

@onready var _location: Label = %Location
@onready var _objective: Label = %Objective
@onready var _distance: Label = %Distance
@onready var _arrow: CompassArrow = %Arrow
@onready var _progress: ProgressBar = %Progress
@onready var _objective_panel: Control = %ObjectivePanel
@onready var _prompt_panel: Control = %PromptPanel
@onready var _prompt: Label = %Prompt
@onready var _toast_panel: Control = %ToastPanel
@onready var _toast: Label = %Toast


func _ready() -> void:
	EventBus.anomaly_observed.connect(_on_observed)
	EventBus.rule_violated.connect(_on_violated)
	var level: Level = get_parent() as Level
	_location.text = level.title if level else ""


func _process(delta: float) -> void:
	if _member == null or not is_instance_valid(_member):
		_member = get_tree().get_first_node_in_group(&"local_member") as ExpeditionMember
		if _member:
			_member.event_received.connect(_on_event)
		return
	_update_objective()
	_update_prompt()
	_update_toasts(delta)


func _update_objective() -> void:
	var visible_goal: bool = _member.is_active() and not _member.has_status(&"lost_purpose")
	_objective_panel.visible = visible_goal
	if not visible_goal:
		return
	var level: Level = get_parent() as Level
	var title: String = level.title if level else ""
	if _member.has_status(&"own_clock"):
		var minutes: float = fmod((ExpeditionJournal.START_HOUR + GameState.game_hours) * 60.0 + _member.watch_offset_min + 1440.0, 1440.0)
		title += "   ·   Ваши часы: %02d:%02d" % [int(minutes / 60.0), int(fmod(minutes, 60.0))]
	_location.text = title
	var points: Array[Node] = get_tree().get_nodes_in_group(&"survey_point")
	var next: SurveyPoint = SurveyPoint.next_point(get_tree())
	var target: Node3D = next
	if next:
		_objective.text = "Фиксация %d из %d" % [next.order, points.size()]
	else:
		target = get_tree().get_first_node_in_group(&"exit_door") as Node3D
		_objective.text = "Фиксации собраны — к КПП" if target else "Дальше записей нет"
	_progress.visible = next != null and next.recorder_path == _member.get_path()
	if _progress.visible:
		_progress.value = next.progress * 100.0
	_arrow.visible = target != null
	_distance.visible = target != null
	if target == null:
		return
	var to: Vector3 = target.global_position - _member.body.global_position
	_distance.text = "%d м" % int(Vector2(to.x, to.z).length())
	var forward: Vector3 = -_member.body.global_basis.z
	_arrow.angle = Vector2(forward.x, forward.z).angle_to(Vector2(to.x, to.z))


func _update_prompt() -> void:
	var target: Node = _member.gaze_target
	var text: String = ""
	if _member.can_act() and target and _member.get_gaze_origin().distance_to(_member.gaze_point) <= 2.5:
		var node: Node = target
		for i in 3:
			if node == null:
				break
			if node.has_method(&"get_prompt"):
				text = node.call(&"get_prompt")
				break
			if node.has_method(&"interact"):
				text = "Взаимодействовать"
				break
			node = node.get_parent()
	if _member.is_sleeping:
		text = "Проснуться — жмите E" if _member.has_status(&"forced_sleep") else "Встать — Z"
	_prompt_panel.visible = text != ""
	_prompt.text = "[E]  " + text if not _member.is_sleeping else text


func _update_toasts(delta: float) -> void:
	if _toasts.is_empty():
		_toast_panel.visible = false
		return
	_toasts[0]["left"] -= delta
	if _toasts[0]["left"] <= 0.0:
		_toasts.pop_front()
		return
	_toast_panel.visible = true
	_toast.text = _toasts[0]["text"]


func show_toast(text: String) -> void:
	_toasts.append({"text": text, "left": toast_time})


func _on_event(event_id: StringName) -> void:
	if MESSAGES.has(event_id):
		show_toast(MESSAGES[event_id])


func _on_observed(member: Node, anomaly_id: StringName) -> void:
	var data: AnomalyData = Encyclopedia.get_data(anomaly_id)
	if member == _member and data:
		show_toast("Замечено: %s. Энциклопедия пополнена." % data.display_name)


func _on_violated(member: Node, anomaly_id: StringName) -> void:
	var data: AnomalyData = Encyclopedia.get_data(anomaly_id)
	if member == _member and data:
		show_toast("Нарушено правило: %s" % data.display_name)
