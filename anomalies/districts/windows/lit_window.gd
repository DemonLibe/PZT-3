class_name LitWindow
extends Node3D
## Окно с тёплым светом. Гаснет и загорается по команде хоста.

const OFF_SOUND: AudioStream = preload("res://audio/sfx/light_off.wav")

@export var light: Light3D
@export var glow: GeometryInstance3D

var is_lit: bool = true

var _light_energy: float = 1.0


func _ready() -> void:
	add_to_group(&"attention_point")
	if light:
		_light_energy = light.light_energy


@rpc("authority", "call_local", "reliable")
func set_lit(value: bool) -> void:
	is_lit = value
	if light:
		light.light_energy = _light_energy if value else 0.0
	if glow:
		glow.visible = value
	if not value:
		Sfx.play_at(self, OFF_SOUND, global_position, -14.0, Sfx.random_pitch())
