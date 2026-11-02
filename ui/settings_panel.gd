extends VBoxContainer
## Панель настроек: меняет Settings сразу и сохраняет.


func _ready() -> void:
	%Sensitivity.value = Settings.mouse_sensitivity
	%Brightness.value = Settings.brightness
	%Master.value = Settings.master_volume
	%Ambient.value = Settings.ambient_volume
	%Sfx.value = Settings.sfx_volume
	%Ps1.button_pressed = Settings.ps1_enabled
	%Jitter.button_pressed = Settings.vertex_jitter
	%Fullscreen.button_pressed = Settings.fullscreen
	%Sensitivity.value_changed.connect(_on_changed.bind("mouse_sensitivity"))
	%Brightness.value_changed.connect(_on_changed.bind("brightness"))
	%Master.value_changed.connect(_on_changed.bind("master_volume"))
	%Ambient.value_changed.connect(_on_changed.bind("ambient_volume"))
	%Sfx.value_changed.connect(_on_changed.bind("sfx_volume"))
	%Ps1.toggled.connect(_on_changed.bind("ps1_enabled"))
	%Jitter.toggled.connect(_on_changed.bind("vertex_jitter"))
	%Fullscreen.toggled.connect(_on_changed.bind("fullscreen"))


func _on_changed(value: Variant, key: String) -> void:
	Settings.set(key, value)
	Settings.apply()
	Settings.save_settings()
