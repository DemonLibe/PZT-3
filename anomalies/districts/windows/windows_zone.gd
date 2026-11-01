class_name WindowsZone
extends AnomalyZone
## «Окна» (Район 2): свет в окне гаснет, когда к нему поворачивают взгляд.
## Наказания нет — только паника от резких поворотов.

@export var windows_root: Node

var _windows: Array[LitWindow] = []
## member -> направление взгляда в прошлом кадре
var _prev_dir: Dictionary = {}
## member -> поворачивал ли резко в прошлом кадре (паника — один раз за поворот)
var _was_sharp: Dictionary = {}
## window -> {"off_at": время, когда погаснет, "on_at": когда загорится}
var _timers: Dictionary = {}
var _clock: float = 0.0


func _ready() -> void:
	super()
	for child in windows_root.find_children("*", "LitWindow", true, false):
		_windows.append(child)


func _physics_process(delta: float) -> void:
	super(delta)
	if not NetAuthority.is_authority():
		return
	_clock += delta
	for window in _timers.keys():
		var timer: Dictionary = _timers[window]
		if timer.has("off_at") and _clock >= timer["off_at"]:
			timer.erase("off_at")
			timer["on_at"] = _clock + float(param("relight_after", 6.0))
			window.set_lit.rpc(false)
		elif timer.has("on_at") and _clock >= timer["on_at"]:
			_timers.erase(window)
			window.set_lit.rpc(true)


func _check_rule(member: ExpeditionMember, delta: float) -> void:
	var dir: Vector3 = member.get_gaze_direction()
	var prev: Vector3 = _prev_dir.get(member, dir)
	_prev_dir[member] = dir
	var speed: float = rad_to_deg(prev.angle_to(dir)) / maxf(delta, 0.0001)
	var sharp: bool = speed > float(param("sharp_turn_deg_per_sec", 180.0))
	if sharp and not _was_sharp.get(member, false):
		member.add_panic(float(param("panic_add", 0.05)))
	_was_sharp[member] = sharp
	var half_cone: float = float(param("cone_deg", 25.0)) * 0.5
	for window in _windows:
		if not window.is_lit or _timers.has(window):
			continue
		var to_window: Vector3 = (window.global_position - member.get_gaze_origin()).normalized()
		var angle_now: float = rad_to_deg(dir.angle_to(to_window))
		var angle_prev: float = rad_to_deg(prev.angle_to(to_window))
		# Окно вошло в конус, и взгляд к нему поворачивается.
		if angle_now <= half_cone and angle_now < angle_prev - 0.01:
			var delay: float = GameState.rng.randf_range(float(param("delay_min", 0.5)), float(param("delay_max", 1.0)))
			_timers[window] = {"off_at": _clock + delay}
			observe(member)


func _on_member_exited(member: ExpeditionMember) -> void:
	_prev_dir.erase(member)
	_was_sharp.erase(member)


func get_debug_text(_member: ExpeditionMember) -> String:
	var lit: int = _windows.filter(func(w: LitWindow) -> bool: return w.is_lit).size()
	return "Окна: горит %d из %d" % [lit, _windows.size()]
