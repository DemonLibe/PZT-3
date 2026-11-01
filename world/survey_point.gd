class_name SurveyPoint
extends StaticBody3D
## Точка фиксации (диктофон Вольфа) — цель вылазки. E — начать запись, затем стоять рядом record_time секунд.
## Отошёл, уснул или пропал — запись прерывается.

signal completed

const DONE_SOUND: AudioStream = preload("res://audio/sfx/count_tick.wav")

@export var record_time: float = 4.0
@export var max_distance: float = 3.0
@export var lamp: OmniLight3D
@export var indicator: GeometryInstance3D
@export var color_waiting: Color = Color(1.0, 0.25, 0.15)
@export var color_done: Color = Color(0.3, 1.0, 0.4)

var is_done: bool = false
## Прогресс записи 0–1 и кто записывает — для HUD (приходят от хоста).
var progress: float = 0.0
var recorder_path: NodePath = NodePath()

var _recorder: ExpeditionMember
var _sync_timer: float = 0.0
var _blink: float = 0.0


func _ready() -> void:
	add_to_group(&"survey_point")
	_apply_color(color_waiting)


func _process(delta: float) -> void:
	if is_done or lamp == null:
		return
	# Ожидающая точка мигает, во время записи горит ровно.
	_blink += delta
	lamp.visible = not recorder_path.is_empty() or fmod(_blink, 1.2) < 0.6


func interact(member: ExpeditionMember) -> void:
	if not NetAuthority.is_authority() or is_done or _recorder != null:
		return
	_recorder = member
	_set_progress.rpc(0.0, member.get_path())


func _physics_process(delta: float) -> void:
	if not NetAuthority.is_authority() or _recorder == null:
		return
	if not is_instance_valid(_recorder) or not _recorder.can_act() \
			or _recorder.body.global_position.distance_to(global_position) > max_distance:
		if is_instance_valid(_recorder):
			_recorder.event_received.emit(&"survey_interrupted")
		_recorder = null
		_set_progress.rpc(0.0, NodePath())
		return
	var value: float = progress + delta / record_time
	if value >= 1.0:
		_recorder.event_received.emit(&"survey_done")
		_recorder = null
		_complete.rpc()
		return
	progress = value
	_sync_timer += delta
	if _sync_timer >= 0.2:
		_sync_timer = 0.0
		_set_progress.rpc(value, recorder_path)


@rpc("authority", "call_local", "unreliable_ordered")
func _set_progress(value: float, path: NodePath) -> void:
	progress = value
	recorder_path = path


@rpc("authority", "call_local", "reliable")
func _complete() -> void:
	is_done = true
	progress = 1.0
	recorder_path = NodePath()
	if lamp:
		lamp.visible = true
	_apply_color(color_done)
	Sfx.play_at(self, DONE_SOUND, global_position + Vector3.UP, -4.0, 1.6)
	completed.emit()


func _apply_color(color: Color) -> void:
	if lamp:
		lamp.light_color = color
	var material: StandardMaterial3D = indicator.material_override as StandardMaterial3D if indicator else null
	if material:
		material.albedo_color = color
