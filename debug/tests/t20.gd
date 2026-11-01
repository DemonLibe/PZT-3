extends TestHarness
## Район 14 «Почта».

var letters: Array = []

func _ready() -> void:
	EventBus.radio_message.connect(func(sp, t): if sp == "Письмо": letters.append(t))
	var level := await load_level("res://levels/district_14_mail.tscn", 0)
	var m := local_member()
	var box: Node3D = level.get_node("Mailboxes/Mailbox2")
	m.body.global_position = box.global_position + Vector3(1.4, -1.2, 0)
	m.body.global_position.y = 0
	await frames(2)
	face(m, box.global_position)
	await frames(3)
	check(m.gaze_target == box, "смотрит на почтовый ящик (%s)" % m.gaze_label)
	var p0: float = m.panic
	await press(&"interact")
	await frames(3)
	check(m.has_status(&"read_letter"), "письмо прочитано")
	check(m.panic > p0 + 0.3, "тревога после письма (%.2f)" % m.panic)
	check(letters.size() == 1 and letters[0].contains("Орлов"), "письмо адресовано по имени")
	finish()
