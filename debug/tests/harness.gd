class_name TestHarness
extends Node
## Общие помощники для автотестов.

var failures: int = 0

func check(cond: bool, what: String) -> void:
	if cond:
		print("  OK   ", what)
	else:
		failures += 1
		print("  FAIL ", what)

func wait(sec: float) -> void:
	await get_tree().create_timer(sec, true, true).timeout

func frames(n: int) -> void:
	for i in n:
		await get_tree().physics_frame

func finish() -> void:
	print("ИТОГ: ", "все проверки пройдены" if failures == 0 else "провалено: %d" % failures)
	get_tree().quit(failures)

## Повернуть участника лицом к точке (тело — по горизонтали, голова — по вертикали).
func face(m: ExpeditionMember, point: Vector3) -> void:
	var to: Vector3 = point - m.get_gaze_origin()
	m.body.look_at(m.body.global_position + Vector3(to.x, 0, to.z))
	m.head.rotation.x = atan2(to.y, Vector2(to.x, to.z).length())

func local_member() -> ExpeditionMember:
	return get_tree().get_first_node_in_group(&"local_member") as ExpeditionMember

func load_level(path: String, npcs: int = 6) -> Node:
	var level: Node = load(path).instantiate()
	level.npc_count = npcs
	add_child(level)
	await frames(10)
	return level

func npcs_of(level: Node) -> Array[ExpeditionMember]:
	var out: Array[ExpeditionMember] = []
	for b in level.get_node("Members").get_children():
		if b.name.begins_with("npc"): out.append(ExpeditionMember.find_on(b))
	return out

func press(action: StringName) -> void:
	var ev := InputEventAction.new(); ev.action = action; ev.pressed = true
	Input.parse_input_event(ev)
	await frames(2)
	var ev2 := InputEventAction.new(); ev2.action = action; ev2.pressed = false
	Input.parse_input_event(ev2)
	await frames(2)
