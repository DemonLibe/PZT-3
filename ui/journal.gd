extends Control
## Журнал последней экспедиции: события и судьба каждого участника.


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	%BackButton.pressed.connect(get_tree().change_scene_to_file.bind(GameState.BASE_SCENE))
	var journal: ExpeditionJournal = GameState.last_journal
	if journal == null:
		%Header.text = "Журнал экспедиции"
		%Text.text = "Записей нет."
		return
	%Header.text = "Журнал экспедиции №%d · %s" % [journal.number, journal.destination]
	var lines: PackedStringArray = []
	lines.append("Итог: %s." % journal.outcome)
	lines.append("")
	for member_name in journal.fates.keys():
		lines.append("%s — %s" % [member_name, journal.fates[member_name]])
	lines.append("")
	lines.append_array(journal.entries)
	%Text.text = "\n".join(lines)
