class_name MemberAudio
extends Node
## Звуки участника: шаги (записи CC0), «счёт» рядом со спящим в Районе 8, звук пропажи.
## Свои шаги игрок слышит без 3D-эффекта, чужие — из точки, где идёт участник.

const STEPS: Array[AudioStream] = [
	preload("res://audio/steps/01-footstep_0.ogg"), preload("res://audio/steps/02-footstep.ogg"),
	preload("res://audio/steps/03-footstep.ogg"), preload("res://audio/steps/04-footstep.ogg"),
	preload("res://audio/steps/05-footstep.ogg"), preload("res://audio/steps/06-footstep.ogg"),
]
const COUNT_TICK: AudioStream = preload("res://audio/sfx/count_tick.wav")
const VANISH: AudioStream = preload("res://audio/sfx/vanish.wav")
const STEP_INTERVAL: Dictionary = {
	ExpeditionMember.Motion.CROUCH: 0.8, ExpeditionMember.Motion.WALK: 0.55, ExpeditionMember.Motion.RUN: 0.34}
const STEP_VOLUME: Dictionary = {
	ExpeditionMember.Motion.CROUCH: -26.0, ExpeditionMember.Motion.WALK: -16.0, ExpeditionMember.Motion.RUN: -10.0}

@export var member: ExpeditionMember

var _step_timer: float = 0.0
var _tick_timer: float = 0.0
var _last_step: int = -1
var _own: AudioStreamPlayer


func _ready() -> void:
	_own = AudioStreamPlayer.new()
	_own.bus = &"Body"
	add_child(_own)
	member.vanished.connect(func(_c: StringName) -> void: Sfx.play_at(self, VANISH, member.body.global_position, -2.0))
	member.died.connect(func(_c: StringName) -> void: Sfx.play_at(self, VANISH, member.body.global_position, -6.0, 0.6))


func _process(delta: float) -> void:
	if not member.is_active():
		return
	_update_steps(delta)
	_update_counting(delta)


func _update_steps(delta: float) -> void:
	if not STEP_INTERVAL.has(member.motion) or member.is_sleeping:
		_step_timer = 0.12  # первый шаг — почти сразу, как тронулся
		return
	_step_timer -= delta
	if _step_timer > 0.0:
		return
	_step_timer = STEP_INTERVAL[member.motion] * GameState.rng.randf_range(0.95, 1.05)
	var index: int = GameState.rng.randi_range(0, STEPS.size() - 1)
	if index == _last_step:
		index = (index + 1) % STEPS.size()  # не повторять один и тот же шаг подряд
	_last_step = index
	var volume: float = STEP_VOLUME[member.motion]
	if member.is_in_group(&"local_member"):
		_own.stream = STEPS[index]
		_own.volume_db = volume
		_own.pitch_scale = GameState.rng.randf_range(0.92, 1.06)
		_own.play()
	else:
		Sfx.play_at(self, STEPS[index], member.body.global_position, volume + 4.0, GameState.rng.randf_range(0.92, 1.06))


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
