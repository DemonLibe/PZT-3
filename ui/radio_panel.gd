extends CanvasLayer
## Реплики по рации и в отряде: последние строки вверху экрана, гаснут со временем.

@export var line_time: float = 7.0
@export var max_lines: int = 3

var _lines: Array[Dictionary] = []

@onready var _label: Label = $Panel/Label
@onready var _panel: Control = $Panel


func _ready() -> void:
	EventBus.radio_message.connect(_on_radio_message)


func _process(delta: float) -> void:
	for line in _lines:
		line["left"] -= delta
	_lines = _lines.filter(func(l: Dictionary) -> bool: return l["left"] > 0.0)
	var texts: PackedStringArray = []
	for line in _lines:
		texts.append("%s: %s" % [line["speaker"], line["text"]])
	_label.text = "\n".join(texts)
	_panel.visible = not texts.is_empty()


func _on_radio_message(speaker: String, text: String) -> void:
	_lines.append({"speaker": speaker, "text": text, "left": line_time})
	while _lines.size() > max_lines:
		_lines.pop_front()
	print("[Рация] %s: %s" % [speaker, text])
