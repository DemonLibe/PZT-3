extends TestHarness
## Район 7 «Гости».

func _ready() -> void:
	var level := await load_level("res://levels/district_07_guests.tscn", 1)
	var zone: GuestsZone = level.get_node("GuestsZone")
	var m := local_member()
	var n: ExpeditionMember = npcs_of(level)[0]
	await press(&"squad_hold")
	zone.data.params["spawn_interval"] = 1.0
	await wait(1.5)
	var double: GuestDouble = zone.get_node_or_null("GuestDouble")
	check(double != null, "появился двойник")
	var mesh: MeshInstance3D = double.get_child(0) if double else null
	check(mesh != null and mesh.cast_shadow == GeometryInstance3D.SHADOW_CASTING_SETTING_OFF, "у двойника нет тени")
	# Игрок идёт с двойником
	double.target = m
	m.body.global_position = double.global_position + Vector3(0, 0, 1.4)
	await frames(2)
	face(m, double.global_position + Vector3(0, 1.0, 0))
	await frames(3)
	check(m.gaze_target == double, "смотрит на двойника (%s)" % m.gaze_label)
	await press(&"interact")
	await frames(3)
	check(m.is_vanished and m.fate_cause == &"guests", "пошёл «домой» — пропал")
	finish()
