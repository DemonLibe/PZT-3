extends TestHarness

func _ready() -> void:
	var level: Node = load("res://levels/district_05_mirror.tscn").instantiate()
	add_child(level)
	await frames(10)
	var m := local_member()
	var squad: Squad = level.get_node("Squad")
	check(squad.size() == 4, "в отряде 4 участника (%d)" % squad.size())
	check(squad.leader == m, "ведёт игрок")
	var nav: NavigationRegion3D = level.get_node("NavigationRegion3D")
	check(nav.navigation_mesh.get_polygon_count() > 0, "навигация построена (%d полигонов)" % nav.navigation_mesh.get_polygon_count())
	var npcs: Array[ExpeditionMember] = []
	for b in level.get_node("Members").get_children():
		if b.name.begins_with("npc"): npcs.append(ExpeditionMember.find_on(b))
	# Игрок уходит вперёд на 20 м
	m.body.global_position = Vector3(0, 0, -5)
	await wait(9.0)
	var near: int = 0
	for n in npcs:
		if n.body.global_position.distance_to(m.body.global_position) < 5.0: near += 1
	check(near == 3, "все 3 NPC догнали игрока (%d)" % near)
	# Команда «стоять»
	var ev := InputEventAction.new(); ev.action = &"squad_hold"; ev.pressed = true
	Input.parse_input_event(ev)
	await frames(3)
	var held: Vector3 = npcs[0].body.global_position
	m.body.global_position = Vector3(0, 0, 12)
	await wait(4.0)
	check(npcs[0].body.global_position.distance_to(held) < 1.5, "по команде 2 стоят на месте")
	ev = InputEventAction.new(); ev.action = &"squad_follow"; ev.pressed = true
	Input.parse_input_event(ev)
	await wait(7.0)
	check(npcs[0].body.global_position.distance_to(m.body.global_position) < 5.0, "по команде 1 снова идут за игроком")
	# NPC может пропасть в Зеркале: высокая паника = долгий взгляд в окно
	for n in npcs:
		n.panic = 0.7
	var vanished: int = 0
	for i in 60:
		await wait(1.0)
		vanished = npcs.filter(func(n): return n.is_vanished).size()
		if vanished > 0: break
	check(vanished > 0, "NPC пропал в Зеркале (через %d с)" % [0])
	check(m.panic > 0.0, "у игрока выросла паника от потери (%.2f)" % m.panic)
	finish()
