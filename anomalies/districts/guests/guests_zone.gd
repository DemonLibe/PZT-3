class_name GuestsZone
extends AnomalyZone
## «Гости» (Район 7): в домах появляется копия одного из участников — без тени.
## Двойник дружелюбен и зовёт «домой». Кто пошёл с ним — пропал.

const INVITES: PackedStringArray = [
	"Пойдём домой. Там тепло, ужин на столе.",
	"Хватит ходить. Пойдём, переночуешь у нас.",
	"Ты устал. Дома всё готово, пойдём.",
]

@export var entrances_root: Node

var _double: GuestDouble
var _timer: float = 0.0


func _physics_process(delta: float) -> void:
	super(delta)
	if not NetAuthority.is_authority():
		return
	if _double and is_instance_valid(_double):
		return
	_timer += delta
	if _timer >= float(param("spawn_interval", 25.0)):
		_timer = 0.0
		_spawn_double()


func go_home(member: ExpeditionMember, double: GuestDouble) -> void:
	if not NetAuthority.is_authority() or not member.can_act():
		return
	_remove_double.rpc()
	violate(member)


func get_debug_text(_member: ExpeditionMember) -> String:
	if _double and is_instance_valid(_double):
		return "Гости: двойник %s зовёт %s" % [_double.original.display_name, _double.target.display_name]
	return "Гости: следующий через %.0f с" % (float(param("spawn_interval", 25.0)) - _timer)


func _spawn_double() -> void:
	var active: Array[ExpeditionMember] = members.filter(func(m: ExpeditionMember) -> bool: return m.is_active())
	if active.is_empty():
		return
	var original: ExpeditionMember = active[GameState.rng.randi_range(0, active.size() - 1)]
	var target: ExpeditionMember = active[GameState.rng.randi_range(0, active.size() - 1)]
	var spots: Array[Node] = entrances_root.get_children()
	var spot: Node3D = spots[GameState.rng.randi_range(0, spots.size() - 1)]
	_create_double.rpc(original.get_path(), target.get_path(), spot.global_position)
	for member in active:
		observe(member)
	EventBus.radio_message.emit(original.display_name, INVITES[GameState.rng.randi_range(0, INVITES.size() - 1)])


@rpc("authority", "call_local", "reliable")
func _create_double(original_path: NodePath, target_path: NodePath, at: Vector3) -> void:
	var original: ExpeditionMember = get_node_or_null(original_path) as ExpeditionMember
	if original == null:
		return
	var double: GuestDouble = GuestDouble.new()
	double.name = "GuestDouble"
	double.zone = self
	double.original = original
	double.target = get_node_or_null(target_path) as ExpeditionMember
	var source: MeshInstance3D = original.body.get_node_or_null("BodyMesh") as MeshInstance3D
	if source:
		var mesh: MeshInstance3D = source.duplicate() as MeshInstance3D
		mesh.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF  # единственное отличие — нет тени
		double.add_child(mesh)
	var shape: CollisionShape3D = CollisionShape3D.new()
	var capsule: CapsuleShape3D = CapsuleShape3D.new()
	capsule.radius = 0.35
	capsule.height = 1.8
	shape.shape = capsule
	shape.position = Vector3(0, 0.9, 0)
	double.add_child(shape)
	add_child(double)
	double.global_position = at
	_double = double


@rpc("authority", "call_local", "reliable")
func _remove_double() -> void:
	if _double and is_instance_valid(_double):
		_double.queue_free()
	_double = null
