class_name MirrorZone
extends AnomalyZone
## «Зеркало» (Район 5): прямой взгляд в окно. До safe_time безопасно,
## потом картинка повторяет движения с задержкой, после vanish_time — пропажа.

@export var view: MirrorView
## Узел, внутри которого лежат все окна MirrorWindow.
@export var windows_root: Node

var _windows: Array[MirrorWindow] = []
## member -> {"look": секунды прямого взгляда, "away": секунды без взгляда, "window": окно}
var _states: Dictionary = {}


func _ready() -> void:
	super()
	for child in windows_root.find_children("*", "MirrorWindow", true, false):
		var window: MirrorWindow = child
		_windows.append(window)
		window.set_view_texture(view.get_texture())


func _check_rule(member: ExpeditionMember, delta: float) -> void:
	var state: Dictionary = _state(member)
	var window: MirrorWindow = _direct_window(member)
	if window:
		state["away"] = 0.0
		state["window"] = window
		var multiplier: float = float(param("flash_multiplier", 3.0)) if member.has_status(&"camera_flash") else 1.0
		state["look"] += delta * multiplier
		observe(member)
	else:
		state["away"] += delta
		if state["away"] > float(param("reset_after", 1.0)):
			state["look"] = 0.0
	_update_mimic(member, state)
	if state["look"] >= float(param("vanish_time", 15.0)):
		var looked_at: MirrorWindow = state["window"]
		_states.erase(member)
		_update_mimic(member, {"look": 0.0})
		violate(member)
		if looked_at and not looked_at.is_cracked:
			looked_at.crack.rpc()


func _on_member_exited(member: ExpeditionMember) -> void:
	_states.erase(member)
	_update_mimic(member, {"look": 0.0})


func get_debug_text(member: ExpeditionMember) -> String:
	if not _states.has(member):
		return ""
	var state: Dictionary = _states[member]
	return "Зеркало: взгляд %.1f с (безопасно до %.0f, пропажа %.0f), отвёл %.1f с" % [
		state["look"], float(param("safe_time", 4.0)), float(param("vanish_time", 15.0)), state["away"]]


func _state(member: ExpeditionMember) -> Dictionary:
	if not _states.has(member):
		_states[member] = {"look": 0.0, "away": 0.0, "window": null}
	return _states[member]


## Окно, в которое участник смотрит прямо (в узком конусе и без преград).
func _direct_window(member: ExpeditionMember) -> MirrorWindow:
	var cone: float = float(param("direct_cone_deg", 10.0))
	for window in _windows:
		if member.is_in_view_cone(window.global_position, cone) and _has_line_of_sight(member, window):
			return window
	return null


func _has_line_of_sight(member: ExpeditionMember, window: MirrorWindow) -> bool:
	var query: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(
		member.get_gaze_origin(), window.global_position, 1)
	var hit: Dictionary = get_world_3d().direct_space_state.intersect_ray(query)
	if hit.is_empty():
		return true
	return window.is_ancestor_of(hit["collider"]) or hit["position"].distance_to(window.global_position) < 0.3


func _update_mimic(member: ExpeditionMember, state: Dictionary) -> void:
	var mimicking: bool = state["look"] > float(param("safe_time", 4.0))
	if mimicking and view.mimic_member != member:
		_set_mimic.rpc(member.get_path())
	elif not mimicking and view.mimic_member == member:
		_set_mimic.rpc(NodePath())


@rpc("authority", "call_local", "reliable")
func _set_mimic(member_path: NodePath) -> void:
	var member: ExpeditionMember = get_node_or_null(member_path) as ExpeditionMember if not member_path.is_empty() else null
	view.set_mimic(member, float(param("mimic_delay", 0.5)))
