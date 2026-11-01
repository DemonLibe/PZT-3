extends TestHarness

var events: Array = []

func _ready() -> void:
	EventBus.rule_violated.connect(func(m, id): events.append("violated:" + id))
	EventBus.member_vanished.connect(func(m): events.append("vanished"))
	EventBus.anomaly_observed.connect(func(m, id): events.append("observed:" + id))
	var room: Node = load("res://debug/test_room.tscn").instantiate()
	add_child(room)
	await frames(5)
	var m: ExpeditionMember = get_tree().get_first_node_in_group(&"local_member")
	# Повернуться к кубу: игрок в (0,0,6), куб в (5,0.5,0)
	var to_cube: Vector3 = Vector3(5, 0.5, 0) - m.get_gaze_origin()
	m.body.look_at(m.body.global_position + Vector3(to_cube.x, 0, to_cube.z))
	m.head.rotation.x = atan2(to_cube.y, Vector2(to_cube.x, to_cube.z).length())
	await frames(3)
	check(m.gaze_label == "RedCube", "смотрит на куб (%s)" % m.gaze_label)
	await wait(2.0)
	check(m.is_active(), "через 2 с ещё на месте")
	check(events.has("observed:test_cube"), "аномалия замечена")
	await wait(1.5)
	check(m.is_vanished, "через 3+ с пропал")
	check(events.has("violated:test_cube") and events.has("vanished"), "EventBus: нарушение и пропажа")
	check(not m.body.visible, "тело скрыто")
	finish()
