extends Control
## Отладочное меню сети: соло, хост или подключение к 127.0.0.1.

const LEVELS: Dictionary = {
	"Район 5 — Зеркало": "res://levels/district_05_mirror.tscn",
}

@onready var _level_select: OptionButton = %LevelSelect
@onready var _address: LineEdit = %Address
@onready var _status: Label = %Status


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	for title in LEVELS.keys():
		_level_select.add_item(title)
	_status.text = NetAuthority.last_error
	%SoloButton.pressed.connect(_start.bind(NetAuthority.Mode.SOLO))
	%HostButton.pressed.connect(_start.bind(NetAuthority.Mode.HOST))
	%JoinButton.pressed.connect(_start.bind(NetAuthority.Mode.CLIENT))


func _start(mode: NetAuthority.Mode) -> void:
	NetAuthority.last_error = ""
	NetAuthority.prepare(mode, _address.text.strip_edges())
	var title: String = _level_select.get_item_text(_level_select.selected)
	get_tree().change_scene_to_file(LEVELS[title])
