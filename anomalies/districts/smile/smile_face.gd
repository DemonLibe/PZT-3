class_name SmileFace
extends MeshInstance3D
## Лицо с растянутой улыбкой: в окне, на фотографии, в отражении.


func _ready() -> void:
	add_to_group(&"attention_point")
	add_to_group(&"smile_face")
