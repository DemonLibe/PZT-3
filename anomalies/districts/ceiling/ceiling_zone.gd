class_name CeilingZone
extends AnomalyZone
## «Потолок» (Район 25): тёмные капающие пятна на потолках. Кто надышался парами
## (провёл в комнате дольше inhale_time), видит галлюцинации несколько минут.

## member -> секунды в комнате
var _breathed: Dictionary = {}
## member -> когда галлюцинации пройдут
var _until: Dictionary = {}
var _clock: float = 0.0


func _physics_process(delta: float) -> void:
	_clock += delta
	super(delta)
	if not NetAuthority.is_authority():
		return
	for member in _until.keys():
		if is_instance_valid(member) and _clock >= float(_until[member]):
			_until.erase(member)
			member.remove_status(&"hallucinating")


func _check_rule(member: ExpeditionMember, delta: float) -> void:
	observe(member)
	if member.has_status(&"hallucinating"):
		return
	_breathed[member] = float(_breathed.get(member, 0.0)) + delta
	if _breathed[member] >= float(param("inhale_time", 25.0)):
		_breathed.erase(member)
		member.add_status(&"hallucinating")
		_until[member] = _clock + float(param("hallucination_time", 90.0))
		EventBus.rule_violated.emit(member, data.id)


func _on_member_exited(member: ExpeditionMember) -> void:
	_breathed.erase(member)


func get_debug_text(member: ExpeditionMember) -> String:
	if _until.has(member):
		return "Потолок: галлюцинации ещё %.0f с" % (float(_until[member]) - _clock)
	return "Потолок: дышит парами %.0f / %.0f с" % [float(_breathed.get(member, 0.0)), float(param("inhale_time", 25.0))]
