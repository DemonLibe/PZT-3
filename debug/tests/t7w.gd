extends TestHarness

var observed: Array = []

func _ready() -> void:
	EventBus.anomaly_observed.connect(func(m, id): observed.append(m.display_name))
	var level := await load_level("res://levels/district_02_windows.tscn", 0)
	var m := local_member()
	var win: LitWindow = level.get_node("Windows/LitWindow3")
	await frames(3)
	m.body.global_position = Vector3(0, 0, win.global_position.z)
	face(m, win.global_position + Vector3(0, 0, 12))  # смотрим мимо окна
	await wait(0.5)
	check(win.is_lit, "окно горит")
	# Плавно поворачиваемся к окну за 1 с
	for i in 60:
		var t: float = (i + 1) / 60.0
		face(m, win.global_position + Vector3(0, 0, 12.0 * (1.0 - t)))
		await get_tree().physics_frame
	await wait(1.1)
	check(not win.is_lit, "свет погас, когда к окну повернулись")
	await wait(6.5)
	check(win.is_lit, "через ~6 с загорелся снова")
	var p0: float = m.panic
	m.look(PI * 0.9, 0)  # резкий поворот за кадр
	await frames(3)
	check(m.panic > p0 + 0.04, "резкий поворот повысил панику (%.2f -> %.2f)" % [p0, m.panic])
	check(m.is_active(), "наказания нет")
	# NPC тоже гасят окна взглядом
	level.queue_free()
	await frames(3)
	var lvl2 := await load_level("res://levels/district_02_windows.tscn", 3)
	local_member().body.global_position = Vector3(0, 0, 20)
	for n in npcs_of(lvl2): n.body.global_position = Vector3(0, 0, n.body.global_position.z - 20)
	for i in 40:
		await wait(0.5)
		if observed.any(func(x): return x != "Орлов"): break
	check(observed.any(func(x): return x != "Орлов"), "окна реагируют на взгляд NPC (%s)" % str(observed))
	finish()
