extends TestHarness
## Секция 34 «Ткач».

func _ready() -> void:
	var level := await load_level("res://levels/section_34_weaver.tscn", 0)
	level.loss_delay = 9999.0
	var zone: WeaverZone = level.get_node("WeaverZone")
	var m := local_member()
	await frames(5)
	var threads: Array = level.get_node("Threads").get_children()
	var dark: Node3D = null
	var fresh: Node3D = null
	for t in threads:
		zone._set_thread(t.name, false)
	dark = threads[0]
	fresh = threads[threads.size() - 1]
	zone._set_thread(fresh.name, true)
	m.body.global_position = Vector3(dark.global_position.x, 0, dark.global_position.z)
	await wait(0.5)
	check(m.is_active(), "под тёмной нитью — безопасно")
	m.body.global_position = Vector3(fresh.global_position.x, 0, fresh.global_position.z)
	await wait(0.5)
	check(m.is_vanished and m.fate_cause == &"weaver", "под свежей нитью — свёрток")
	finish()
