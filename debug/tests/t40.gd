extends TestHarness
## Секции 48 «Пустой конвой» и 49 «Смотрящий из шахты».

func _ready() -> void:
	var level := await load_level("res://levels/section_48_convoy.tscn", 0)
	level.loss_delay = 9999.0
	var zone: ConvoyZone = level.get_node("ConvoyZone")
	var m := local_member()
	# Встать лицом к стене коридора
	m.body.global_position = Vector3(-1.3, 0, 5)
	await frames(2)
	face(m, Vector3(-5, 1.6, 5))
	zone._set_phase(ConvoyZone.Phase.MARCH)
	await wait(2.0)
	check(m.is_active(), "смирно лицом к стене — строй проходит мимо")
	zone._set_phase(ConvoyZone.Phase.MARCH)
	face(m, Vector3(-1.3, 1.6, -10))
	await wait(0.5)
	check(m.is_vanished and m.fate_cause == &"convoy", "не встал к стене — строй остановился")
	level.queue_free()
	await frames(3)
	level = await load_level("res://levels/section_49_shaft.tscn", 0)
	m = local_member()
	var hours: float = GameState.game_hours
	m.body.global_position = Vector3(0, 0, 5.2)
	await frames(2)
	face(m, Vector3(0, -2.0, 4.0))
	await wait(1.5)
	check(m.is_sleeping and m.has_status(&"memory_gap"), "заглянул в шахту — потерял сознание")
	check(GameState.game_hours > hours + 1.0, "провал в памяти на часы")
	finish()
