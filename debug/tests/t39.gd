extends TestHarness
## Секции 46 «Кормилица» и 47 «Судья».

func _ready() -> void:
	var level := await load_level("res://levels/section_46_nurse.tscn", 1)
	level.loss_delay = 9999.0
	var zone: NurseZone = level.get_node("NurseZone")
	var m := local_member()
	var n: ExpeditionMember = npcs_of(level)[0]
	await press(&"squad_hold")
	n.body.global_position = Vector3(0, 0, 12)
	n.body.get_node("NPCBrain").hold_position = n.body.global_position
	m.body.global_position = Vector3(0, 0, 10)
	await wait(2.0)
	check(m.is_active(), "рядом свои — Кормилицы нет")
	zone.data.params["alone_time"] = 2.0
	m.body.global_position = Vector3(5.5, 0, -10)
	for i in 20:
		await wait(0.3)
		if m.is_vanished: break
	check(m.is_vanished and m.fate_cause == &"nurse", "остался один — увела Кормилица")
	zone.data.params["alone_time"] = 6.0
	level.queue_free()
	await frames(3)
	level = await load_level("res://levels/section_47_judge.tscn", 1)
	level.loss_delay = 9999.0
	m = local_member()
	n = npcs_of(level)[0]
	await press(&"squad_hold")
	n.body.global_position = Vector3(0, 0, 3)
	n.body.get_node("NPCBrain").hold_position = n.body.global_position
	m.body.global_position = Vector3(0, 0, 5)
	await frames(3)
	face(m, n.body.global_position + Vector3(0, 1.4, 0))
	await frames(2)
	await press(&"speak")
	await frames(3)
	check(m.is_vanished and n.is_vanished, "накричал на товарища — Судья наказал обоих")
	finish()
