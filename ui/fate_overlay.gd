extends CanvasLayer
## Экран судьбы локального участника: затемнение, когда он погиб или пропал.
## Слушает сигналы участника, ничего в мире не меняет.

const TEXT_VANISHED: String = "Сигнал участника потерян."
const TEXT_DIED: String = "Пульс участника не фиксируется."

@export var fade_time: float = 2.5

var _member: ExpeditionMember

@onready var _black: ColorRect = $Black
@onready var _label: Label = $Black/Label


func _ready() -> void:
	_black.modulate.a = 0.0
	_black.visible = false


func _process(_delta: float) -> void:
	if _member != null:
		return
	_member = get_tree().get_first_node_in_group(&"local_member") as ExpeditionMember
	if _member:
		_member.vanished.connect(func(_c: StringName) -> void: _show(TEXT_VANISHED))
		_member.died.connect(func(_c: StringName) -> void: _show(TEXT_DIED))


func _show(text: String) -> void:
	_label.text = text
	_black.visible = true
	var tween: Tween = create_tween()
	tween.tween_property(_black, "modulate:a", 1.0, fade_time)
