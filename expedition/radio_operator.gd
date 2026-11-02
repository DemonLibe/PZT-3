class_name RadioOperator
extends Node
## Голоса снаружи и в отряде: подполковник Дорохов по рации, сержант Мельников вслух.
## Слушает события экспедиции на хосте и рассылает реплики всем через EventBus.radio_message.

const DOROKHOV: String = "Дорохов"
const GUIDE_NAME: String = "Мельников"
## До какой по счёту экспедиции Дорохов не запоминает имён (по сюжету — до третьего района).
const NAMES_FROM_EXPEDITION: int = 3

@export var intro_delay: float = 2.0

var _hinted: Dictionary = {}
var _numbers: Dictionary = {}


func _ready() -> void:
	if not NetAuthority.is_authority():
		return
	EventBus.member_died.connect(_on_member_lost)
	EventBus.member_vanished.connect(_on_member_lost)
	EventBus.anomaly_observed.connect(_on_anomaly_observed)
	await get_tree().create_timer(intro_delay).timeout
	var level: Level = get_parent() as Level
	var title: String = level.title if level else "зону"
	say(DOROKHOV, "Группа, вход: %s. Работаем по протоколу. Вольфу нужны три фиксации. Конец связи." % title)
	for point in get_tree().get_nodes_in_group(&"survey_point"):
		point.completed.connect(_on_survey_completed)


func say(speaker: String, text: String) -> void:
	if NetAuthority.is_authority():
		_broadcast.rpc(speaker, text)


@rpc("authority", "call_local", "reliable")
func _broadcast(speaker: String, text: String) -> void:
	EventBus.radio_message.emit(speaker, text)


func _on_survey_completed() -> void:
	var points: Array[Node] = get_tree().get_nodes_in_group(&"survey_point")
	var done: int = points.filter(func(p: Node) -> bool: return p.is_done).size()
	if done >= points.size():
		say(DOROKHOV, "Все фиксации есть. Возвращайтесь к КПП.")
	else:
		say(DOROKHOV, "Фиксация %d из %d принята." % [done, points.size()])


func _on_member_lost(member: Node) -> void:
	var lost: ExpeditionMember = member as ExpeditionMember
	if lost == null or lost.is_in_group(&"local_member"):
		return
	say(DOROKHOV, "Потерял сигнал: %s." % _call_sign(lost))


func _on_anomaly_observed(member: Node, anomaly_id: StringName) -> void:
	if _hinted.has(anomaly_id):
		return
	_hinted[anomaly_id] = true
	var data: AnomalyData = Encyclopedia.get_data(anomaly_id)
	if data == null or data.guide_hint == "":
		return
	if _guide_alive():
		say(GUIDE_NAME, data.guide_hint)
	else:
		say(DOROKHOV, "Протокол района: %s" % data.guide_hint)


## Дорохов до третьей экспедиции зовёт заключённых по номерам.
func _call_sign(member: ExpeditionMember) -> String:
	if Encyclopedia.expedition_count + 1 >= NAMES_FROM_EXPEDITION or member.display_name == GUIDE_NAME:
		return member.display_name
	if not _numbers.has(member):
		_numbers[member] = _numbers.size() + 1
	return "номер %d" % _numbers[member]


func _guide_alive() -> bool:
	var squad: Squad = get_tree().get_first_node_in_group(&"squad") as Squad
	if squad == null:
		return false
	return squad.active_members().any(func(m: ExpeditionMember) -> bool: return m.display_name == GUIDE_NAME)
