class_name BarracksZone
extends AnomalyZone
## «Казармы» (Секция 33): радиоузел в случайные моменты отдаёт военные команды.
## Не выполнил точно и сразу — приходит «прапорщик». Спасение: громко сказать
## «Виноват, господин прапорщик» до того, как он подойдёт (срабатывает не всегда).

const COMMANDS: Dictionary = {
	"Лечь!": "crouch", "Смирно!": "idle", "Шагом марш!": "walk", "Бегом марш!": "run",
}

@export var prapor: Node3D
@export var prapor_start: Node3D

var _command: String = ""
var _deadline: float = 0.0
var _next: float = 15.0
var _clock: float = 0.0
var _victim: ExpeditionMember


func _ready() -> void:
	super()
	add_to_group(&"speech_context")
	EventBus.member_spoke.connect(_on_spoke)
	prapor.visible = false


func _physics_process(delta: float) -> void:
	_clock += delta
	super(delta)
	if not NetAuthority.is_authority():
		return
	if _victim:
		_hunt(delta)
	elif _command == "" and _clock >= _next and not members.is_empty():
		_command = COMMANDS.keys()[GameState.rng.randi_range(0, COMMANDS.size() - 1)]
		_deadline = _clock + float(param("react_time", 3.0))
		_announce.rpc(_command)
	elif _command != "" and _clock >= _deadline:
		_judge()


func speech_phrase(member: ExpeditionMember) -> String:
	return "Виноват, господин прапорщик!" if member == _victim else ""


func get_debug_text(_member: ExpeditionMember) -> String:
	if _victim:
		return "Казармы: прапорщик идёт к %s" % _victim.display_name
	if _command != "":
		return "Казармы: команда «%s», осталось %.1f с" % [_command, _deadline - _clock]
	return "Казармы: тишина"


func _judge() -> void:
	var wanted: String = COMMANDS[_command]
	_command = ""
	_next = _clock + GameState.rng.randf_range(float(param("interval_min", 20.0)), float(param("interval_max", 40.0)))
	for member in members:
		if not member.is_active():
			continue
		observe(member)
		var complied: bool = _complies(member, wanted)
		if member.auto_doors:  # напарник: дисциплина против паники
			complied = GameState.rng.randf() < float(param("npc_discipline", 0.75)) - member.panic * 0.5
		if not complied:
			_victim = member
			EventBus.rule_violated.emit(member, data.id)
			_show_prapor.rpc(true, prapor_start.global_position)
			return


func _complies(member: ExpeditionMember, wanted: String) -> bool:
	match wanted:
		"crouch":
			return member.head.position.y < 1.2
		"idle":
			return member.motion == ExpeditionMember.Motion.IDLE
		"walk":
			return member.motion == ExpeditionMember.Motion.WALK
		"run":
			return member.motion == ExpeditionMember.Motion.RUN
	return true


func _hunt(delta: float) -> void:
	if not _victim.is_active():
		_victim = null
		_show_prapor.rpc(false, prapor.global_position)
		return
	var to: Vector3 = _victim.body.global_position - prapor.global_position
	to.y = 0.0
	if to.length() < 1.2:
		var victim: ExpeditionMember = _victim
		_victim = null
		_show_prapor.rpc(false, prapor.global_position)
		data.punishment.apply(victim, data.id)
		return
	prapor.global_position += to.normalized() * float(param("prapor_speed", 1.6)) * delta
	prapor.look_at(prapor.global_position + to.normalized(), Vector3.UP)


func _on_spoke(member: Node, _phrase: String) -> void:
	if not NetAuthority.is_authority() or member != _victim:
		return
	if GameState.rng.randf() < float(param("apology_success", 0.667)):
		_victim = null
		_show_prapor.rpc(false, prapor.global_position)


@rpc("authority", "call_local", "reliable")
func _announce(command: String) -> void:
	EventBus.radio_message.emit("Радиоузел", command)


@rpc("authority", "call_local", "reliable")
func _show_prapor(value: bool, at: Vector3) -> void:
	prapor.visible = value
	prapor.global_position = at
