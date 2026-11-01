extends TestHarness
## Район 24 «Голоса в рации».

var calls: Array = []

func _ready() -> void:
	EventBus.radio_message.connect(func(sp, t): if sp.ends_with("(рация)"): calls.append(t))
	var level := await load_level("res://levels/district_24_voices.tscn", 0)
	var zone: RadioVoicesZone = level.get_node("RadioVoicesZone")
	var m := local_member()
	m.body.global_position = Vector3(0, 0, 5)
	zone.data.params["call_interval"] = 1.0
	await wait(1.5)
	check(calls.size() >= 1 and calls[0].contains("X 0"), "голос назвал координаты группы: " + (calls[0] if calls else "-"))
	zone.data.params["call_interval"] = 999.0
	var before: int = calls.size()
	await press(&"radio_reply")
	await wait(3.0)
	check(calls.size() == before + 1, "ответил — тот же вызов повторился с другой интонацией")
	zone.data.params["call_interval"] = 20.0
	finish()
