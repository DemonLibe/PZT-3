extends TestHarness
## Секции 43 «Эхо», 44 «Сборщик», 45 «Тихий».

func _ready() -> void:
	var level := await load_level("res://levels/section_43_echo.tscn", 0)
	level.loss_delay = 9999.0
	var zone: EchoZone = level.get_node("EchoZone")
	var m := local_member()
	zone.data.params["lost_chance"] = 0.0
	m.body.global_position = Vector3(0, 0, 0)
	await press(&"speak")
	await wait(2.0)
	check(zone._echoes.size() == 1, "сказал вслух — эхо повторяет")
	var hours: float = GameState.game_hours
	m.body.global_position = zone._echoes[0]["pos"]
	m.body.global_position.y = 0
	await wait(0.5)
	check(m.body.global_position.distance_to(Vector3(0, 0, 16.5)) < 1.0 and GameState.game_hours > hours + 1.0, "пошёл на эхо — блуждал часы и вернулся к началу")
	zone.data.params["lost_chance"] = 0.3
	level.queue_free()
	await frames(3)
	level = await load_level("res://levels/section_44_collector.tscn", 0)
	var cz: CollectorZone = level.get_node("CollectorZone")
	m = local_member()
	m.body.global_position = Vector3(0, 0, 0)
	cz._drop_timer = 999.0
	await wait(0.5)
	var item: DroppedItem = null
	for c in cz.get_children():
		if c is DroppedItem: item = c
	check(item != null and item.owner_member == m, "игрок обронил вещь")
	m.body.global_position = item.global_position + Vector3(0, 0, -1.2)
	await frames(2)
	face(m, item.global_position)
	await frames(3)
	await press(&"interact")
	await frames(3)
	check(m.has_status(&"marked"), "поднял свою вещь — «меченый»")
	level.queue_free()
	await frames(3)
	level = await load_level("res://levels/section_45_silent.tscn", 0)
	level.loss_delay = 9999.0
	var sz: SilentZone = level.get_node("SilentZone")
	m = local_member()
	sz.data.params["vanish_after"] = 2.0
	sz._radius = 5.0
	m.body.global_position = Vector3(0, 0, -20)
	await wait(1.0)
	check(m.has_status(&"silence"), "внезапная тишина — Тихий рядом")
	await wait(2.0)
	check(m.is_vanished and m.fate_cause == &"silent", "не отступил — не обнаружен")
	sz.data.params["vanish_after"] = 60.0
	finish()
