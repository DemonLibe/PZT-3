extends TestHarness
## Секции 37 «Мясник» и 39 «Точильщик».

func _ready() -> void:
	var level := await load_level("res://levels/section_37_butcher.tscn", 0)
	level.loss_delay = 9999.0
	var m := local_member()
	m.body.global_position = Vector3(4.5, 0, -11)
	await wait(0.5)
	check(m.is_active(), "безоружным к Мяснику — можно")
	m.body.global_position = Vector3(0, 0, 5)
	await press(&"weapon")
	check(m.weapon_out, "оружие в руках (Q)")
	m.body.global_position = Vector3(4.5, 0, -11)
	await wait(0.5)
	check(not m.is_alive and m.fate_cause == &"butcher", "вошёл с оружием — атака")
	level.queue_free()
	await frames(3)
	level = await load_level("res://levels/section_39_grinder.tscn", 0)
	level.loss_delay = 9999.0
	m = local_member()
	m.body.global_position = Vector3(0, 0, 10.5)
	Input.action_press(&"move_forward")
	await wait(1.5)
	Input.action_release(&"move_forward")
	check(m.is_active(), "по решётке шагом — безопасно")
	m.body.global_position = Vector3(0, 0, 0.5)
	Input.action_press(&"move_forward"); Input.action_press(&"sprint")
	await wait(1.2)
	Input.action_release(&"move_forward"); Input.action_release(&"sprint")
	check(m.is_vanished and m.fate_cause == &"grinder", "побежал по металлу — пол провалился")
	finish()
