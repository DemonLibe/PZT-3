class_name SleepZone
extends AnomalyZone
## «Сон» (Район 8): сонливость растёт, при 1.0 участник засыпает.
## Не проснулся за 20–40 с — гибель. Проснуться: серия нажатий или разбудит другой.

## member -> момент гибели (по часам зоны)
var _death_at: Dictionary = {}
var _clock: float = 0.0


func _physics_process(delta: float) -> void:
	_clock += delta
	super(delta)


func _check_rule(member: ExpeditionMember, delta: float) -> void:
	if not member.is_sleeping:
		_death_at.erase(member)
		member.add_drowsiness(float(param("drowsiness_rate", 0.01)) * delta)
		if member.drowsiness > 0.2:
			observe(member)
		if member.drowsiness >= 1.0:
			_fall_asleep(member)
		return
	if not _death_at.has(member):
		_fall_asleep(member)
	if member.wake_taps >= int(param("wake_taps", 8)):
		_wake(member)
	elif _clock >= float(_death_at[member]):
		_death_at.erase(member)
		violate(member)


func _on_member_exited(member: ExpeditionMember) -> void:
	if _death_at.has(member) and member.is_active():
		_wake(member)


func get_debug_text(member: ExpeditionMember) -> String:
	if _death_at.has(member):
		return "Сон: спит, гибель через %.1f с, нажатий %d/%d" % [
			float(_death_at[member]) - _clock, min(member.wake_taps, 999), int(param("wake_taps", 8))]
	return "Сон: сонливость %.2f" % member.drowsiness


func _fall_asleep(member: ExpeditionMember) -> void:
	member.add_status(&"forced_sleep")
	member.set_sleeping(true)
	_death_at[member] = _clock + GameState.rng.randf_range(float(param("death_min", 20.0)), float(param("death_max", 40.0)))


func _wake(member: ExpeditionMember) -> void:
	_death_at.erase(member)
	member.remove_status(&"forced_sleep")
	member.set_sleeping(false)
	member.drowsiness = float(param("wake_drowsiness", 0.5))
