extends TestHarness
## Район 10 «Кухня».

func _ready() -> void:
	Encyclopedia.reset()
	var level := await load_level("res://levels/district_10_kitchen.tscn", 0)
	var m := local_member()
	var fridge: Node3D = level.get_node("Fridges/Fridge1")
	m.body.global_position = fridge.global_position + Vector3(1.3, -0.85, 0.2)
	await frames(3)
	check(Encyclopedia.article_level(&"kitchen") == 1, "вошёл на кухню — статья открыта частично")
	face(m, fridge.global_position)
	await frames(3)
	m.drowsiness = 0.6
	await press(&"interact")
	await wait(3.3)
	check(m.has_status(&"ate_kitchen_meat") and m.drowsiness < 0.35, "съел мясо: сонливость снизилась, скрытый статус")
	check(Encyclopedia.article_level(&"kitchen") == 2, "статья открыта полностью")
	finish()
