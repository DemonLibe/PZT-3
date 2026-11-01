extends TestHarness
## Клиент: подключается, смотрит в окно 15+ с, проверяет пропажу у себя.

func _ready() -> void:
	NetAuthority.prepare(NetAuthority.Mode.CLIENT, "127.0.0.1")
	var level: Node = load("res://levels/district_05_mirror.tscn").instantiate()
	add_child(level)
	check(NetAuthority.mode == NetAuthority.Mode.CLIENT and not NetAuthority.is_authority(), "режим CLIENT")
	var m: ExpeditionMember
	for i in 100:
		m = local_member()
		if m: break
		await wait(0.1)
	check(m != null and m.body.name != "1", "у клиента своё тело (%s)" % (m.body.name if m else "-"))
	check(level.get_node("Members").get_child_count() == 8, "клиент видит хоста и 6 NPC")
	var view: MirrorView = level.get_node("MirrorView")
	var win: MirrorWindow = level.get_node("Windows/MirrorWindow2")
	m.body.global_position = Vector3(-1.5, 0, -1.0)
	await wait(0.5)
	face(m, win.global_position)
	await wait(2.0)
	check(m.gaze_time > 1.0, "взгляд считается на хосте и приходит клиенту (%.1f)" % m.gaze_time)
	await wait(3.0)
	check(view.mimic_member == m, "клиент: после 4 с картинка повторяет движения")
	for i in 150:
		if m.is_vanished: break
		await wait(0.1)
	check(m.is_vanished, "клиент: пропал после 15 с")
	check(not m.body.visible, "клиент: тело скрыто")
	await wait(0.3)
	check(win.is_cracked, "клиент: окно треснуло")
	finish()
