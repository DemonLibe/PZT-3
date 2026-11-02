extends TestHarness

var slept: Dictionary = {}

func _ready() -> void:
	var level := await load_level("res://levels/district_08_sleep.tscn")
	level.loss_delay = 9999.0  # тест сам решает, когда закончить
	var m := local_member()
	var npcs := npcs_of(level)
	m.body.global_position = Vector3(0, 0, 10)  # маршрут длинный — сразу в район «Сна»
	for x in npcs + [m]:
		x.sleeping_changed.connect(func(v): if v: slept[x] = true)
	await wait(1.0)
	check(m.drowsiness > 0.005, "сонливость растёт в зоне (%.3f)" % m.drowsiness)
	# NPC отводим и оставляем стоять подальше
	await press(&"squad_hold")
	for i in npcs.size(): npcs[i].body.global_position = Vector3(-6 + 2.4 * i, 0, -14)
	m.body.global_position = Vector3(0, 0, 15)
	await wait(0.3)
	m.drowsiness = 0.995
	await wait(1.0)
	check(m.is_sleeping, "при 1.0 игрок засыпает")
	for i in 8:
		await press(&"interact")
	await wait(0.2)
	check(not m.is_sleeping and m.is_active(), "8 нажатий E — проснулся")
	check(absf(m.drowsiness - 0.5) < 0.05, "после пробуждения сонливость 0.5")
	# NPC засыпает — сосед будит
	var n: ExpeditionMember = npcs[0]
	n.drowsiness = 0.999
	for i in 30:
		await wait(0.5)
		if slept.has(n) and not n.is_sleeping: break
	check(slept.has(n), "NPC уснул")
	check(not n.is_sleeping and n.is_active(), "другой участник разбудил NPC")
	# Разводим всех дальше радиуса пробуждения — будить некому
	var far := [Vector3(-6, 0, -15), Vector3(6, 0, -15), Vector3(-6, 0, -4), Vector3(6, 0, -4), Vector3(-6, 0, 7), Vector3(6, 0, 7)]
	for i in npcs.size(): npcs[i].body.global_position = far[i]
	m.body.global_position = Vector3(0, 0, 17)
	await wait(0.3)
	for x in npcs: x.drowsiness = 0.999
	m.drowsiness = 0.999
	var start: float = Time.get_ticks_msec() / 1000.0
	for i in 90:
		await wait(0.5)
		if not m.is_alive and npcs.filter(func(x): return not x.is_alive).size() >= 2: break
	var took: float = Time.get_ticks_msec() / 1000.0 - start
	check(not m.is_alive and took > 19.0, "уснувший игрок погиб (через ~%.0f с)" % took)
	check(npcs.filter(func(x): return not x.is_alive).size() >= 2, "NPC тоже погибают во сне")
	finish()
