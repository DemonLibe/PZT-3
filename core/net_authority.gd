extends Node
## Кто управляет логикой мира. Сеть — на этапе 5, пока всегда SOLO.

enum Mode { SOLO, HOST, CLIENT }

var mode: Mode = Mode.SOLO


func _ready() -> void:
	print("[NetAuthority] готов, режим: ", Mode.keys()[mode])


## true — этот экземпляр игры вправе менять состояние мира.
func is_authority() -> bool:
	return mode != Mode.CLIENT
