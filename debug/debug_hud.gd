extends CanvasLayer
## Отладочный HUD: состояние локального участника и данные аномалий.
## Только читает состояние, ничего не меняет. F3 — показать/скрыть.

const MOTION_NAMES: PackedStringArray = ["стоит", "присед", "шаг", "бег"]

@onready var _label: Label = $Panel/Label


func _process(_delta: float) -> void:
	var member: ExpeditionMember = get_tree().get_first_node_in_group(&"local_member") as ExpeditionMember
	if member == null:
		_label.text = "Нет локального участника"
		return
	var lines: PackedStringArray = []
	lines.append("FPS: %d" % Engine.get_frames_per_second())
	lines.append("Цель взгляда: %s" % (member.gaze_label if member.gaze_label != "" else "—"))
	lines.append("Секунды взгляда: %.2f" % member.gaze_time)
	lines.append("Шум: %.2f (%s)" % [member.noise_level, MOTION_NAMES[member.motion]])
	lines.append("Паника: %.2f   Сонливость: %.2f" % [member.panic, member.drowsiness])
	lines.append("Один: %s   Спит: %s   Ест: %s" % [_yes(member.is_alone), _yes(member.is_sleeping), _yes(member.is_eating)])
	lines.append("Жив: %s   Пропал: %s" % [_yes(member.is_alive), _yes(member.is_vanished)])
	lines.append("Статусы: %s" % (", ".join(PackedStringArray(member.statuses.keys())) if not member.statuses.is_empty() else "—"))
	for provider in get_tree().get_nodes_in_group(&"debug_info"):
		var text: String = provider.call(&"get_debug_text", member)
		if text != "":
			lines.append(text)
	_label.text = "\n".join(lines)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed(&"debug_hud"):
		visible = not visible


func _yes(value: bool) -> String:
	return "да" if value else "нет"
