class_name MirrorWindow
extends MeshInstance3D
## Окно «Зеркала». Стекло показывает картинку из MirrorView.

const CRACK_SOUND: AudioStream = preload("res://audio/sfx/light_off.wav")
const GLASS_SHADER: Shader = preload("res://anomalies/districts/mirror/mirror_glass.gdshader")

var is_cracked: bool = false

var _material: ShaderMaterial


func _ready() -> void:
	add_to_group(&"attention_point")
	_material = ShaderMaterial.new()
	_material.shader = GLASS_SHADER
	material_override = _material


func set_view_texture(texture: Texture2D) -> void:
	_material.set_shader_parameter(&"view_tex", texture)


## Стекло треснуло изнутри. Вызывается хостом для всех.
@rpc("authority", "call_local", "reliable")
func crack() -> void:
	is_cracked = true
	Sfx.play_at(self, CRACK_SOUND, global_position, -4.0, 0.45)
	_material.set_shader_parameter(&"cracked", 1.0)
