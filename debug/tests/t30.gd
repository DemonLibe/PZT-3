extends TestHarness
## Секции 30 «Порог» и 50 «Порог второй».

func _ready() -> void:
	await frames(1)
	Encyclopedia.reset()
	var level := await load_level("res://levels/section_30_threshold.tscn", 0)
	local_member().body.global_position = Vector3(0, 0, 5)
	await wait(0.5)
	check(Encyclopedia.article_level(&"threshold") == 1, "Порог: секция отмечена, опасности нет")
	level.queue_free()
	await frames(3)
	var dummy: Node = Node.new()
	get_tree().root.add_child(dummy)
	get_tree().current_scene = dummy
	GameState.begin_expedition({"title": "Гигадом, секция 50", "path": "res://levels/section_50_threshold.tscn"})
	await wait(2.0)
	local_member().body.global_position = Vector3(0, 0, -23.5)
	await wait(1.0)
	var j: ExpeditionJournal = GameState.last_journal
	check(j != null and j.outcome.contains("51-ю секцию"), "Порог второй: журнал обрывается записью о входе в 51-ю")
	finish()
