extends TestHarness
## Секция 33 «Казармы».

var orders: Array = []

func _ready() -> void:
	EventBus.radio_message.connect(func(sp, t): if sp == "Радиоузел": orders.append(t))
	var level := await load_level("res://levels/section_33_barracks.tscn", 0)
	level.loss_delay = 9999.0
	var zone: BarracksZone = level.get_node("BarracksZone")
	var m := local_member()
	m.body.global_position = Vector3(0, 0, 5)
	zone._next = 0.0
	await wait(0.5)
	check(orders.size() == 1, "радиоузел отдал команду: " + (orders[0] if orders else "-"))
	# Выполнить команду
	var cmd: String = orders[0]
	if cmd == "Лечь!": Input.action_press(&"crouch")
	elif cmd == "Шагом марш!": Input.action_press(&"move_forward")
	elif cmd == "Бегом марш!": Input.action_press(&"move_forward"); Input.action_press(&"sprint")
	await wait(3.2)
	for a in [&"crouch", &"move_forward", &"sprint"]: Input.action_release(a)
	check(zone._victim == null, "команда выполнена — прапорщика нет")
	# Не выполнить следующую (стоим, когда велят бежать)
	zone._command = "Бегом марш!"
	zone._deadline = zone._clock + 0.2
	await wait(0.5)
	check(zone._victim == m and level.get_node("Prapor").visible, "не выполнил — идёт прапорщик")
	zone.data.params["apology_success"] = 1.0
	await press(&"speak")
	await frames(3)
	check(zone._victim == null and not level.get_node("Prapor").visible, "«Виноват, господин прапорщик» — ушёл")
	zone.data.params["apology_success"] = 0.667
	zone._command = "Бегом марш!"
	zone._deadline = zone._clock + 0.2
	level.get_node("PraporStart").global_position = m.body.global_position + Vector3(0, 0, -3)
	for i in 20:
		await wait(0.25)
		if not m.is_alive: break
	check(not m.is_alive and m.fate_cause == &"barracks", "не успел — загнан до смерти")
	finish()
