class_name ReflectionZone
extends AnomalyZone
## «Отражение группы» (Район 12): вдали идёт вторая такая же группа — с задержкой 3–40 с.
## Не приближаться и не подавать сигналов. Нарушил — «отражение» опережает: показывает,
## как падает участник, и через omen_delay с это случается с ним самим.

@export var offset: Vector3 = Vector3(0, 0, -48)

## Тела участников -> история [время, позиция, поворот] (пишется на каждой машине)
var _history: Dictionary = {}
var _ghosts: Dictionary = {}
var _delay: float = 10.0
var _clock: float = 0.0
var _repick: float = 0.0
## member -> время гибели
var _omens: Dictionary = {}


func _process(delta: float) -> void:
	_clock += delta
	var squad: Squad = get_tree().get_first_node_in_group(&"squad") as Squad
	if squad == null:
		return
	for member in squad.members:
		if not is_instance_valid(member):
			continue
		var history: Array = _history.get(member, [])
		history.append([_clock, member.body.global_position, member.body.global_rotation.y])
		while history.size() > 2 and history[1][0] < _clock - 45.0:
			history.pop_front()
		_history[member] = history
		_update_ghost(member, history)


func _physics_process(delta: float) -> void:
	super(delta)
	if not NetAuthority.is_authority():
		return
	_repick -= delta
	if _repick <= 0.0:
		_repick = 10.0
		_set_delay.rpc(GameState.rng.randf_range(float(param("delay_min", 3.0)), float(param("delay_max", 40.0))))
	for member in _omens.keys():
		if is_instance_valid(member) and member.is_active() and _clock >= float(_omens[member]):
			_omens.erase(member)
			violate(member)


func _check_rule(member: ExpeditionMember, _delta: float) -> void:
	if _omens.has(member):
		return
	for ghost in _ghosts.values():
		var at: Vector3 = (ghost as Node3D).global_position + Vector3(0, 1.0, 0)
		if member.is_in_view_cone(at, 60.0):
			observe(member)
		var close: bool = member.body.global_position.distance_to(at) < float(param("approach_limit", 15.0))
		var signal_sent: bool = member.flashlight_on and member.is_in_view_cone(at, 20.0)
		if close or signal_sent:
			_omens[member] = _clock + float(param("omen_delay", 60.0))
			EventBus.rule_violated.emit(member, data.id)
			_show_omen.rpc(member.get_path())
			return


func get_debug_text(member: ExpeditionMember) -> String:
	var text: String = "Отражение: задержка %.0f с" % _delay
	if _omens.has(member):
		text += ", ОПЕРЕЖАЕТ: %.0f с" % (float(_omens[member]) - _clock)
	return text


func _update_ghost(member: ExpeditionMember, history: Array) -> void:
	if not _ghosts.has(member):
		var source: MeshInstance3D = member.body.get_node_or_null("BodyMesh") as MeshInstance3D
		if source == null:
			return
		var ghost: Node3D = Node3D.new()
		ghost.add_child(source.duplicate())
		add_child(ghost)
		_ghosts[member] = ghost
	var ghost_node: Node3D = _ghosts[member]
	var target_time: float = _clock - _delay
	var sample: Array = history[0]
	for entry in history:
		if entry[0] > target_time:
			break
		sample = entry
	if ghost_node.get_meta(&"fallen", false):
		return
	ghost_node.global_position = sample[1] + offset
	ghost_node.global_rotation.y = sample[2]


@rpc("authority", "call_local", "reliable")
func _set_delay(value: float) -> void:
	_delay = value


## Отражение показывает будущее: участник падает.
@rpc("authority", "call_local", "reliable")
func _show_omen(member_path: NodePath) -> void:
	var member: ExpeditionMember = get_node_or_null(member_path) as ExpeditionMember
	if member and _ghosts.has(member):
		var ghost: Node3D = _ghosts[member]
		ghost.set_meta(&"fallen", true)
		ghost.global_position = member.body.global_position + offset
		create_tween().tween_property(ghost, "rotation:x", -PI / 2.0, 0.8)
