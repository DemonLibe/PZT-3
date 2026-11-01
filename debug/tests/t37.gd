extends TestHarness
## Секции 41 «Пожарные» и 42 «Кукольник».

func _ready() -> void:
	var level := await load_level("res://levels/section_41_firemen.tscn", 0)
	var zone: FiremenZone = level.get_node("FiremenZone")
	var m := local_member()
	m.body.global_position = Vector3(0, 0, 0)
	await wait(1.0)
	check(zone._figures.is_empty(), "без огня — никого")
	await press(&"fire")
	await wait(1.0)
	check(m.fire_on and zone._figures.size() == 3, "зажёг огонь (G) — появились обгоревшие фигуры")
	for i in 40:
		await wait(0.25)
		if m.has_status(&"burns"): break
	check(m.has_status(&"burns"), "фигуры сошлись к огню — ожоги")
	level.queue_free()
	await frames(3)
	level = await load_level("res://levels/section_42_puppeteer.tscn", 0)
	level.loss_delay = 9999.0
	m = local_member()
	var double: Node3D = level.get_node("Doubles/Double1")
	m.body.global_position = double.global_position + Vector3(0, 0, 1.4)
	await frames(2)
	face(m, double.global_position + Vector3(0, 1.0, 0))
	await frames(3)
	await press(&"interact")
	check(not m.has_status(&"struck_double"), "без оружия — не ударить")
	await press(&"weapon")
	face(m, double.global_position + Vector3(0, 1.0, 0))
	await frames(3)
	await press(&"interact")
	check(m.has_status(&"struck_double"), "ударил дубля")
	GameState.debug_skip_hours(4.5)
	await wait(0.3)
	check(not m.is_alive and m.fate_cause == &"puppeteer", "через несколько часов — то же самое, зеркально")
	finish()
