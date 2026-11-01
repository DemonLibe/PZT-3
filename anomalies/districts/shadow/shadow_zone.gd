class_name ShadowZone
extends AnomalyZone
## «Тень» (Район 6): при особом свете тень иногда указывает за спину.
## Обернуться, пока она указывает (больше turn_deg за turn_window с), — пропажа.

const FIGURE_SCENE: PackedScene = preload("res://anomalies/districts/shadow/shadow_figure.tscn")

## Особый источник света.
@export var light: Node3D

## member -> {"until": конец указания, "history": [[время, накопленный угол]], "acc": угол, "yaw": прошлый yaw}
var _pointing: Dictionary = {}
var _figures: Dictionary = {}
var _clock: float = 0.0
var _check_timer: float = 0.0


func _physics_process(delta: float) -> void:
	_clock += delta
	super(delta)
	if not NetAuthority.is_authority():
		return
	_check_timer += delta
	if _check_timer >= float(param("check_interval", 5.0)):
		_check_timer = 0.0
		for member in members:
			if member.is_active() and not _pointing.has(member) \
					and GameState.rng.randf() < float(param("point_chance", 0.15)):
				_start_pointing(member)


func _check_rule(member: ExpeditionMember, _delta: float) -> void:
	if not _pointing.has(member):
		return
	var state: Dictionary = _pointing[member]
	if _clock >= state["until"]:
		_stop_pointing(member)
		return
	var yaw: float = member.body.global_rotation.y
	state["acc"] += rad_to_deg(angle_difference(state["yaw"], yaw))
	state["yaw"] = yaw
	var history: Array = state["history"]
	history.append([_clock, state["acc"]])
	while history.size() > 1 and history[0][0] < _clock - float(param("turn_window", 1.0)):
		history.pop_front()
	for entry in history:
		if absf(state["acc"] - entry[1]) > float(param("turn_deg", 150.0)):
			_stop_pointing(member)
			violate(member)
			return


func _on_member_exited(member: ExpeditionMember) -> void:
	if _pointing.has(member):
		_stop_pointing(member)


func get_debug_text(member: ExpeditionMember) -> String:
	if not _pointing.has(member):
		return "Тень: повторяет движения"
	return "Тень: УКАЗЫВАЕТ ещё %.1f с" % (float(_pointing[member]["until"]) - _clock)


func _start_pointing(member: ExpeditionMember) -> void:
	var yaw: float = member.body.global_rotation.y
	_pointing[member] = {"until": _clock + float(param("point_duration", 6.0)),
		"history": [], "acc": 0.0, "yaw": yaw}
	observe(member)
	_show_figure.rpc(member.get_path(), true)


func _stop_pointing(member: ExpeditionMember) -> void:
	_pointing.erase(member)
	_show_figure.rpc(member.get_path(), false)


@rpc("authority", "call_local", "reliable")
func _show_figure(member_path: NodePath, value: bool) -> void:
	var member: ExpeditionMember = get_node_or_null(member_path) as ExpeditionMember
	if member == null:
		return
	if not _figures.has(member_path):
		var figure: ShadowFigure = FIGURE_SCENE.instantiate()
		add_child(figure)
		figure.visible = false
		_figures[member_path] = figure
	var figure: ShadowFigure = _figures[member_path]
	if value:
		figure.point_behind(member.body, light.global_position if light else global_position + Vector3.UP * 5.0)
	else:
		figure.stop()
