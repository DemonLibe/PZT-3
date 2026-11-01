class_name SilenceZone
extends AnomalyZone
## «Тишина» (Район 11): звука нет, слышно только своё сердце — и оно замедляется.
## Ниже death_bpm — остановка сердца. Перед этим — собственный голос снаружи, зовущий по имени.

## member -> сказал ли уже голос его имя
var _called: Dictionary = {}


func _check_rule(member: ExpeditionMember, delta: float) -> void:
	observe(member)
	if not member.has_status(&"silence"):
		member.add_status(&"silence")
	member.pulse_bpm = maxf(0.0, member.pulse_bpm - float(param("bpm_drop_per_sec", 0.45)) * delta)
	if member.pulse_bpm < float(param("call_bpm", 45.0)) and not _called.has(member):
		_called[member] = true
		_tell_member(member, member.display_name)
	if member.pulse_bpm < float(param("death_bpm", 40.0)):
		violate(member)


func _physics_process(delta: float) -> void:
	super(delta)
	if not NetAuthority.is_authority():
		return
	# Вне района пульс понемногу возвращается.
	var squad: Squad = get_tree().get_first_node_in_group(&"squad") as Squad
	if squad == null:
		return
	for member in squad.active_members():
		if not members.has(member) and member.pulse_bpm < float(param("start_bpm", 72.0)):
			member.pulse_bpm = minf(float(param("start_bpm", 72.0)), member.pulse_bpm + float(param("bpm_recover_per_sec", 1.5)) * delta)


func _on_member_exited(member: ExpeditionMember) -> void:
	member.remove_status(&"silence")
	_called.erase(member)


func get_debug_text(member: ExpeditionMember) -> String:
	return "Тишина: пульс %.0f уд/мин (остановка ниже %.0f)" % [member.pulse_bpm, float(param("death_bpm", 40.0))]


## Голос слышит только сам участник.
func _tell_member(member: ExpeditionMember, member_name: String) -> void:
	var peer: int = member.get_parent().get_multiplayer_authority()
	if member.is_in_group(&"local_member"):
		_call_name(member_name)
	elif NetAuthority.is_networked() and peer != 1:
		_call_name.rpc_id(peer, member_name)


@rpc("authority", "call_remote", "reliable")
func _call_name(member_name: String) -> void:
	EventBus.radio_message.emit("Голос снаружи", "%s!" % member_name)
