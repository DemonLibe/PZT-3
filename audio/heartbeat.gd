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
var _muted: bool = false


func _ready() -> void:
	_player = AudioStreamPlayer.new()
	_player.stream = BEAT
	_player.bus = &"Body"
	add_child(_player)


func _process(delta: float) -> void:
	if not member.is_in_group(&"local_member"):
		return
	_update_silence()
	if not member.is_active():
		return
	if member.has_status(&"silence") or member.has_status(&"wall_pulse"):
		# В «Тишине» и после «Дыхания стен» слышно только своё сердце — и его ритм идёт от пульса участника.
		_timer -= delta
		if _timer <= 0.0:
			_timer = 60.0 / maxf(member.pulse_bpm, 20.0)
			_player.volume_db = -2.0
			_player.play()
		return
	if member.panic < audible_from:
		return
	_timer -= delta
	if _timer > 0.0:
		return
	var t: float = clampf((member.panic - audible_from) / (1.0 - audible_from), 0.0, 1.0)
	_timer = lerpf(calm_interval, panic_interval, t)
	_player.volume_db = lerpf(-26.0, -4.0, t)
	_player.play()


## Глушим всё, кроме сердца, пока участник в «Тишине».
func _update_silence() -> void:
	var silent: bool = member.is_active() and member.has_status(&"silence")
	if silent == _muted:
		return
	_muted = silent
	for bus_name in [&"SFX", &"Ambient"]:
		var index: int = AudioServer.get_bus_index(bus_name)
		if index >= 0:
			AudioServer.set_bus_mute(index, silent)
	if not silent:
		Settings.apply()
