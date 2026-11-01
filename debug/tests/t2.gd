extends TestHarness

var noise_events: Array = []

func _ready() -> void:
	EventBus.noise_emitted.connect(func(m, p, l): noise_events.append(l))
	var room: Node = load("res://debug/test_room.tscn").instantiate()
	add_child(room)
	await frames(10)
	var m: ExpeditionMember = get_tree().get_first_node_in_group(&"local_member")
	check(m != null, "игрок зарегистрирован как local_member")
	check(m.gaze_label == "Pillar", "цель взгляда = Pillar (%s)" % m.gaze_label)
	await wait(1.0)
	check(m.gaze_time > 0.8, "секунды взгляда растут (%.2f)" % m.gaze_time)
	check(m.noise_level == 0.0, "стоя шум 0")
	noise_events.clear()
	Input.action_press(&"move_forward")
	await wait(1.0)
	check(is_equal_approx(m.noise_level, 0.3), "шаг: шум 0.3 (%.2f)" % m.noise_level)
	check(noise_events.size() >= 3 and noise_events.size() <= 5, "noise_emitted ~4 раза в секунду (%d)" % noise_events.size())
	Input.action_press(&"sprint")
	await wait(0.5)
	check(is_equal_approx(m.noise_level, 0.8), "бег: шум 0.8 (%.2f)" % m.noise_level)
	Input.action_release(&"sprint")
	Input.action_press(&"crouch")
	await wait(0.6)
	check(is_equal_approx(m.noise_level, 0.1), "присед: шум 0.1 (%.2f)" % m.noise_level)
	check(m.head.position.y < 1.2, "голова опустилась при приседе (%.2f)" % m.head.position.y)
	Input.action_release(&"crouch")
	Input.action_release(&"move_forward")
	await wait(0.5)
	check(m.noise_level == 0.0, "остановился: шум 0")
	var z_before: float = m.body.global_position.z
	check(z_before < 5.0, "игрок прошёл вперёд (z=%.2f)" % z_before)
	# Поворот мышью: отвернуться от колонны
	m.look(PI, 0.0)
	await frames(3)
	check(m.gaze_label != "Pillar", "отвернулся — цель сменилась (%s)" % m.gaze_label)
	var ev := InputEventAction.new(); ev.action = &"flashlight"; ev.pressed = true
	Input.parse_input_event(ev)
	await frames(3)
	check(m.flashlight_on and m.flashlight.visible, "фонарь включается по F")
	finish()
