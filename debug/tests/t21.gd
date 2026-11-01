extends TestHarness
## Район 16 «Колыбельная».

func _ready() -> void:
	var level := await load_level("res://levels/district_16_lullaby.tscn", 1)
	var zone: LullabyZone = level.get_node("LullabyZone")
	var m := local_member()
	var n: ExpeditionMember = npcs_of(level)[0]
	await press(&"squad_hold")
	zone.data.params["song_length"] = 4.0
	zone.data.params["warn_time"] = 3.0
	zone.data.params["reset_after"] = 1.0
	m.body.global_position = Vector3(4, 0, -4.5)
	await wait(2.5)
	m.body.global_position = Vector3(0, 0, 17)  # ушёл, не дослушав
	await wait(1.5)
	m.body.global_position = Vector3(4, 0, -4.5)
	await wait(2.5)
	check(not m.has_status(&"nameless"), "прервал прослушивание — имя помнит")
	await wait(2.0)
	check(m.has_status(&"nameless"), "дослушал до конца — забыл имя")
	n.body.global_position = Vector3(4, 0, -3.0)
	n.body.get_node("NPCBrain").hold_position = n.body.global_position
	await wait(4.5)
	check(n.has_status(&"nameless"), "NPC тоже забыл имя")
	await press(&"squad_follow")
	m.body.global_position = Vector3(0, 0, 17)
	await wait(4.0)
	check(n.body.global_position.distance_to(Vector3(4, 0, -3.0)) < 2.0, "безымянный NPC больше не слушает приказов")
	zone.data.params["song_length"] = 360.0
	zone.data.params["warn_time"] = 300.0
	zone.data.params["reset_after"] = 15.0
	finish()
