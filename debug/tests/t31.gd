extends TestHarness
## Секция 31 «Шатун».

func _ready() -> void:
	var level := await load_level("res://levels/section_31_shatun.tscn", 0)
	level.loss_delay = 9999.0
	var shatun: Shatun = level.get_node("Shatun")
	var m := local_member()
	m.body.global_position = Vector3(-6.5, 0, 10)
	await wait(2.0)
	check(shatun.global_position.distance_to(Vector3(0, 0, -18)) > 0.5, "Шатун бродит")
	# Встать прямо у него на пути
	var ahead: Vector3 = shatun.global_position - shatun.global_basis.z * 2.0
	m.body.global_position = Vector3(ahead.x, 0, ahead.z)
	await wait(0.5)
	check(not m.is_alive and m.fate_cause == &"shatun", "оказался в створе движения — разорван")
	finish()
