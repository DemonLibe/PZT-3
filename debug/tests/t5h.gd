extends TestHarness
## Хост: ждёт клиента и проверяет, что «Зеркало» забрало клиента.

func _ready() -> void:
	NetAuthority.prepare(NetAuthority.Mode.HOST)
	var level: Node = load("res://levels/district_05_mirror.tscn").instantiate()
	add_child(level)
	check(NetAuthority.mode == NetAuthority.Mode.HOST, "режим HOST")
	var members: Node = level.get_node("Members")
	for i in 200:
		if members.get_child_count() >= 5: break
		await wait(0.1)
	check(members.get_child_count() == 5, "на хосте 2 игрока + 3 NPC")
	var client_member: ExpeditionMember
	for b in members.get_children():
		if b.name != "1" and not b.name.begins_with("npc"): client_member = ExpeditionMember.find_on(b)
	check(client_member != null and client_member.display_name == "Участник 2", "участник клиента")
	for i in 300:
		if client_member.is_vanished: break
		await wait(0.1)
	check(client_member.is_vanished, "хост: клиента забрало Зеркало")
	check(local_member().is_active(), "хост цел")
	await wait(2.0)
	finish()
