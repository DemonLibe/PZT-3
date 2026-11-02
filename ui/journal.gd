extends Control
## Журнал последней экспедиции: итог, судьба каждого участника и события по времени.


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	%BackButton.pressed.connect(get_tree().change_scene_to_file.bind(GameState.BASE_SCENE))
	%BackButton.grab_focus()
	var journal: ExpeditionJournal = GameState.last_journal
	if journal == null:
		%Header.text = "Журнал экспедиции"
		%Outcome.text = ""
		%Text.text = "Записей нет."
		return
	%Header.text = "Журнал экспедиции №%d  ·  %s" % [journal.number, journal.destination]
	%Outcome.text = "Итог: %s." % journal.outcome
	var lines: PackedStringArray = ["Состав:"]
	for member_name in journal.fates.keys():
		lines.append("    %s — %s" % [member_name, journal.fates[member_name]])
	lines.append("")
	lines.append("Записи:")
	for entry in journal.entries:
		lines.append("    " + entry)
	%Text.text = "\n".join(lines)
