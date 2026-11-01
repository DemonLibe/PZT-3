extends Node
## Настройки игрока: мышь, громкость, PS1-вид, полный экран. Хранятся в user://settings.cfg.

signal changed

const PATH: String = "user://settings.cfg"

var mouse_sensitivity: float = 1.0
var master_volume: float = 0.8
var ambient_volume: float = 0.8
var sfx_volume: float = 1.0
var ps1_enabled: bool = true
var fullscreen: bool = false


func _ready() -> void:
	load_settings()
	apply()


func apply() -> void:
	_set_bus_volume(&"Master", master_volume)
	_set_bus_volume(&"Ambient", ambient_volume)
	_set_bus_volume(&"SFX", sfx_volume)
	RetroRender.set_enabled(ps1_enabled)
	if DisplayServer.get_name() != "headless":
		var mode: DisplayServer.WindowMode = DisplayServer.WINDOW_MODE_FULLSCREEN if fullscreen else DisplayServer.WINDOW_MODE_WINDOWED
		if DisplayServer.window_get_mode() != mode:
			DisplayServer.window_set_mode(mode)
	changed.emit()


func save_settings() -> void:
	var config: ConfigFile = ConfigFile.new()
	for key in ["mouse_sensitivity", "master_volume", "ambient_volume", "sfx_volume", "ps1_enabled", "fullscreen"]:
		config.set_value("settings", key, get(key))
	config.save(PATH)


func load_settings() -> void:
	var config: ConfigFile = ConfigFile.new()
	if config.load(PATH) != OK:
		return
	for key in config.get_section_keys("settings"):
		if key in self:
			set(key, config.get_value("settings", key))


func _set_bus_volume(bus_name: StringName, linear: float) -> void:
	var index: int = AudioServer.get_bus_index(bus_name)
	if index < 0:
		return
	AudioServer.set_bus_mute(index, linear <= 0.001)
	AudioServer.set_bus_volume_db(index, linear_to_db(maxf(linear, 0.001)))
