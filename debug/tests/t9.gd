extends TestHarness

func level() -> Node:
	return get_tree().current_scene

func go(title: String) -> void:
	get_tree().current_scene = null  # чтобы смена сцены не удалила тест
	for d in Destinations.LIST:
		if d["title"] == title:
			GameState.begin_expedition(d)
	await wait(1.0)

func _ready() -> void:
	await frames(2)
	Encyclopedia.reset()
	# 1. Район 5: игрок пропадает в Зеркале
	await go("Район 5")
	check(level() != null and level().name == "District05Mirror", "экспедиция вышла в Район 5")
	check(GameState.is_expedition_active() and GameState.journal.number == 1, "журнал №1 заведён")
	var m := local_member()
	var win: Node3D = level().get_node("Windows/MirrorWindow1")
	m.body.global_position = Vector3(-1.5, 0, -13)
	await frames(2)
	face(m, win.global_position)
	await wait(16.0)
	check(m.is_vanished, "игрок пропал")
	await wait(5.0)
	check(level() != null and level().name == "JournalView", "показан журнал экспедиции")
	var j: ExpeditionJournal = GameState.last_journal
	check(j.outcome == "отряд потерян", "итог: отряд потерян")
	check(j.fates.get("Орлов") == "пропал", "судьба игрока: пропал")
	check("\n".join(j.entries).contains("Орлов: связь потеряна. Зеркало."), "запись о пропаже в журнале")
	check(Encyclopedia.article_level(&"mirror") == 2, "статья «Зеркало» открыта полностью")
	var recs: Array = Encyclopedia.incidents.get("mirror", [])
	check(recs.has("Экспедиция №1: Орлов — пропал."), "в статье запись о пропавшем")
	check(not "\n".join(PackedStringArray(recs)).contains("отказался"), "пропавшие не записаны как оставшиеся")
	check(FileAccess.file_exists(Encyclopedia.SAVE_PATH), "Энциклопедия сохранена на диск")
	print("   ", Encyclopedia.get_article_text(&"mirror").replace("\n", " | "))
	# 2. Район 1: возвращение через выход
	await go("Район 1")
	m = local_member()
	var door: Node3D = level().get_node("ExitDoor")
	m.body.global_position = door.global_transform * Vector3(0, 0, 1.6)
	await frames(2)
	face(m, door.global_position + Vector3(0, 1.2, 0))
	await frames(3)
	await press(&"interact")
	await wait(0.5)
	j = GameState.last_journal
	check(j.number == 2 and j.outcome.begins_with("возвращение на базу"), "экспедиция №2 вернулась через выход: " + j.outcome)
	check(j.fates.get("Орлов") == "вернулся", "Орлов вернулся")
	check(Encyclopedia.article_level(&"dinner") == 0, "в дом с ужином не заходили — статья закрыта")
	# 3. Потеря цели: выход не открывается
	await go("Район 1")
	m = local_member()
	m.add_status(&"lost_purpose")
	door = level().get_node("ExitDoor")
	m.body.global_position = door.global_transform * Vector3(0, 0, 1.6)
	await frames(2)
	face(m, door.global_position + Vector3(0, 1.2, 0))
	await frames(3)
	await press(&"interact")
	await wait(0.5)
	check(GameState.is_expedition_active() and level().name == "District01Dinner", "потерявший цель не может выйти")
	check(not level().get_node("HUD").find_child("ObjectivePanel", true, false).visible, "метки цели в HUD пропали")
	# 4. Тень: отчёт обрывается
	var jj := ExpeditionJournal.new(99, "тест")
	jj.record_loss("Огава", true, Encyclopedia.get_data(&"shadow"))
	check(jj.entries[-1].ends_with("что там за сп"), "отчёт пропавшего в Тени обрывается на полуслове")
	finish()
