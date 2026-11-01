class_name WeaverZone
extends AnomalyZone
## «Ткач» (Секция 34): под потолком — нити, похожие на сухожилия. Свежие (блестящие)
## реагируют на тепло: прошёл под такой — сверху падает свёрток. Потемневшие безопасны.

@export var threads_root: Node
@export var fresh_material: Material
@export var dark_material: Material

var _fresh: Dictionary = {}
var _timer: float = 0.0


func _ready() -> void:
	super()
	_rehang.call_deferred()


func _physics_process(delta: float) -> void:
	super(delta)
	if not NetAuthority.is_authority():
		return
	_timer += delta
	if _timer >= float(param("rehang_interval", 40.0)):
		_timer = 0.0
		_rehang()


func _check_rule(member: ExpeditionMember, _delta: float) -> void:
	for thread in threads_root.get_children():
		var t: Node3D = thread
		var flat: Vector2 = Vector2(t.global_position.x - member.body.global_position.x, t.global_position.z - member.body.global_position.z)
		if flat.length() < 3.0:
			observe(member)
		if _fresh.get(t.name, false) and flat.length() < float(param("trigger_radius", 0.6)):
			_set_thread.rpc(t.name, false)
			violate(member)
			return


func get_debug_text(_member: ExpeditionMember) -> String:
	return "Ткач: свежих нитей %d" % _fresh.values().filter(func(v: bool) -> bool: return v).size()


func _rehang() -> void:
	if not NetAuthority.is_authority():
		return
	for thread in threads_root.get_children():
		_set_thread.rpc(thread.name, GameState.rng.randf() < float(param("fresh_ratio", 0.4)))


@rpc("authority", "call_local", "reliable")
func _set_thread(thread_name: String, fresh: bool) -> void:
	_fresh[thread_name] = fresh
	var thread: MeshInstance3D = threads_root.get_node_or_null(thread_name) as MeshInstance3D
	if thread:
		thread.material_override = fresh_material if fresh else dark_material
