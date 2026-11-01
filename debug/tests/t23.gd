extends TestHarness
## Район 20 «Шаги».

func _ready() -> void:
	var level := await load_level("res://levels/district_20_steps.tscn", 1)
	level.loss_delay = 9999.0
	var zone: StepsZone = level.get_node("StepsZone")
	var m := local_member()
	var n: ExpeditionMember = npcs_of(level)[0]
	await press(&"squad_hold")
	n.body.global_position = Vector3(0, 0, 0)
	m.body.global_position = Vector3(0, 0, -12)
	n.body.get_node("NPCBrain").hold_position = Vector3(0, 0, 8)
	await wait(1.0)
	check(zone.get_debug_text(m).contains("Наумов") or zone._last == n, "замыкающий — NPC позади")
	zone.data.params["step_after_stop_chance"] = 1.0
	zone.data.params["min_walk_before_stop"] = 1.0
	for i in 40:
		await wait(0.25)
		if n.is_vanished: break
	check(n.is_vanished and n.fate_cause == &"steps", "замыкающий остановился, а шаг прозвучал — пропал")
	zone.data.params["step_after_stop_chance"] = 0.08
	zone.data.params["min_walk_before_stop"] = 2.0
	finish()
