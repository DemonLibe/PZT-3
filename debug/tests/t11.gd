extends TestHarness
## Точки замера: запись, прерывание, выполнение задания.

func _ready() -> void:
	await frames(1)
	Encyclopedia.reset()
	var level := await load_level("res://levels/district_05_mirror.tscn", 0)
	var m := local_member()
	var points: Array = level.get_node("SurveyPoints").get_children()
	check(points.size() == 3, "в районе 3 точки замера")
	var p: SurveyPoint = points[0]
	m.body.global_position = p.global_position + Vector3(1.4, 0, 0)
	await frames(2)
	face(m, p.global_position + Vector3(0, 1.1, 0))
	await frames(3)
	check(m.gaze_target == p, "смотрит на точку замера (%s)" % m.gaze_label)
	await press(&"interact")
	await wait(2.0)
	check(p.progress > 0.3 and not p.is_done, "идёт запись (%.0f%%)" % (p.progress * 100))
	check(level.get_node("HUD").find_child("Progress", true, false).visible, "HUD показывает запись")
	m.body.global_position += Vector3(5, 0, 0)  # отошёл
	await wait(0.3)
	check(p.progress == 0.0 and not p.is_done, "отошёл — запись прервана")
	m.body.global_position = p.global_position + Vector3(1.4, 0, 0)
	await frames(2)
	face(m, p.global_position + Vector3(0, 1.1, 0))
	await frames(3)
	await press(&"interact")
	await wait(4.3)
	check(p.is_done, "через 4 с замер записан")
	check(level.get_node("HUD").find_child("Objective", true, false).text == "Фиксация 2 из 3", "HUD ведёт к следующей: " + level.get_node("HUD").find_child("Objective", true, false).text)
	for q in points:
		q._complete()
	await frames(2)
	check(level.get_node("HUD").find_child("Objective", true, false).text.begins_with("Фиксации собраны"), "все фиксации собраны")
	var dummy: Node = Node.new()
	get_tree().root.add_child(dummy)
	get_tree().current_scene = dummy
	var door: Node3D = level.get_node("ExitDoor")
	m.body.global_position = door.global_transform * Vector3(0, 0, 1.6)
	await frames(2)
	face(m, door.global_position + Vector3(0, 1.2, 0))
	await frames(3)
	await press(&"interact")
	await wait(0.5)
	var j: ExpeditionJournal = GameState.last_journal
	check(j != null and j.outcome.ends_with("задание выполнено"), "итог: " + (j.outcome if j else "-"))
	check(Encyclopedia.is_completed("Район 5"), "Район 5 отмечен выполненным")
	finish()
