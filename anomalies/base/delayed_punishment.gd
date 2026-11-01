class_name DelayedPunishment
extends Node
## Отложенное наказание: висит на теле участника и через случайное число
## игровых часов применяет наказание из AnomalyData («Ужин», «Стирка», «Улыбка»).

var member: ExpeditionMember
var data: AnomalyData
var onset_hours: float = 3.0
var start_hours: float = 0.0


## Повесить на участника, если такого ещё нет. Часы — из параметров данных.
static func attach(target: ExpeditionMember, anomaly: AnomalyData, node_name: String, min_key: String, max_key: String) -> void:
	if not NetAuthority.is_authority() or target.body.has_node(node_name):
		return
	var effect: DelayedPunishment = DelayedPunishment.new()
	effect.name = node_name
	effect.member = target
	effect.data = anomaly
	effect.start_hours = GameState.game_hours
	effect.onset_hours = GameState.rng.randf_range(float(anomaly.param(min_key, 3.0)), float(anomaly.param(max_key, 9.0)))
	target.body.add_child(effect)


func _process(_delta: float) -> void:
	if not NetAuthority.is_authority() or member == null or data == null:
		return
	if not member.is_active():
		queue_free()
		return
	if GameState.game_hours - start_hours >= onset_hours:
		data.punish(member)
		queue_free()


func hours_left() -> float:
	return onset_hours - (GameState.game_hours - start_hours)
