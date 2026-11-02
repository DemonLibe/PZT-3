extends Node
## Настройки игрока: мышь, громкость, PS1-вид, полный экран. Хранятся в user://settings.cfg.

signal changed

const PATH: String = "user://settings.cfg"

var mouse_sensitivity: float = 1.0
var master_volume: float = 0.8
var ambient_volume: float = 0.8
var sfx_volume: float = 1.0
var ps1_enabled: bool = true
## Дрожание вершин в духе PS1 (по умолчанию выключено: свет на стенах «плавает»).
var vertex_jitter: bool = false
## Яркость картинки (1 — как задумано в уровне).
var brightness: float = 1.6
var fullscreen: bool = false


func _ready() -> void:
	load_settings()
	get_tree().node_added.connect(_on_node_added)
	apply()


func apply() -> void:
	_set_bus_volume(&"Master", master_volume)
	_set_bus_volume(&"Ambient", ambient_volume)
	_set_bus_volume(&"SFX", sfx_volume)
	RetroRender.set_enabled(ps1_enabled)
	RetroRender.set_vertex_jitter(vertex_jitter)
	for node in get_tree().root.find_children("*", "WorldEnvironment", true, false):
		_apply_brightness(node)
	if DisplayServer.get_name() != "headless":
		var mode: DisplayServer.WindowMode = DisplayServer.WINDOW_MODE_FULLSCREEN if fullscreen else DisplayServer.WINDOW_MODE_WINDOWED
		if DisplayServer.window_get_mode() != mode:
			DisplayServer.window_set_mode(mode)
	changed.emit()


func save_settings() -> void:
	var config: ConfigFile = ConfigFile.new()
	for key in ["mouse_sensitivity", "master_volume", "ambient_volume", "sfx_volume", "ps1_enabled", "fullscreen", "brightness", "vertex_jitter"]:
		config.set_value("settings", key, get(key))
	config.save(PATH)


func load_settings() -> void:
	var config: ConfigFile = ConfigFile.new()
	if config.load(PATH) != OK:
		return
	for key in config.get_section_keys("settings"):
		if key in self:
			set(key, config.get_value("settings", key))


func _on_node_added(node: Node) -> void:
	if node is WorldEnvironment:
		_apply_brightness.call_deferred(node)


func _apply_brightness(world: WorldEnvironment) -> void:
	if not is_instance_valid(world) or world.environment == null:
		return
	world.environment.adjustment_enabled = true
	world.environment.adjustment_brightness = brightness


func _set_bus_volume(bus_name: StringName, linear: float) -> void:
	var index: int = AudioServer.get_bus_index(bus_name)
	if index < 0:
		return
	AudioServer.set_bus_mute(index, linear <= 0.001)
	AudioServer.set_bus_volume_db(index, linear_to_db(maxf(linear, 0.001)))
