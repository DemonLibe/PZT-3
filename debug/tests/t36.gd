extends TestHarness
## Секции 38 «Плакальщицы» и 40 «Хозяин ключей».

var lines: Array = []

func _ready() -> void:
	EventBus.radio_message.connect(func(sp, t): lines.append(sp + ": " + t))
	var level := await load_level("res://levels/section_38_mourners.tscn", 0)
	var zone: MournersZone = level.get_node("MournersZone")
	var m := local_member()
	m.body.global_position = Vector3(0, 0, 4)
	await wait(0.5)
	check(zone._followers.is_empty(), "издали — никто не идёт следом")
	m.body.global_position = Vector3(0.0, 0, -6.0)
	await wait(0.5)
	check(zone._followers.size() == 1, "подошёл вплотную — плакальщица пошла следом")
	level.queue_free()
	await frames(3)
	level = await load_level("res://levels/section_40_keymaster.tscn", 0)
	m = local_member()
	var master: Node3D = level.get_node("KeyMaster")
	m.body.global_position = Vector3(-5.2, 0, 0.0)
	await frames(2)
	face(m, master.global_position + Vector3(0, 1.0, 0))
	await frames(3)
	await press(&"interact")
	await frames(2)
	check(lines.any(func(l): return l.begins_with("Хозяин ключей: Ключ откроет")), "Хозяин ключей предложил обмен")
	await press(&"interact")
	await frames(2)
	check(m.has_status(&"has_useless_key"), "взял ключ — потерял отданное, ключ бесполезен")
	finish()
