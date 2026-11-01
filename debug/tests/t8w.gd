extends TestHarness

func _ready() -> void:
	var level := await load_level("res://levels/section_36_warden.tscn", 0)
	var m := local_member()
	var warden: Warden = level.get_node("Warden")
	var door: Door = level.get_node("Door4")
	var path: Path3D = level.get_node("WardenPath")
	check(path.curve.get_baked_length() > 60.0, "маршрут Смотрителя загружен (%.0f м)" % path.curve.get_baked_length())
	await wait(0.5)
	check(not door.is_open, "дверь закрыта")
	# Ждём, пока Смотритель проверит комнату 4 (игрок внутри, дверь закрыта)
	var checked: bool = false
	for i in 400:
		await wait(0.1)
		if warden.state == Creature.State.INVESTIGATE and warden.global_position.x > 10: checked = true
		if checked and warden.state == Creature.State.PATROL: break
	check(checked, "Смотритель проверил комнату 4")
	check(m.is_active(), "за закрытой дверью — цел")
	# Игрок открывает дверь взглядом и E
	face(m, door.global_position + Vector3(0, 1.1, 0))
	m.body.global_position = Vector3(12, 0, -3.5)
	await frames(3)
	face(m, door.global_position + Vector3(0, 1.1, 0))
	await frames(3)
	await press(&"interact")
	await wait(0.5)
	check(door.is_open, "игрок открыл дверь (E)")
	for i in 500:
		await wait(0.1)
		if m.is_vanished: break
	check(m.is_vanished and m.fate_cause == &"warden", "дверь открыта, игрок внутри — Смотритель забрал")
	# NPC и двери: напарник сам открывает и закрывает
	level.queue_free()
	await frames(3)
	var lvl2 := await load_level("res://levels/section_36_warden.tscn", 1)
	var n: ExpeditionMember = npcs_of(lvl2)[0]
	var d2: Door = lvl2.get_node("Door2")
	var w2: Warden = lvl2.get_node("Warden")
	w2.process_mode = Node.PROCESS_MODE_DISABLED
	var p := local_member()
	p.body.global_position = Vector3(-4, 0, -6)   # игрок в комнате 2
	n.body.global_position = Vector3(-8, 0, 0.5)   # NPC в коридоре
	var opened: bool = false
	for i in 150:
		await wait(0.1)
		if d2.is_open: opened = true
		if opened and not d2.is_open: break
	check(opened, "NPC открыл дверь, идя за игроком")
	check(not d2.is_open, "NPC закрыл дверь за собой")
	check(n.body.global_position.z < -2.5, "NPC в комнате (z=%.1f)" % n.body.global_position.z)
	finish()
