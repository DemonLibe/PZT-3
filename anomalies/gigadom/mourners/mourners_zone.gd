class_name MournersZone
extends AnomalyZone
## «Плакальщицы» (Секция 38): плачущие фигуры спиной к группе, голосами близких.
## Не подходить, не заговаривать, не смотреть в глаза при развороте. Контакт —
## плачущих становится больше, и они идут следом, с каждым разом ближе.

@export var mourners_root: Node

var _turned: bool = false
var _turn_timer: float = 0.0
var _followers: Array[Node3D] = []
var _follow_distance: float = 15.0
var _contacted: Dictionary = {}


func _ready() -> void:
	super()
	EventBus.member_spoke.connect(_on_spoke)


func _physics_process(delta: float) -> void:
	super(delta)
	if not NetAuthority.is_authority():
		return
	_turn_timer += delta
	if _turn_timer >= float(param("turn_interval", 8.0)):
		_turn_timer = 0.0
		_set_turned.rpc(not _turned)
	_move_followers(delta)


func _check_rule(member: ExpeditionMember, _delta: float) -> void:
	for mourner in mourners_root.get_children():
		var at: Vector3 = (mourner as Node3D).global_position + Vector3(0, 1.5, 0)
		var distance: float = at.distance_to(member.get_gaze_origin())
		if distance < 12.0 and member.is_in_view_cone(at, 60.0):
			observe(member)
		var looked_in_eyes: bool = _turned and distance < 10.0 and member.is_in_view_cone(at, 12.0)
		if distance < float(param("approach_distance", 3.0)) or looked_in_eyes:
			_contact(member)
			return


func get_debug_text(_member: ExpeditionMember) -> String:
	return "Плакальщицы: %s, следом идут %d (дистанция %.0f м)" % ["обернулись" if _turned else "спиной",
		_followers.size(), _follow_distance]


func _on_spoke(member: Node, _phrase: String) -> void:
	var expedition_member: ExpeditionMember = member as ExpeditionMember
	if not NetAuthority.is_authority() or expedition_member == null or not members.has(expedition_member):
		return
	for mourner in mourners_root.get_children():
		if (mourner as Node3D).global_position.distance_to(expedition_member.body.global_position) < 8.0:
			_contact(expedition_member)
			return


func _contact(member: ExpeditionMember) -> void:
	if _contacted.get(member, -10.0) > Time.get_ticks_msec() / 1000.0 - 5.0:
		return
	_contacted[member] = Time.get_ticks_msec() / 1000.0
	EventBus.rule_violated.emit(member, data.id)
	member.add_panic(float(param("panic_contact", 0.2)))
	_follow_distance = maxf(2.0, _follow_distance - float(param("close_in", 3.0)))
	_spawn_follower.rpc(member.body.global_position + member.body.global_basis.z * _follow_distance)


func _move_followers(delta: float) -> void:
	var squad: Squad = get_tree().get_first_node_in_group(&"squad") as Squad
	if squad == null or squad.leader == null:
		return
	var target: Vector3 = squad.leader.body.global_position
	for follower in _followers:
		var to: Vector3 = target - follower.global_position
		to.y = 0.0
		if to.length() > _follow_distance:
			follower.global_position += to.normalized() * 1.4 * delta


@rpc("authority", "call_local", "reliable")
func _set_turned(value: bool) -> void:
	_turned = value
	for mourner in mourners_root.get_children():
		(mourner as Node3D).rotate_y(PI)


@rpc("authority", "call_local", "reliable")
func _spawn_follower(at: Vector3) -> void:
	var source: Node3D = mourners_root.get_child(0) as Node3D
	var follower: Node3D = source.duplicate() as Node3D
	add_child(follower)
	follower.global_position = Vector3(at.x, 0.0, at.z)
	_followers.append(follower)
