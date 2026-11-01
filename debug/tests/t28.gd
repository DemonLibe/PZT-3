extends TestHarness
## Район 28 «Дыхание стен».

func _ready() -> void:
	var level := await load_level("res://levels/district_28_walls.tscn", 0)
	var zone: BreathingWallsZone = level.get_node("BreathingWallsZone")
	var m := local_member()
	var wall: Node3D = level.get_node("Walls/Wall1")
	zone.data.params["touch_limit"] = 1.5
	m.body.global_position = wall.global_position + Vector3(1.0, -1.3, 0)
	await frames(2)
	face(m, wall.global_position)
	await frames(3)
	await press(&"interact")
	await wait(2.0)
	check(m.has_status(&"wall_pulse"), "ладонь на стене дольше лимита — пульс следует за стеной")
	zone.data.params["touch_limit"] = 60.0
	finish()
