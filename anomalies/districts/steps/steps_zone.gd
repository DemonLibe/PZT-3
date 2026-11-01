class_name StepsZone
extends AnomalyZone
## «Шаги» (Район 20): позади группы — шаги, повторяющие шаги замыкающего с задержкой в один шаг.
## Если замыкающий остановился, а шаг позади всё равно прозвучал, — дальше записей нет.

const STEP: AudioStream = preload("res://audio/sfx/footstep.wav")

var _last: ExpeditionMember
var _was_moving: float = 0.0
var _step_timer: float = 0.0
## member -> время пропажи
var _doomed: Dictionary = {}
var _clock: float = 0.0


func _physics_process(delta: float) -> void:
	_clock += delta
	super(delta)
	if not NetAuthority.is_authority():
		return
	for member in _doomed.keys():
		if is_instance_valid(member) and member.is_active() and _clock >= float(_doomed[member]):
			_doomed.erase(member)
			violate(member)
	_last = _rearmost()
	if _last == null:
		return
	observe(_last)
	var moving: bool = _last.motion != ExpeditionMember.Motion.IDLE
	if moving:
		_was_moving += delta
		_step_timer -= delta
		if _step_timer <= 0.0:
			_step_timer = 0.5
			_echo.rpc(_behind(_last), -8.0)
		return
	if _was_moving > float(param("min_walk_before_stop", 2.0)) and not _doomed.has(_last):
		if GameState.rng.randf() < float(param("step_after_stop_chance", 0.08)):
			_doomed[_last] = _clock + float(param("doom_delay", 3.0))
			_echo.rpc(_behind(_last), -4.0)  # шаг позади, хотя замыкающий стоит
	_was_moving = 0.0


func get_debug_text(member: ExpeditionMember) -> String:
	var text: String = "Шаги: замыкающий — %s" % (_last.display_name if _last else "—")
	if _doomed.has(member):
		text += ", ШАГ ПОСЛЕ ОСТАНОВКИ"
	return text


## Замыкающий — тот, кто дальше всех от ведущего.
func _rearmost() -> ExpeditionMember:
	var squad: Squad = get_tree().get_first_node_in_group(&"squad") as Squad
	if squad == null or squad.leader == null:
		return null
	var best: ExpeditionMember = null
	var best_distance: float = -1.0
	for member in members:
		if not member.is_active():
			continue
		var d: float = member.body.global_position.distance_to(squad.leader.body.global_position)
		if d > best_distance:
			best_distance = d
			best = member
	return best


func _behind(member: ExpeditionMember) -> Vector3:
	return member.body.global_position + member.body.global_basis.z * 1.4


@rpc("authority", "call_local", "unreliable")
func _echo(at: Vector3, volume_db: float) -> void:
	Sfx.play_at(self, STEP, at, volume_db, 0.9)
