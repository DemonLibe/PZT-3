class_name CreatureAudio
extends Node
## Звуки существа: тяжёлые шаги при движении и, если задан, тихий напев рядом.

const STEP: AudioStream = preload("res://audio/sfx/heavy_step.wav")

@export var creature: CharacterBody3D
@export var hum: AudioStream
@export var hum_volume_db: float = -10.0
@export var step_interval: float = 0.7
@export var step_volume_db: float = -6.0

var _hum_player: AudioStreamPlayer3D
var _timer: float = 0.0
var _last_position: Vector3


func _ready() -> void:
	_last_position = creature.global_position
	if hum:
		_hum_player = AudioStreamPlayer3D.new()
		_hum_player.stream = hum
		_hum_player.bus = &"SFX"
		_hum_player.volume_db = hum_volume_db
		_hum_player.unit_size = 4.0
		_hum_player.position = Vector3(0, 2.6, 0)
		creature.add_child.call_deferred(_hum_player)
		_hum_player.finished.connect(_hum_player.play)
		_hum_player.ready.connect(_hum_player.play)


func _process(delta: float) -> void:
	# Скорость по смещению — работает и у клиента, где позицию присылает хост.
	var speed: float = creature.global_position.distance_to(_last_position) / maxf(delta, 0.0001)
	_last_position = creature.global_position
	if speed < 0.3:
		_timer = 0.0
		return
	_timer -= delta
	if _timer <= 0.0:
		_timer = step_interval * clampf(2.0 / speed, 0.4, 1.5)
		Sfx.play_at(self, STEP, creature.global_position, step_volume_db, Sfx.random_pitch(0.1))
