class_name DinnerEffect
extends Node
## Отложенное действие ужина: висит на теле съевшего и через случайное
## число игровых часов отнимает у него цель (наказание из AnomalyData).

var member: ExpeditionMember
var data: AnomalyData
var onset_hours: float = 3.0
var start_hours: float = 0.0


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
