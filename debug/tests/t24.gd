extends TestHarness
## Район 21 «Дверь»: щель растёт с каждым закрытием.

func _ready() -> void:
	Encyclopedia.reset()
	var level := await load_level("res://levels/district_21_door.tscn", 0)
	var zone: DoorGapZone = level.get_node("DoorGapZone")
	var m := local_member()
	var gap0: float = zone.gap_deg()
	var door: Node3D = level.get_node("GapDoor")
	m.body.global_position = Vector3(-12.6, 0.1, 6.0)
	await frames(2)
	face(m, door.global_position + Vector3(0, 1.0, 0.0))
	await frames(3)
	check(m.gaze_target == door, "смотрит на дверь (%s)" % m.gaze_label)
	await press(&"interact")
	await frames(3)
	check(Encyclopedia.visits_of(&"door_closed") == 1 and zone.gap_deg() > gap0, "закрыл — в следующий раз щель шире (%.0f° → %.0f°)" % [gap0, zone.gap_deg()])
	finish()
