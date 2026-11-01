extends TestHarness
## Район 4 «Стирка».

func _ready() -> void:
	var level := await load_level("res://levels/district_04_laundry.tscn", 0)
	var m := local_member()
	var item: Node3D = level.get_node("Laundry/Laundry3")
	m.body.global_position = item.global_position + Vector3(1.5, -1.62, 0)
	await frames(2)
	face(m, item.global_position)
	await frames(3)
	check(m.gaze_target == item, "смотрит на бельё (%s)" % m.gaze_label)
	await press(&"interact")
	await frames(3)
	check(m.has_status(&"wore_laundry") and not item.visible, "надел бельё")
	check(not m.has_status(&"fabric_skin"), "сразу ничего не видно")
	GameState.debug_skip_hours(8.5)
	await wait(0.3)
	check(m.has_status(&"fabric_skin"), "через 5–8 игровых часов — кожа стала тканью")
	m.body.global_position = Vector3(0, 0, 10)
	Input.action_press(&"move_forward"); Input.action_press(&"sprint")
	await wait(0.6)
	check(m.motion != ExpeditionMember.Motion.RUN, "бежать больше не может")
	Input.action_release(&"move_forward"); Input.action_release(&"sprint")
	level.queue_free()
	await frames(3)
	var lvl2 := await load_level("res://levels/district_04_laundry.tscn", 1)
	var n: ExpeditionMember = npcs_of(lvl2)[0]
	await press(&"squad_hold")
	n.body.global_position = Vector3(2.0, 0, -6.0)
	n.body.get_node("NPCBrain").hold_position = n.body.global_position
	n.panic = 0.7
	for i in 80:
		await wait(0.5)
		n.panic = maxf(n.panic, 0.6)
		if n.has_status(&"wore_laundry"): break
	check(n.has_status(&"wore_laundry"), "испуганный NPC надел бельё")
	finish()
