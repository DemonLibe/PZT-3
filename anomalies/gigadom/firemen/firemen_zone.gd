class_name FiremenZone
extends AnomalyZone
## «Пожарные» (Секция 41): обгоревшие фигуры появляются только на открытый огонь.
## Сходятся к огню и к тем, кто рядом; от касания — ожоги неясной природы.

@export var spawns_root: Node
@export var figure_template: Node3D

var _figures: Array[Node3D] = []
var _no_fire_time: float = 0.0


func _ready() -> void:
	super()
	figure_template.visible = false


func _physics_process(delta: float) -> void:
	super(delta)
	if not NetAuthority.is_authority():
		return
	var burning: Array[ExpeditionMember] = members.filter(func(m: ExpeditionMember) -> bool: return m.is_active() and m.fire_on)
	if burning.is_empty():
		_no_fire_time += delta
		if _no_fire_time > float(param("fade_after", 5.0)) and not _figures.is_empty():
			_clear.rpc()
		return
	_no_fire_time = 0.0
	if _figures.is_empty():
		for spot in spawns_root.get_children():
			_spawn.rpc((spot as Node3D).global_position)
	var fire: Vector3 = burning[0].body.global_position
	for figure in _figures:
		var to: Vector3 = fire - figure.global_position
		to.y = 0.0
		figure.global_position += to.normalized() * float(param("speed", 1.3)) * delta
		for member in members:
			if member.is_active() and member.body.global_position.distance_to(figure.global_position) < 1.0 \
					and not member.has_status(&"burns"):
				member.add_status(&"burns")
				member.add_panic(0.3)
				EventBus.rule_violated.emit(member, data.id)


func _check_rule(member: ExpeditionMember, _delta: float) -> void:
	if member.fire_on or not _figures.is_empty():
		observe(member)


func get_debug_text(_member: ExpeditionMember) -> String:
	return "Пожарные: фигур %d" % _figures.size()


@rpc("authority", "call_local", "reliable")
func _spawn(at: Vector3) -> void:
	var figure: Node3D = figure_template.duplicate() as Node3D
	figure.visible = true
	add_child(figure)
	figure.global_position = at
	_figures.append(figure)


@rpc("authority", "call_local", "reliable")
func _clear() -> void:
	for figure in _figures:
		figure.queue_free()
	_figures.clear()
