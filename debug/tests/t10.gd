extends TestHarness
## Сквозной проход среза через меню.

func scene() -> Node:
	return get_tree().current_scene

func open(path: String) -> void:
	get_tree().change_scene_to_file(path)
	await wait(0.6)

func _ready() -> void:
	await frames(1)
	# Тест живёт рядом со сценами: текущей делаем пустышку, её и будут сменять.
	var dummy: Node = Node.new()
	get_tree().root.add_child(dummy)
	get_tree().current_scene = dummy
	await frames(1)
	Encyclopedia.reset()
	await open("res://ui/main_menu.tscn")
	check(scene().name == "MainMenu", "главное меню")
	var keep: Node = scene()
	keep.find_child("StartButton", true, false).pressed.emit()
	await wait(0.6)
	check(scene().name == "BaseMenu", "кнопка «Начать» — база")
	for i in Destinations.LIST.size():
		var dest: Dictionary = Destinations.LIST[i]
		var base: Node = scene()
		base.get_node("%Destination").select(i)
		base.get_node("%StartButton").pressed.emit()
		await wait(2.5)
		var lvl: Node = scene()
		check(lvl is Level and lvl.title == dest["title"], "вылазка: %s" % dest["title"])
		var m := local_member()
		if i == 0:
			# Пауза: открыть и закрыть
			get_tree().get_first_node_in_group(&"local_controller").pause_requested.emit()
			await frames(2)
			check(get_tree().paused and lvl.get_node("PauseMenu").visible, "пауза по Esc")
			lvl.get_node("PauseMenu").close()
			await frames(2)
			check(not get_tree().paused, "продолжить")
		var door: Node3D = lvl.get_node_or_null("ExitDoor")
		if door == null:
			# Район 30: КПП нет — вылазку прерываем через паузу.
			get_tree().get_first_node_in_group(&"local_controller").pause_requested.emit()
			await frames(2)
			lvl.get_node("PauseMenu")._abort()
			await wait(0.8)
			check(scene() != null and scene().name == "JournalView", "%s: нет КПП, вылазка прервана" % dest["title"])
			var jv: Node = scene()
			jv.get_node("%BackButton").pressed.emit()
			await wait(0.6)
			continue
		var front: Vector3 = door.global_transform * Vector3(0, 0, 1.6)
		m.body.global_position = front
		await frames(2)
		face(m, door.global_position + Vector3(0, 1.2, 0))
		await frames(3)
		await press(&"interact")
		await wait(0.8)
		check(scene() != null and scene().name == "JournalView", "%s: возвращение, журнал" % dest["title"])
		var journal_view: Node = scene()
		journal_view.get_node("%BackButton").pressed.emit()
		await wait(0.6)
		check(scene().name == "BaseMenu", "назад на базу")
	check(Encyclopedia.expedition_count == Destinations.LIST.size(), "проведено экспедиций: %d" % Encyclopedia.expedition_count)
	var base2: Node = scene()
	base2.get_node("%EncyclopediaButton").pressed.emit()
	await wait(0.6)
	check(scene().name == "EncyclopediaView" and scene().get_node("%Articles").item_count == Encyclopedia.list_ids().size(), "Энциклопедия: %d статей" % Encyclopedia.list_ids().size())
	await open("res://ui/settings_menu.tscn")
	var panel: Node = scene().find_child("SettingsPanel", true, false)
	panel.get_node("%Ps1").button_pressed = false
	await frames(2)
	check(not RetroRender._post.visible and FileAccess.file_exists(Settings.PATH), "настройки: PS1 выключается и сохраняется")
	panel.get_node("%Ps1").button_pressed = true
	finish()
