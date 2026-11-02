extends Control
## Главное меню.


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	%StartButton.text = "Начать экспедиции" if Encyclopedia.expedition_count == 0 else "Продолжить экспедиции"
	%StartButton.pressed.connect(get_tree().change_scene_to_file.bind(GameState.BASE_SCENE))
	%SettingsButton.pressed.connect(_open_settings)
	%QuitButton.pressed.connect(get_tree().quit)
	%StartButton.grab_focus()


func _open_settings() -> void:
	preload("res://ui/settings_menu.gd").return_scene = scene_file_path
	get_tree().change_scene_to_file("res://ui/settings_menu.tscn")
