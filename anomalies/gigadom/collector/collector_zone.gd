class_name CollectorZone
extends AnomalyZone
## «Сборщик» (Секция 44): собирает оброненные вещи в кучи в тупиковых помещениях.
## Свою оброненную вещь не поднимать. Поднявший становится «меченым» — Сборщик начинает
## появляться рядом с ним.

const ITEMS: PackedStringArray = ["фонарик", "флягу", "блокнот", "перчатку"]

@export var collector: Node3D

var _drop_timer: float = 0.0
var _appear_timer: float = 0.0


func _ready() -> void:
	super()
	collector.visible = false


func _physics_process(delta: float) -> void:
	super(delta)
	if not NetAuthority.is_authority() or members.is_empty():
		return
	_drop_timer += delta
	if _drop_timer >= float(param("drop_interval", 30.0)):
		_drop_timer = 0.0
		var dropper: ExpeditionMember = members[GameState.rng.randi_range(0, members.size() - 1)]
		if dropper.is_active():
			var item: String = ITEMS[GameState.rng.randi_range(0, ITEMS.size() - 1)]
			_drop.rpc(dropper.get_path(), dropper.body.global_position + dropper.body.global_basis.z * 0.8)
			EventBus.radio_message.emit(dropper.display_name, "Чёрт, %s выронил." % item)
	_appear_timer += delta
	if _appear_timer >= float(param("appear_interval", 15.0)):
		_appear_timer = 0.0
		var marked: Array[ExpeditionMember] = members.filter(func(m: ExpeditionMember) -> bool: return m.is_active() and m.has_status(&"marked"))
		if not marked.is_empty():
			var m: ExpeditionMember = marked[0]
			_appear.rpc(m.body.global_position + m.body.global_basis.z * 6.0)


func _check_rule(member: ExpeditionMember, _delta: float) -> void:
	if collector.visible and collector.global_position.distance_to(member.body.global_position) < 10.0:
		observe(member)


func pick_up(member: ExpeditionMember, item: DroppedItem) -> void:
	if not NetAuthority.is_authority() or not member.can_act():
		return
	item.queue_free()
	if item.owner_member == member and not member.has_status(&"marked"):
		member.add_status(&"marked")
		EventBus.rule_violated.emit(member, data.id)


func get_debug_text(member: ExpeditionMember) -> String:
	return "Сборщик: %s" % ("МЕЧЕНЫЙ" if member.has_status(&"marked") else "вещи на полу не трогать")


@rpc("authority", "call_local", "reliable")
func _drop(owner_path: NodePath, at: Vector3) -> void:
	var item: DroppedItem = DroppedItem.new()
	item.zone = self
	item.owner_member = get_node_or_null(owner_path) as ExpeditionMember
	var mesh: MeshInstance3D = MeshInstance3D.new()
	var box: BoxMesh = BoxMesh.new()
	box.size = Vector3(0.25, 0.1, 0.15)
	mesh.mesh = box
	item.add_child(mesh)
	var shape: CollisionShape3D = CollisionShape3D.new()
	var box_shape: BoxShape3D = BoxShape3D.new()
	box_shape.size = Vector3(0.4, 0.3, 0.4)
	shape.shape = box_shape
	item.add_child(shape)
	add_child(item)
	item.global_position = Vector3(at.x, 0.05, at.z)


@rpc("authority", "call_local", "reliable")
func _appear(at: Vector3) -> void:
	collector.visible = true
	collector.global_position = Vector3(at.x, 0.0, at.z)
	await get_tree().create_timer(4.0).timeout
	collector.visible = false
