class_name ExitDoor
extends StaticBody3D
## Выход из района: E — вернуть экспедицию на базу.
## Кто потерял цель, открыть её не может.

## Кто дальше этого расстояния от двери, остаётся в районе.
@export var return_radius: float = 15.0


func _ready() -> void:
	add_to_group(&"exit_door")


func interact(member: ExpeditionMember) -> void:
	if not NetAuthority.is_authority():
		return
	if member.has_status(&"lost_purpose"):
		member.event_received.emit(&"exit_refused")
		return
	var squad: Squad = get_tree().get_first_node_in_group(&"squad") as Squad
	var survivors: Array[ExpeditionMember] = []
	var left_behind: Array[ExpeditionMember] = []
	for other in (squad.active_members() if squad else [member]):
		if other.has_status(&"lost_purpose") or other.body.global_position.distance_to(global_position) > return_radius:
			left_behind.append(other)
		else:
			survivors.append(other)
	GameState.end_expedition("возвращение на базу", survivors, left_behind)
