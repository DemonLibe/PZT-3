extends TestHarness
## Район 11 «Тишина».

var calls: Array = []

func _ready() -> void:
	EventBus.radio_message.connect(func(sp, t): if sp == "Голос снаружи": calls.append(t))
	var level := await load_level("res://levels/district_11_silence.tscn", 0)
	level.loss_delay = 9999.0
	var zone: SilenceZone = level.get_node("SilenceZone")
	var m := local_member()
	m.body.global_position = Vector3(0, 0, -5)
	await wait(2.0)
	check(m.has_status(&"silence"), "в районе — тишина")
	var sfx: int = AudioServer.get_bus_index(&"SFX")
	check(AudioServer.is_bus_mute(sfx), "звуки заглушены, слышно только сердце")
	check(m.pulse_bpm < 72.0, "пульс замедляется (%.1f)" % m.pulse_bpm)
	m.body.global_position = Vector3(0, 0, 17)
	await wait(2.0)
	check(not m.has_status(&"silence") and not AudioServer.is_bus_mute(sfx), "вышел — звук вернулся")
	m.body.global_position = Vector3(0, 0, -5)
	zone.data.params["bpm_drop_per_sec"] = 8.0
	for i in 20:
		await wait(0.3)
		if not m.is_alive: break
	check(calls.has("Орлов!"), "перед остановкой — свой голос снаружи")
	check(not m.is_alive and m.fate_cause == &"silence", "пульс ниже 40 — остановка сердца")
	zone.data.params["bpm_drop_per_sec"] = 0.45
	finish()
