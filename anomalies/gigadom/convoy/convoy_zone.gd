class_name ConvoyZone
extends AnomalyZone
## «Пустой конвой» (Секция 48): через равные интервалы по главному коридору проходит строй
## безликих фигур. При звуке шагов — остановиться, встать смирно лицом к стене до полного
## прохождения. Иначе строй останавливается и разворачивается — последняя запись группы.

const STEP: AudioStream = preload("res://audio/sfx/heavy_step.wav")

@export var column: Node3D
@export var path_start: Node3D
@export var path_end: Node3D

enum Phase { QUIET, WARNING, MARCH }

var phase: Phase = Phase.QUIET
var _timer: float = 0.0
var _step: float = 0.0
var _npc_ok: Dictionary = {}


func _ready() -> void:
	super()
	column.visible = false


func _physics_process(delta: float) -> void:
	super(delta)
	if not NetAuthority.is_authority():
		return
	_timer += delta
	match phase:
		Phase.QUIET:
			if _timer >= float(param("interval", 45.0)):
				_set_phase.rpc(Phase.WARNING)
		Phase.WARNING:
			_drum(delta)
			if _timer >= float(param("warning_time", 5.0)):
				_set_phase.rpc(Phase.MARCH)
		Phase.MARCH:
			_drum(delta)
			var t: float = _timer / float(param("march_time", 10.0))
			_move_column.rpc(path_start.global_position.lerp(path_end.global_position, clampf(t, 0.0, 1.0)))
			if t >= 1.0:
				_set_phase.rpc(Phase.QUIET)


func _check_rule(member: ExpeditionMember, _delta: float) -> void:
	if phase != Phase.MARCH:
		return
	observe(member)
	if _at_attention(member):
		return
	_halt.rpc()
	var squad: Squad = get_tree().get_first_node_in_group(&"squad") as Squad
	for other in (squad.active_members() if squad else [member]):
		violate(other)
	_set_phase.rpc(Phase.QUIET)


func get_debug_text(member: ExpeditionMember) -> String:
	return "Конвой: %s%s" % [["тихо", "ШАГИ СТРОЯ", "СТРОЙ ИДЁТ"][phase], " — смирно у стены" if _at_attention(member) else ""]


## Стоит неподвижно лицом к стене (в шаге от неё).
func _at_attention(member: ExpeditionMember) -> bool:
	if member.auto_doors:
		if not _npc_ok.has(member):
			_npc_ok[member] = GameState.rng.randf() < float(param("npc_discipline", 0.85)) - member.panic * 0.5
		return _npc_ok[member]
	if member.motion != ExpeditionMember.Motion.IDLE:
		return false
	var from: Vector3 = member.get_gaze_origin()
	var query: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(from, from + member.get_gaze_direction() * 1.3, 1)
	return not get_world_3d().direct_space_state.intersect_ray(query).is_empty()


func _drum(delta: float) -> void:
	_step -= delta
	if _step <= 0.0:
		_step = 0.5
		_play_step.rpc(column.global_position if column.visible else path_start.global_position)


@rpc("authority", "call_local", "reliable")
func _set_phase(value: Phase) -> void:
	phase = value
	_timer = 0.0
	_npc_ok.clear()
	column.visible = value == Phase.MARCH
	if value == Phase.WARNING:
		EventBus.radio_message.emit("Мельников", "Шаги строя! К стене, смирно!")


@rpc("authority", "call_local", "unreliable_ordered")
func _move_column(at: Vector3) -> void:
	column.global_position = at


@rpc("authority", "call_local", "reliable")
func _halt() -> void:
	column.rotate_y(PI / 2.0)


@rpc("authority", "call_local", "unreliable")
func _play_step(at: Vector3) -> void:
	Sfx.play_at(self, STEP, at, -2.0, 0.8)
