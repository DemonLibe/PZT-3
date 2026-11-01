class_name MailZone
extends AnomalyZone
## «Почта» (Район 14): в ящиках — письма каждому участнику по имени, с деталями,
## которых нет ни в одном деле. Содержание не разглашается; прочитавший — в тревоге.

@export var mailboxes_root: Node


func _ready() -> void:
	super()
	for child in mailboxes_root.find_children("*", "Mailbox", true, false):
		child.zone = self


func _check_rule(member: ExpeditionMember, _delta: float) -> void:
	for box in mailboxes_root.get_children():
		if (box as Node3D).global_position.distance_to(member.body.global_position) < 4.0:
			observe(member)
			return


func read_letter(member: ExpeditionMember) -> void:
	if not NetAuthority.is_authority() or not member.can_act() or member.has_status(&"read_letter"):
		return
	member.add_status(&"read_letter")
	member.add_panic(float(param("panic_read", 0.45)))
	EventBus.rule_violated.emit(member, data.id)
	var text: String = "Конверт подписан: «%s». Почерк знакомый. Вы дочитываете до конца и не хотите об этом говорить." % member.display_name
	var peer: int = member.get_parent().get_multiplayer_authority()
	if member.is_in_group(&"local_member"):
		_show(text)
	elif NetAuthority.is_networked() and peer != 1:
		_show.rpc_id(peer, text)


func get_debug_text(member: ExpeditionMember) -> String:
	return "Почта: %s" % ("письмо прочитано" if member.has_status(&"read_letter") else "письмо ждёт")


@rpc("authority", "call_remote", "reliable")
func _show(text: String) -> void:
	EventBus.radio_message.emit("Письмо", text)
