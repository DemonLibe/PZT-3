class_name MemberAudio
extends Node
## Звуки участника: шаги, «счёт» рядом со спящим в Районе 8, звук пропажи.
## Только читает состояние участника — работает одинаково у хоста и клиента.

const FOOTSTEP: AudioStream = preload("res://audio/sfx/footstep.wav")
const COUNT_TICK: AudioStream = preload("res://audio/sfx/count_tick.wav")
const VANISH: AudioStream = preload("res://audio/sfx/vanish.wav")
const STEP_INTERVAL: Dictionary = {
	ExpeditionMember.Motion.CROUCH: 0.75, ExpeditionMember.Motion.WALK: 0.5, ExpeditionMember.Motion.RUN: 0.32}
const STEP_VOLUME: Dictionary = {
	ExpeditionMember.Motion.CROUCH: -20.0, ExpeditionMember.Motion.WALK: -9.0, ExpeditionMember.Motion.RUN: -3.0}

@export var member: ExpeditionMember

var _step_timer: float = 0.0
var _tick_timer: float = 0.0


func _ready() -> void:
	member.vanished.connect(func(_c: StringName) -> void: Sfx.play_at(self, VANISH, member.body.global_position, -2.0))
	member.died.connect(func(_c: StringName) -> void: Sfx.play_at(self, VANISH, member.body.global_position, -6.0, 0.6))


func _process(delta: float) -> void:
	if not member.is_active():
		return
	_update_steps(delta)
	_update_counting(delta)


func _update_steps(delta: float) -> void:
	if not STEP_INTERVAL.has(member.motion) or member.is_sleeping:
		_step_timer = 0.1
		return
	_step_timer -= delta
	if _step_timer <= 0.0:
		_step_timer = STEP_INTERVAL[member.motion]
		Sfx.play_at(self, FOOTSTEP, member.body.global_position, STEP_VOLUME[member.motion], Sfx.random_pitch())


## Перед гибелью во сне рядом слышен тихий ритмичный звук, будто кто-то считает.
func _update_counting(delta: float) -> void:
	if not (member.is_sleeping and member.has_status(&"forced_sleep")):
		_tick_timer = 0.5
		return
	_tick_timer -= delta
	if _tick_timer <= 0.0:
		_tick_timer = GameState.rng.randf_range(0.95, 1.05)
		var beside: Vector3 = member.body.global_position + member.body.global_basis.x * 0.8 + Vector3(0, 0.3, 0)
		Sfx.play_at(self, COUNT_TICK, beside, -12.0, Sfx.random_pitch(0.03))
