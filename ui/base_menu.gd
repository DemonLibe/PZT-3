extends Control
## База: кампания строго по порядку. Список направлений, сведения о выбранном, выход.

const DESTINATIONS: GDScript = preload("res://levels/destinations.gd")
const ENCYCLOPEDIA_SCENE: String = "res://ui/encyclopedia_view.tscn"
const SETTINGS_SCENE: String = "res://ui/settings_menu.tscn"
const NET_SCENE: String = "res://debug/net_menu.tscn"
const MAIN_SCENE: String = "res://ui/main_menu.tscn"
const COLOR_DONE: Color = Color(0.55, 0.72, 0.5)
const COLOR_CURRENT: Color = Color(0.92, 0.7, 0.38)
const COLOR_LOCKED: Color = Color(0.38, 0.38, 0.36)

var _selected: int = 0


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	NetAuthority.prepare(NetAuthority.Mode.SOLO)
	%Subtitle.text = "Экспедиций: %d   ·   Пройдено: %d из %d" % [
		Encyclopedia.expedition_count, Encyclopedia.completed.size(), DESTINATIONS.LIST.size()]
	for i in DESTINATIONS.LIST.size():
		var title: String = DESTINATIONS.LIST[i]["title"]
		var done: bool = Encyclopedia.is_completed(title)
		var open: bool = DESTINATIONS.is_unlocked(i)
		var state: String = "пройден" if done else ("текущий" if open else "закрыт")
		var index: int = %Destinations.add_item("%s   —   %s" % [title, state])
		%Destinations.set_item_custom_fg_color(index, COLOR_DONE if done else (COLOR_CURRENT if open else COLOR_LOCKED))
	%Destinations.item_selected.connect(_select)
	%StartButton.pressed.connect(_start)
	%EncyclopediaButton.pressed.connect(get_tree().change_scene_to_file.bind(ENCYCLOPEDIA_SCENE))
	%JournalButton.visible = GameState.last_journal != null
	%JournalButton.pressed.connect(get_tree().change_scene_to_file.bind(GameState.JOURNAL_SCENE))
	%SettingsButton.pressed.connect(_open_settings)
	%NetButton.pressed.connect(get_tree().change_scene_to_file.bind(NET_SCENE))
	%BackButton.pressed.connect(get_tree().change_scene_to_file.bind(MAIN_SCENE))
	var current: int = DESTINATIONS.current_index()
	%Destinations.select(current)
	%Destinations.ensure_current_is_visible()
	_select(current)
	%StartButton.grab_focus()


func _select(index: int) -> void:
	_selected = index
	var destination: Dictionary = DESTINATIONS.LIST[index]
	var title: String = destination["title"]
	var open: bool = DESTINATIONS.is_unlocked(index)
	%DestTitle.text = title
	if Encyclopedia.is_completed(title):
		%DestState.text = "Задание выполнено. Можно пройти снова."
	elif open:
		%DestState.text = "Текущее направление. Три фиксации по маршруту, выход — через КПП."
	else:
		%DestState.text = "Закрыто. Сначала выполните задание: %s." % DESTINATIONS.LIST[index - 1]["title"]
	var anomaly: StringName = StringName(destination.get("anomaly", ""))
	if Encyclopedia.article_level(anomaly) > 0:
		%Info.text = "%s\n\n%s" % [Encyclopedia.get_title(anomaly), Encyclopedia.get_article_text(anomaly)]
	else:
		%Info.text = "Сведения о направлении не задокументированы.\nЗапись в Энциклопедии появится после первой встречи с аномалией."
	%StartButton.disabled = not open
	%StartButton.text = "Выйти в экспедицию" if open else "Закрыто"


func _start() -> void:
	if DESTINATIONS.is_unlocked(_selected):
		GameState.begin_expedition(DESTINATIONS.LIST[_selected])


func _open_settings() -> void:
	preload("res://ui/settings_menu.gd").return_scene = scene_file_path
	get_tree().change_scene_to_file(SETTINGS_SCENE)
