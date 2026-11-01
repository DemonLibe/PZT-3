class_name GrinderZone
extends AnomalyZone
## «Точильщик» (Секция 39): существо в вентиляции реагирует на вибрацию шагов по металлу.
## По решёткам — только шагом, без рывков и бега. Побежал — пол проваливается.

@export var gratings_root: Node


func _check_rule(member: ExpeditionMember, _delta: float) -> void:
	var grating: Node3D = _grating_under(member)
	if grating == null:
		return
	observe(member)
	if member.motion == ExpeditionMember.Motion.RUN:
		_collapse.rpc(grating.name)
		violate(member)


func get_debug_text(member: ExpeditionMember) -> String:
	return "Точильщик: %s" % ("на металле" if _grating_under(member) else "на бетоне")


func _grating_under(member: ExpeditionMember) -> Node3D:
	for grating in gratings_root.get_children():
		var g: Node3D = grating
		if not g.visible:
			continue
		var half: Vector3 = g.get_meta(&"half_size", Vector3(1, 0, 1))
		var local: Vector3 = member.body.global_position - g.global_position
		if absf(local.x) <= half.x and absf(local.z) <= half.z:
			return g
	return null


@rpc("authority", "call_local", "reliable")
func _collapse(grating_name: String) -> void:
	var grating: Node3D = gratings_root.get_node_or_null(grating_name) as Node3D
	if grating:
		grating.visible = false
