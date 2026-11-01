extends Control
## Просмотр Энциклопедии: список статей и текст выбранной.

var _ids: PackedStringArray = []


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	_ids = Encyclopedia.list_ids()
	for id in _ids:
		var level: int = Encyclopedia.article_level(id)
		var mark: String = ["·", "◐", "●"][level]
		%Articles.add_item("%s  %s" % [mark, Encyclopedia.get_title(id)])
	%Articles.item_selected.connect(_show)
	%BackButton.pressed.connect(get_tree().change_scene_to_file.bind(GameState.BASE_SCENE))
	if not _ids.is_empty():
		%Articles.select(0)
		_show(0)


func _show(index: int) -> void:
	%Text.text = Encyclopedia.get_article_text(_ids[index])
