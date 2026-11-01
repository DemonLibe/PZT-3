extends CanvasLayer
## Сонливость и сон локального участника: темнеет по краям, во сне — почти чёрный экран.

@export var max_awake_darkness: float = 0.55

@onready var _dark: ColorRect = $Dark
@onready var _hint: Label = $Dark/Hint


func _process(delta: float) -> void:
	var member: ExpeditionMember = get_tree().get_first_node_in_group(&"local_member") as ExpeditionMember
	if member == null or not member.is_active():
		_dark.modulate.a = 0.0
		return
	var target: float = 0.0
	if member.is_sleeping:
		target = 0.96
		if member.has_status(&"forced_sleep"):
			_hint.text = "Не спать. [E]"
		else:
			_hint.text = "Отдых. [Z] — встать"
	else:
		target = maxf(0.0, member.drowsiness - 0.4) / 0.6 * max_awake_darkness
		_hint.text = ""
	_dark.modulate.a = move_toward(_dark.modulate.a, target, delta * 1.5)
