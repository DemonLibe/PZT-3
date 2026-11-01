class_name MemberNoise
extends Node
## Шум участника: считает noise_level по движению и раз в noise_interval
## сообщает в EventBus.noise_emitted. Работает только на авторитетной стороне.

@export var member: ExpeditionMember
@export var noise_crouch: float = 0.1
@export var noise_walk: float = 0.3
@export var noise_run: float = 0.8
@export var noise_interval: float = 0.25

var _timer: float = 0.0


func _physics_process(delta: float) -> void:
	if not NetAuthority.is_authority() or member == null:
		return
	member.noise_level = _noise_for_motion()
	_timer += delta
	if _timer < noise_interval:
		return
	_timer = 0.0
	if member.noise_level > 0.0:
		EventBus.noise_emitted.emit(member, member.body.global_position, member.noise_level)


func _noise_for_motion() -> float:
	if not member.can_act() or member.is_eating:
		return 0.0
	match member.motion:
		ExpeditionMember.Motion.CROUCH:
			return noise_crouch
		ExpeditionMember.Motion.WALK:
			return noise_walk
		ExpeditionMember.Motion.RUN:
			return noise_run
	return 0.0
