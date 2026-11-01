extends TestHarness
## Район 27 «Спутник за столом».

func _ready() -> void:
	var level := await load_level("res://levels/district_27_companion.tscn", 2)
	level.loss_delay = 9999.0
	var m := local_member()
	var fig: Node3D = level.get_node("Figure")
	m.body.global_position = Vector3(-9.8, 0.1, 5.5)
	await frames(2)
	face(m, fig.global_position + Vector3(0, 1.0, 0))
	await frames(3)
	check(m.gaze_target == fig, "смотрит на фигуру за столом (%s)" % m.gaze_label)
	await wait(1.0)
	check(m.is_active(), "пока молчим — фигура неподвижна")
	await press(&"interact")
	await wait(2.0)
	var all_gone: bool = npcs_of(level).all(func(n): return not n.is_active())
	check(m.is_vanished and all_gone, "окликнул — группа не вышла на связь")
	finish()
