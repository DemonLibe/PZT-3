extends TestHarness

func _ready() -> void:
	var level := await load_level("res://levels/district_06_shadow.tscn", 0)
	var zone: ShadowZone = level.get_node("ShadowZone")
	zone.data.params["point_chance"] = 1.0
	zone.data.params["check_interval"] = 1.0
	var m := local_member()
	m.body.global_position = Vector3(0, 0, 0)
	await wait(1.5)
	check(zone.get_debug_text(m).contains("УКАЗЫВАЕТ"), "тень указывает за спину")
	var fig: Node3D = zone.get_child(zone.get_child_count() - 1)
	check(fig is ShadowFigure and fig.visible, "копия тени видна")
	# Медленный поворот на 90° за 2 с — можно
	for i in 120:
		m.look(deg_to_rad(90.0) / 120.0, 0)
		await get_tree().physics_frame
	check(m.is_active(), "медленный поворот на 90° — без последствий")
	# Обернуться на 170° за 0.5 с — нельзя
	for i in 30:
		m.look(deg_to_rad(170.0) / 30.0, 0)
		await get_tree().physics_frame
	await frames(2)
	check(m.is_vanished, "обернулся, пока тень указывала — пропал")
	# NPC в панике вертится и пропадает
	level.npc_count = 3
	var lvl2 := await load_level("res://levels/district_06_shadow.tscn", 3)
	lvl2.get_node("ShadowZone").data.params["point_chance"] = 1.0
	var npcs := npcs_of(lvl2)
	for n in npcs:
		n.body.global_position = Vector3(GameState.rng.randf_range(-3, 3), 0, GameState.rng.randf_range(-3, 3))
		n.panic = 1.0
	var gone: int = 0
	for i in 60:
		await wait(0.5)
		for n in npcs: n.panic = 1.0
		gone = npcs.filter(func(n): return n.is_vanished).size()
		if gone > 0: break
	check(gone > 0, "NPC в панике обернулся и пропал")
	finish()
