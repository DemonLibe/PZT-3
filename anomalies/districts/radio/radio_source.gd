class_name RadioSource
extends AudioStreamPlayer3D
## Приёмник в доме: по кругу бормочет эфир.


func _ready() -> void:
	bus = &"SFX"
	finished.connect(play)
	play()
