extends TestHarness
## Район 12 «Отражение группы».

func _ready() -> void:
	var level := await load_level("res://levels/district_12_reflection.tscn", 0)
	level.loss_delay = 9999.0
	var zone: ReflectionZone = level.get_node("ReflectionZone")
	var m := local_member()
	zone._set_delay(3.0)
	zone._repick = 999.0
	m.body.global_position = Vector3(0, 0, 10)
	await wait(3.5)
	var ghost: Node3D = zone._ghosts.get(m)
	check(ghost != null, "вдали видна вторая группа")
	check(ghost and ghost.global_position.distance_to(m.body.global_position + zone.offset) < 0.5, "отражение повторяет маршрут со смещением")
	var before: Vector3 = ghost.global_position
	m.body.global_position = Vector3(2, 0, 8)
	await wait(1.0)
	check(ghost.global_position.distance_to(before) < 0.1, "через 1 с отражение ещё не сдвинулось (задержка)")
	await wait(2.5)
	check(ghost.global_position.distance_to(before) > 2.0, "через 3 с отражение повторило движение")
	# Сигнал фонарём в сторону отражения
	face(m, ghost.global_position + Vector3(0, 1, 0))
	await press(&"flashlight")
	await frames(3)
	check(zone.get_debug_text(m).contains("ОПЕРЕЖАЕТ"), "подал сигнал — отражение опережает")
	check(ghost.get_meta(&"fallen", false), "отражение показало падение")
	zone.data.params["omen_delay"] = 60.0
	zone._omens[m] = zone._clock + 1.0
	await wait(1.5)
	check(not m.is_alive and m.fate_cause == &"reflection", "увиденное у отражения случилось")
	finish()
