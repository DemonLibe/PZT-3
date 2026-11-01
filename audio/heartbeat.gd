class_name Heartbeat
extends Node
## Сердцебиение локального игрока: чем выше паника, тем чаще и громче.

const BEAT: AudioStream = preload("res://audio/sfx/heartbeat.wav")

@export var member: ExpeditionMember
@export var calm_interval: float = 1.3
@export var panic_interval: float = 0.45
## Ниже этой паники сердце не слышно.
@export var audible_from: float = 0.1

var _player: AudioStreamPlayer
var _timer: float = 0.0


func _ready() -> void:
	_player = AudioStreamPlayer.new()
	_player.stream = BEAT
	_player.bus = &"Body"
	add_child(_player)


func _process(delta: float) -> void:
	if not member.is_in_group(&"local_member") or not member.is_active() or member.panic < audible_from:
		return
	_timer -= delta
	if _timer > 0.0:
		return
	var t: float = clampf((member.panic - audible_from) / (1.0 - audible_from), 0.0, 1.0)
	_timer = lerpf(calm_interval, panic_interval, t)
	_player.volume_db = lerpf(-26.0, -4.0, t)
	_player.play()
