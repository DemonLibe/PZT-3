class_name SmileZone
extends AnomalyZone
## «Улыбка» (Район 9): лица с улыбкой шире анатомической нормы.
## Кто смотрит прямо на лицо дольше react_time — рефлекторно улыбается в ответ;
## через несколько игровых часов улыбка фиксируется навсегда.

## member -> секунды прямого взгляда на улыбку
var _urge: Dictionary = {}
var _faces: Array[Node3D] = []


func _ready() -> void:
	super()
	for face in get_tree().get_nodes_in_group(&"smile_face"):
		_faces.append(face)


func _check_rule(member: ExpeditionMember, delta: float) -> void:
	if member.has_status(&"smiled"):
		return
	var face: Node3D = _direct_face(member)
	if face == null:
		_urge[member] = maxf(0.0, float(_urge.get(member, 0.0)) - delta * 2.0)
		return
	observe(member)
	_urge[member] = float(_urge.get(member, 0.0)) + delta
	if _urge[member] >= float(param("react_time", 2.5)):
		_urge.erase(member)
		member.add_status(&"smiled")
		EventBus.rule_violated.emit(member, data.id)
		DelayedPunishment.attach(member, data, "SmileEffect", "fix_min_hours", "fix_max_hours")


func get_debug_text(member: ExpeditionMember) -> String:
	if member.has_status(&"smiled"):
		return "Улыбка: улыбнулся в ответ"
	return "Улыбка: %.1f / %.1f с" % [float(_urge.get(member, 0.0)), float(param("react_time", 2.5))]


func _direct_face(member: ExpeditionMember) -> Node3D:
	var cone: float = float(param("direct_cone_deg", 12.0))
	for face in _faces:
		if face.global_position.distance_to(member.get_gaze_origin()) < float(param("see_distance", 14.0)) \
				and member.is_in_view_cone(face.global_position, cone) and _line_of_sight(member, face):
			return face
	return null


func _line_of_sight(member: ExpeditionMember, face: Node3D) -> bool:
	var query: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(member.get_gaze_origin(), face.global_position, 1)
	var hit: Dictionary = get_world_3d().direct_space_state.intersect_ray(query)
	return hit.is_empty() or hit["position"].distance_to(face.global_position) < 0.3
