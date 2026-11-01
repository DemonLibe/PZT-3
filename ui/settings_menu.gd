extends Control
## Экран настроек (из главного меню или с базы).

## Куда вернуться по кнопке «Назад».
static var return_scene: String = "res://ui/base_menu.tscn"


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	%BackButton.pressed.connect(func() -> void: get_tree().change_scene_to_file(return_scene))
