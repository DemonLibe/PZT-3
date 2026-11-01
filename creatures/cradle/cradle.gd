class_name Cradle
extends Creature
## «Колыбель» (Секция 32): слепое существо идёт на самый громкий чужой звук.
## Спящий, едящий или беззвучный участник для неё не существует.

var _target: ExpeditionMember
var _target_level: float = 0.0
var _heard_position: Vector3
var _last_heard: float = -1000.0
var _clock: float = 0.0


func _ready() -> void:
	super()
	EventBus.noise_emitted.connect(_on_noise_emitted)


func _think(delta: float) -> void:
	_clock += delta
	if _target and not _target.is_active():
		_target = null
	if _target == null or _clock - _last_heard > float(param("forget_after", 8.0)):
		_target = null
		_target_level = 0.0
		state = State.IDLE
		stop()
		return
	var close: bool = global_position.distance_to(_heard_position) < float(param("rush_distance", 8.0))
	state = State.ATTACK if close else State.INVESTIGATE
	var speed: float = float(param("rush_speed", 6.0)) if close else float(param("walk_speed", 1.5))
	var goal: Vector3 = _target.body.global_position if close and perceives(_target) else _heard_position
	move_to(goal, speed)
	_try_attack()


## Существует ли участник для «Колыбели».
func perceives(member: ExpeditionMember) -> bool:
	return member.is_active() and not member.is_sleeping and not member.is_eating and member.noise_level > 0.0


func get_debug_text(_member: ExpeditionMember) -> String:
	if _target == null:
		return "Колыбель: %s, никого не слышит" % State.keys()[state]
	return "Колыбель: %s, цель %s, %.1f с с последнего звука" % [State.keys()[state], _target.display_name, _clock - _last_heard]


func _try_attack() -> void:
	var reach: float = float(param("attack_range", 1.5))
	for member in all_members():
		if perceives(member) and member.body.global_position.distance_to(global_position) <= reach:
			punish(member)
			if member == _target:
				_target = null


func _on_noise_emitted(member: Node, position: Vector3, level: float) -> void:
	if not NetAuthority.is_authority():
		return
	var source: ExpeditionMember = member as ExpeditionMember
	if source == null or not perceives(source):
		return
	if level < float(param("min_noise", 0.15)):
		return
	if position.distance_to(global_position) > float(param("hearing_radius", 25.0)):
		return
	# Самый громкий источник; свежий звук важнее старого.
	if source == _target or level >= _target_level or _clock - _last_heard > 1.0:
		_target = source
		_target_level = level
		_heard_position = position
		_last_heard = _clock
