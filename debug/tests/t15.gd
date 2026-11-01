extends TestHarness
## Район 9 «Улыбка».

func _ready() -> void:
	var level := await load_level("res://levels/district_09_smile.tscn", 0)
	var m := local_member()
	var face: Node3D = level.get_node("Faces/WindowFace1")
	m.body.global_position = face.global_position + Vector3(5, 0, 0)
	m.body.global_position.y = 0
	await frames(2)
	face(m, face.global_position)
	await wait(1.5)
	check(not m.has_status(&"smiled"), "1.5 с — ещё держится")
	face(m, face.global_position + Vector3(0, 0, 8))
	await wait(1.0)
	face(m, face.global_position)
	await wait(1.5)
	check(not m.has_status(&"smiled"), "отвёл взгляд — порыв ослаб")
	await wait(1.5)
	check(m.has_status(&"smiled"), "долгий прямой взгляд — улыбнулся в ответ")
	GameState.debug_skip_hours(5.5)
	await wait(0.3)
	check(m.has_status(&"smile_fixed"), "через несколько часов улыбка зафиксировалась")
	finish()
