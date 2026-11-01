extends TestHarness

func _ready() -> void:
	var level := await load_level("res://levels/district_01_dinner.tscn")
	var m := local_member()
	var npcs := npcs_of(level)
	await wait(1.0)
	var plates: Array = level.get_node("Plates").get_children()
	var shown: int = plates.filter(func(p): return p.visible).size()
	check(shown == 5, "стол накрыт на 4+1 мест (%d)" % shown)
	for i in npcs.size(): npcs[i].body.global_position = Vector3(-1.5 + 1.5 * i, 0, 15)
	await press(&"squad_hold")
	m.body.global_position = Vector3(-8.7, 0, 0.8)
	m.drowsiness = 0.7
	await frames(3)
	var plate: Node3D = plates[1]
	face(m, plate.global_position)
	await frames(3)
	check(m.gaze_target == plate, "смотрит на тарелку (%s)" % m.gaze_label)
	await press(&"interact")
	check(m.is_eating, "ест")
	await wait(3.3)
	check(not m.is_eating and m.has_status(&"ate_dinner"), "доел, скрытый статус ate_dinner")
	check(absf(m.drowsiness - 0.3) < 0.05, "сонливость снизилась на 0.4 (%.2f)" % m.drowsiness)
	check(not plate.visible, "тарелка пуста")
	GameState.debug_skip_hours(9.5)
	await wait(0.3)
	check(m.has_status(&"lost_purpose"), "через 3–9 игровых часов — потеря цели")
	# NPC и соблазн: уставший напарник рядом со столом
	var n: ExpeditionMember = npcs[0]
	n.body.global_position = Vector3(-7.5, 0, 1.0)
	n.drowsiness = 0.95
	n.panic = 0.5
	var brain = n.body.get_node("NPCBrain")
	brain.hold_position = n.body.global_position
	for i in 60:
		await wait(0.5)
		if i % 4 == 0: print("   npc ", n.body.global_position, " st=", brain.state, " drowsy=", n.drowsiness, " target=", n.body.get_node("NPCInstincts")._target, " gaze=", n.gaze_label, " eat=", n.is_eating)
		if n.has_status(&"ate_dinner"): break
	check(n.has_status(&"ate_dinner"), "уставший NPC поддался соблазну и поел")
	GameState.debug_skip_hours(9.5)
	await wait(0.5)
	check(n.has_status(&"lost_purpose"), "NPC потерял цель")
	var home: Vector3 = n.body.global_position
	await press(&"squad_follow")
	m.body.global_position = Vector3(0, 0, 15)
	await wait(5.0)
	check(n.body.global_position.distance_to(home) < 2.0, "NPC без цели не идёт за игроком, остаётся в доме")
	check(npcs[1].body.global_position.distance_to(m.body.global_position) < 5.0, "остальные NPC идут за игроком")
	finish()
