extends TestHarness
## Район 13 «Часы».

func _ready() -> void:
	var level := await load_level("res://levels/district_13_clocks.tscn", 1)
	level.loss_delay = 9999.0
	var zone: ClocksZone = level.get_node("ClocksZone")
	var m := local_member()
	var n: ExpeditionMember = npcs_of(level)[0]
	await press(&"squad_hold")
	m.body.global_position = Vector3(0, 0, -5)
	n.body.global_position = Vector3(2, 0, -5)
	n.body.get_node("NPCBrain").hold_position = n.body.global_position
	await wait(1.0)
	check(m.has_status(&"own_clock"), "у игрока свои часы")
	check(absf(m.watch_offset_min - n.watch_offset_min) > 1.0, "часы игрока и NPC расходятся (%+.0f и %+.0f)" % [m.watch_offset_min, n.watch_offset_min])
	var first: float = m.watch_offset_min
	check(level.get_node("HUD").find_child("Location", true, false).text.contains("Ваши часы"), "HUD показывает личные часы")
	zone.data.params["sync_time"] = 6.0
	await wait(2.0)
	check(absf(m.watch_offset_min) < absf(first), "показания сходятся")
	await wait(4.0)
	check(m.is_vanished and n.is_vanished, "часы синхронизировались — группа потеряна")
	zone.data.params["sync_time"] = 240.0
	finish()
