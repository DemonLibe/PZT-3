extends TestHarness
## Район 25 «Потолок».

func _ready() -> void:
	var level := await load_level("res://levels/district_25_ceiling.tscn", 0)
	var zone: CeilingZone = level.get_node("CeilingZone")
	var m := local_member()
	zone.data.params["inhale_time"] = 1.5
	m.body.global_position = Vector3(-11.4, 0.1, 6.0)
	await wait(2.0)
	check(m.has_status(&"hallucinating"), "надышался парами — галлюцинации")
	check(level.get_node("HallucinationOverlay/Rect").visible, "картинка поплыла")
	zone.data.params["inhale_time"] = 25.0
	finish()
