extends AnomalyZone
## Тестовая аномалия этапа 3: смотреть на цель дольше gaze_limit — наказание.

@export var target: Node


func _check_rule(member: ExpeditionMember, _delta: float) -> void:
	if member.gaze_target != target:
		return
	observe(member)
	if member.gaze_time > float(param("gaze_limit", 3.0)):
		violate(member)


func get_debug_text(member: ExpeditionMember) -> String:
	if member.gaze_target != target:
		return ""
	return "Куб: %.1f / %.1f с" % [member.gaze_time, float(param("gaze_limit", 3.0))]
