extends Control
## База экспедиции: выбор района, Энциклопедия, журнал, настройки.

const ENCYCLOPEDIA_SCENE: String = "res://ui/encyclopedia_view.tscn"
const SETTINGS_SCENE: String = "res://ui/settings_menu.tscn"
const NET_SCENE: String = "res://debug/net_menu.tscn"


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	NetAuthority.prepare(NetAuthority.Mode.SOLO)
	%Subtitle.text = "База экспедиции · экспедиций проведено: %d" % Encyclopedia.expedition_count
	for destination in Destinations.LIST:
		%Destination.add_item(destination["title"])
	%JournalButton.visible = GameState.last_journal != null
	%SettingsButton.visible = ResourceLoader.exists(SETTINGS_SCENE)
	%StartButton.pressed.connect(func() -> void: GameState.begin_expedition(Destinations.LIST[%Destination.selected]))
	%EncyclopediaButton.pressed.connect(get_tree().change_scene_to_file.bind(ENCYCLOPEDIA_SCENE))
	%JournalButton.pressed.connect(get_tree().change_scene_to_file.bind(GameState.JOURNAL_SCENE))
	%SettingsButton.pressed.connect(get_tree().change_scene_to_file.bind(SETTINGS_SCENE))
	%NetButton.pressed.connect(get_tree().change_scene_to_file.bind(NET_SCENE))
	%QuitButton.pressed.connect(get_tree().quit)
	%StartButton.grab_focus()
