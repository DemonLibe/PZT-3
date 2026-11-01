extends TestHarness
## Район 30 «Ничего».

func _ready() -> void:
	await frames(1)
	var dummy: Node = Node.new()
	get_tree().root.add_child(dummy)
	get_tree().current_scene = dummy
	Encyclopedia.reset()
	GameState.begin_expedition({"title": "Район 30", "path": "res://levels/district_30_nothing.tscn"})
	await wait(2.0)
	var level: Node = get_tree().current_scene
	check(level.get_node_or_null("ExitDoor") == null, "КПП нет")
	check(level.get_node_or_null("RadioOperator") == null, "Дорохов молчит")
	var m := local_member()
	m.body.global_position = Vector3(0, 0, -33)
	await wait(1.0)
	var j: ExpeditionJournal = GameState.last_journal
	check(j != null and j.outcome.contains("Дальнейших записей нет"), "журнал обрывается записью о входе")
	check(Encyclopedia.is_completed("Район 30"), "Район 30 пройден — дальше Гигадом")
	finish()
