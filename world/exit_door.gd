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
	var points: Array[Node] = get_tree().get_nodes_in_group(&"survey_point")
	var done: int = points.filter(func(p: Node) -> bool: return p.is_done).size()
	var result: String = "возвращение на базу, фиксаций %d из %d" % [done, points.size()]
	if done == points.size() and points.size() > 0:
		result += " — задание выполнено"
		var level: Level = owner as Level
		if level:
			Encyclopedia.mark_completed(level.title)
	GameState.end_expedition(result, survivors, left_behind)
