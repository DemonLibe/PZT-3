class_name DoorGapZone
extends AnomalyZone
## «Дверь» (Район 21): щель приоткрытой двери растёт линейно с каждым закрытием.
## Счётчик закрытий хранится между экспедициями.

@export var door: GapDoor

var _looked: Dictionary = {}


func _ready() -> void:
	super()
	door.zone = self
	_open_to_current.call_deferred()


func _check_rule(member: ExpeditionMember, delta: float) -> void:
	var at: Vector3 = door.global_position + Vector3(0, 1.1, 0)
	if at.distance_to(member.get_gaze_origin()) < 6.0 and member.is_in_view_cone(at, 20.0):
		observe(member)
		_looked[member] = float(_looked.get(member, 0.0)) + delta
		if _looked[member] > 3.0:
			_looked[member] = 0.0
			member.add_panic(float(param("panic_look", 0.05)))


func close_door(member: ExpeditionMember) -> void:
	if not NetAuthority.is_authority() or not member.can_act():
		return
	Encyclopedia.add_visit(&"door_closed")
	door.set_gap.rpc(0.0)


func gap_deg() -> float:
	return float(param("base_gap_deg", 3.0)) + float(param("growth_deg", 4.0)) * Encyclopedia.visits_of(&"door_closed")


func get_debug_text(_member: ExpeditionMember) -> String:
	return "Дверь: щель %.0f°, закрыта раз: %d" % [gap_deg(), Encyclopedia.visits_of(&"door_closed")]


func _open_to_current() -> void:
	if NetAuthority.is_authority():
		door.set_gap.rpc(minf(gap_deg(), 95.0))
