class_name ShaftZone
extends AnomalyZone
## «Смотрящий из шахты» (Секция 49): в открытых шахтах при взгляде вниз виден огромный глаз.
## Задержал взгляд дольше секунды — потеря сознания и провал в памяти на часы.

@export var shafts_root: Node

## member -> секунд взгляда вниз в шахту
var _stare: Dictionary = {}
## member -> когда очнётся
var _out: Dictionary = {}
var _clock: float = 0.0


func _physics_process(delta: float) -> void:
	_clock += delta
	super(delta)
	if not NetAuthority.is_authority():
		return
	for member in _out.keys():
		if is_instance_valid(member) and _clock >= float(_out[member]):
			_out.erase(member)
			member.remove_status(&"forced_sleep")
			member.set_sleeping(false)
			member.add_panic(0.3)


func _check_rule(member: ExpeditionMember, delta: float) -> void:
	if member.is_sleeping:
		return
	var shaft: Node3D = _shaft_in_view(member)
	if shaft == null:
		_stare.erase(member)
		return
	observe(member)
	_stare[member] = float(_stare.get(member, 0.0)) + delta
	if _stare[member] > float(param("stare_limit", 1.0)):
		_stare.erase(member)
		EventBus.rule_violated.emit(member, data.id)
		member.add_status(&"forced_sleep")
		member.add_status(&"memory_gap")
		member.set_sleeping(true)
		_out[member] = _clock + float(param("faint_time", 12.0))
		GameState.debug_skip_hours(GameState.rng.randf_range(float(param("gap_min_hours", 2.0)), float(param("gap_max_hours", 24.0))))


func get_debug_text(member: ExpeditionMember) -> String:
	if _out.has(member):
		return "Шахта: без сознания ещё %.0f с" % (float(_out[member]) - _clock)
	return "Шахта: взгляд вниз %.1f / %.1f с" % [float(_stare.get(member, 0.0)), float(param("stare_limit", 1.0))]


func _shaft_in_view(member: ExpeditionMember) -> Node3D:
	for shaft in shafts_root.get_children():
		var bottom: Vector3 = (shaft as Node3D).global_position + Vector3(0, -2.0, 0)
		var flat: float = Vector2(bottom.x - member.body.global_position.x, bottom.z - member.body.global_position.z).length()
		if flat < 2.5 and member.get_gaze_direction().y < -0.6 and member.is_in_view_cone(bottom, 50.0):
			return shaft
	return null
