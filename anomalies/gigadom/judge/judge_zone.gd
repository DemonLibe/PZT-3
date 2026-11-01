class_name JudgeZone
extends AnomalyZone
## «Судья» (Секция 47): появляется только в ответ на открытый конфликт внутри группы
## (крик, угрозы). Наказывает обе стороны, не разбирая, кто начал.

@export var judge: Node3D


func _ready() -> void:
	super()
	add_to_group(&"speech_context")
	EventBus.member_spoke.connect(_on_spoke)
	judge.visible = false


func _check_rule(member: ExpeditionMember, delta: float) -> void:
	# Напарники в панике иногда срываются друг на друга.
	if member.auto_doors and member.panic > 0.6 and GameState.rng.randf() < float(param("npc_conflict_chance", 0.004)) * delta * 60.0:
		var other: ExpeditionMember = _nearest_other(member, 5.0)
		if other:
			_conflict(member, other)


func speech_phrase(member: ExpeditionMember) -> String:
	return "Да ты достал уже!" if _target_of(member) else ""


func get_debug_text(_member: ExpeditionMember) -> String:
	return "Судья: тишина в группе"


func _on_spoke(member: Node, _phrase: String) -> void:
	var expedition_member: ExpeditionMember = member as ExpeditionMember
	if not NetAuthority.is_authority() or expedition_member == null or not members.has(expedition_member):
		return
	var other: ExpeditionMember = _target_of(expedition_member)
	if other:
		_conflict(expedition_member, other)


## На кого участник кричит: смотрит прямо на товарища вплотную.
func _target_of(member: ExpeditionMember) -> ExpeditionMember:
	for other in members:
		if other != member and other.is_active() and other.body.global_position.distance_to(member.body.global_position) < 4.0 \
				and member.is_in_view_cone(other.body.global_position + Vector3(0, 1.4, 0), 25.0):
			return other
	return null


func _nearest_other(member: ExpeditionMember, radius: float) -> ExpeditionMember:
	for other in members:
		if other != member and other.is_active() and other.body.global_position.distance_to(member.body.global_position) < radius:
			return other
	return null


func _conflict(a: ExpeditionMember, b: ExpeditionMember) -> void:
	observe(a)
	observe(b)
	_appear.rpc((a.body.global_position + b.body.global_position) * 0.5)
	violate(a)
	violate(b)


@rpc("authority", "call_local", "reliable")
func _appear(at: Vector3) -> void:
	judge.visible = true
	judge.global_position = Vector3(at.x + 1.5, 0.0, at.z)
	await get_tree().create_timer(3.0).timeout
	judge.visible = false
