class_name ChoirZone
extends AnomalyZone
## «Хористы» (Секция 35): многоголосое пение; силуэты стоят кругом лицом друг к другу.
## Подпел (сказал вслух рядом, даже невольно) — ноги сами несут к кругу, и человек становится частью хора.

@export var circle: Node3D

var _compelled: Array[ExpeditionMember] = []


func _ready() -> void:
	super()
	add_to_group(&"speech_context")
	EventBus.member_spoke.connect(_on_spoke)


func _check_rule(member: ExpeditionMember, delta: float) -> void:
	if _hears(member):
		observe(member)
		# Напарник в панике может подпеть невольно.
		if member.auto_doors and not _compelled.has(member) and \
				GameState.rng.randf() < float(param("npc_hum_chance", 0.01)) * member.panic * delta * 60.0:
			_compel(member)


func _physics_process(delta: float) -> void:
	super(delta)
	if not NetAuthority.is_authority():
		return
	for member in _compelled.duplicate():
		if not member.is_active():
			_compelled.erase(member)
			continue
		var to: Vector3 = circle.global_position - member.body.global_position
		to.y = 0.0
		if to.length() < 1.2:
			_compelled.erase(member)
			member.remove_status(&"compelled")
			violate(member)
			_add_singer.rpc()
			continue
		member.body.look_at(member.body.global_position + to.normalized(), Vector3.UP)
		member.move_intent = Vector2(0, -1)
		member.wants_sprint = false


func speech_phrase(member: ExpeditionMember) -> String:
	return "♪ ♪ ♪" if _hears(member) else ""


func get_debug_text(member: ExpeditionMember) -> String:
	if _compelled.has(member):
		return "Хористы: идёт к кругу"
	return "Хористы: %s" % ("слышит пение" if _hears(member) else "далеко")


func _hears(member: ExpeditionMember) -> bool:
	return circle.global_position.distance_to(member.body.global_position) < float(param("hear_radius", 14.0))


func _on_spoke(member: Node, _phrase: String) -> void:
	var expedition_member: ExpeditionMember = member as ExpeditionMember
	if NetAuthority.is_authority() and expedition_member and _hears(expedition_member) and not _compelled.has(expedition_member):
		_compel(expedition_member)


func _compel(member: ExpeditionMember) -> void:
	_compelled.append(member)
	member.add_status(&"compelled")
	EventBus.rule_violated.emit(member, data.id)


@rpc("authority", "call_local", "reliable")
func _add_singer() -> void:
	var singer: MeshInstance3D = MeshInstance3D.new()
	var capsule: CapsuleMesh = CapsuleMesh.new()
	capsule.radius = 0.3
	capsule.height = 1.8
	singer.mesh = capsule
	circle.add_child(singer)
	var angle: float = circle.get_child_count() * 0.9
	singer.position = Vector3(cos(angle) * 1.5, 0.9, sin(angle) * 1.5)
