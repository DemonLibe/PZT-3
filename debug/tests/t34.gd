extends TestHarness
## Секция 35 «Хористы».

func _ready() -> void:
	var level := await load_level("res://levels/section_35_choir.tscn", 0)
	level.loss_delay = 9999.0
	var m := local_member()
	m.body.global_position = Vector3(0, 0, -4)
	await wait(0.5)
	await press(&"speak")
	await frames(3)
	check(m.has_status(&"compelled"), "подпел — ноги несут к кругу")
	Input.action_press(&"move_back")
	for i in 40:
		await wait(0.25)
		if m.is_vanished: break
	Input.action_release(&"move_back")
	check(m.is_vanished and m.fate_cause == &"choir", "занял место в круге")
	check(level.get_node("Circle").get_child_count() >= 7, "в круге стало больше силуэтов")
	finish()
