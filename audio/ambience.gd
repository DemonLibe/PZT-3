class_name Ambience
extends AudioStreamPlayer
## Фоновый звук уровня по кругу.


func _ready() -> void:
	bus = &"Ambient"
	finished.connect(play)
	play()
