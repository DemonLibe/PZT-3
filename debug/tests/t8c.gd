extends TestHarness

func _ready() -> void:
	var level := await load_level("res://levels/section_32_cradle.tscn", 0)
	var m := local_member()
	var cradle: Cradle = level.get_node("Cradle")
	m.body.global_position = Vector3(0, 0, 2)
	await wait(1.0)
	check(cradle.state == Creature.State.IDLE, "игрок стоит тихо — Колыбель не двигается")
	Input.action_press(&"move_left"); Input.action_press(&"sprint")
	await wait(0.8)
	Input.action_release(&"move_left"); Input.action_release(&"sprint")
	check(cradle.state != Creature.State.IDLE, "бег — Колыбель идёт на звук (%s)" % Creature.State.keys()[cradle.state])
	await wait(14.0)
	check(m.is_alive, "игрок замер — Колыбель пришла, но не тронула")
	check(cradle.global_position.distance_to(m.body.global_position) < 4.0, "Колыбель рядом с игроком (%.1f м)" % cradle.global_position.distance_to(m.body.global_position))
	await wait(9.0)
	check(cradle.state == Creature.State.IDLE, "через 8 с без звука — забыла")
	# Сон: рядом с Колыбелью можно спать
	cradle.global_position = m.body.global_position + Vector3(1.0, 0, 0)
	await press(&"rest")
	check(m.is_sleeping, "игрок лёг спать")
	EventBus.noise_emitted.emit(m, m.body.global_position, 0.9)
	await wait(1.0)
	check(m.is_alive and cradle.state == Creature.State.IDLE, "спящего не слышит и не трогает")
	await press(&"rest")
	check(not m.is_sleeping, "проснулся")
	# Еда: едящего не трогает
	var food: Node3D = level.get_node("Food1")
	m.body.global_position = Vector3(7, 0, 14)
	cradle.global_position = Vector3(8.5, 0, 13.5)
	await frames(3)
	face(m, food.global_position)
	await frames(3)
	await press(&"interact")
	check(m.is_eating, "игрок ест")
	EventBus.noise_emitted.emit(m, m.body.global_position, 0.9)
	await wait(1.0)
	check(m.is_alive, "едящего не трогает")
	await wait(3.5)
	check(not m.is_eating, "доел")
	# Шаг рядом с Колыбелью — смерть
	Input.action_press(&"move_back")
	await wait(1.5)
	Input.action_release(&"move_back")
	check(not m.is_alive and m.fate_cause == &"cradle", "шагнул рядом — Колыбель убила")
	# NPC: шумный напарник
	level.queue_free()
	await frames(3)
	var lvl2 := await load_level("res://levels/section_32_cradle.tscn", 3)
	var c2: Cradle = lvl2.get_node("Cradle")
	var npcs := npcs_of(lvl2)
	await press(&"squad_hold")
	var n := npcs[0]
	n.body.global_position = Vector3(10, 0, 15)  # подальше: пусть идёт долго и шумно
	n.body.get_node("NPCBrain").command = Squad.COMMAND_HOLD
	n.body.get_node("NPCBrain").hold_position = Vector3(-10, 0, -8)
	for i in 80:
		await wait(0.5)
		if not n.is_alive: break
	check(not n.is_alive, "Колыбель нашла идущего NPC")
	check(local_member().is_alive, "стоящий игрок цел")
	finish()
