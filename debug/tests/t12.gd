extends TestHarness
## Район 3 «Радио».

var radio_lines: Array = []

func _ready() -> void:
	EventBus.radio_message.connect(func(sp, t): if sp == "Радио": radio_lines.append(t))
	var level := await load_level("res://levels/district_03_radio.tscn", 0)
	var zone: RadioZone = level.get_node("RadioZone")
	var m := local_member()
	# Далеко от приёмников — паника растёт быстрее
	m.body.global_position = Vector3(0, 0, 10)
	await wait(3.0)
	var far_panic: float = m.panic
	m.panic = 0.0
	m.body.global_position = Vector3(-5.5, 0, -8.3)
	await wait(3.0)
	check(zone.is_listening(m), "у приёмника — слушает")
	check(m.panic < far_panic, "у приёмника паника растёт медленнее (%.3f < %.3f)" % [m.panic, far_panic])
	zone.data.params["prophecy_delay"] = 3.0
	zone.data.params["broadcast_interval"] = 1.0
	await wait(1.5)
	check(radio_lines.size() > 0, "передача слышна: " + (radio_lines[-1] if radio_lines else "-"))
	zone.data.params["prophecy_chance"] = 1.0
	zone.data.params["prophecy_delay"] = 3.0
	for i in 30:
		await wait(0.5)
		if not m.is_alive: break
	check(radio_lines.any(func(t): return t.contains("погибнет Орлов")), "передача назвала время гибели Орлова")
	check(not m.is_alive and m.fate_cause == &"radio", "предсказание сбылось")
	zone.data.params["prophecy_chance"] = 0.15
	zone.data.params["prophecy_delay"] = 90.0
	zone.data.params["broadcast_interval"] = 12.0
	finish()
