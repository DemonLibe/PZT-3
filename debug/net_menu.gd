extends Control
## Отладочное меню сети: соло, хост или подключение к 127.0.0.1.

@onready var _level_select: OptionButton = %LevelSelect
@onready var _address: LineEdit = %Address
@onready var _status: Label = %Status


func _ready() -> void:
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	for destination in Destinations.LIST:
		_level_select.add_item(destination["title"])
	_level_select.select(2)
	_status.text = NetAuthority.last_error
	%SoloButton.pressed.connect(_start.bind(NetAuthority.Mode.SOLO))
	%HostButton.pressed.connect(_start.bind(NetAuthority.Mode.HOST))
	%JoinButton.pressed.connect(_start.bind(NetAuthority.Mode.CLIENT))
	%BackButton.pressed.connect(get_tree().change_scene_to_file.bind(GameState.BASE_SCENE))


func _start(mode: NetAuthority.Mode) -> void:
	NetAuthority.last_error = ""
	NetAuthority.prepare(mode, _address.text.strip_edges())
	GameState.begin_expedition(Destinations.LIST[_level_select.selected])
