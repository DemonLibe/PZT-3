class_name NPCInstincts
extends Node
## Инстинкты напарника поверх приказов: разбудить уснувшего рядом
## и поддаться соблазну (еда), когда клонит в сон. Возвращает true, если занят.

@export var member: ExpeditionMember
@export var navigator: NPCNavigator
@export var actions: MemberActions
@export var wake_radius: float = 8.0
@export var temptation_radius: float = 6.0
## Базовый шанс поддаться соблазну за секунду (умножается на силу соблазна).
@export var temptation_chance: float = 0.5
@export var reach_distance: float = 1.6

var _target: Node3D
var _target_kind: StringName = &""
var _give_up_timer: float = 0.0
## Сколько секунд цель загорожена (смотрим на неё, но видим другое).
var _blocked_time: float = 0.0
var _sidestep: Vector3 = Vector3.INF


func act(delta: float) -> bool:
	if _target == null or not is_instance_valid(_target) or not _target_still_valid():
		_target = null
		_pick_target(delta)
	if _target == null:
		return false
	_give_up_timer -= delta
	if _give_up_timer <= 0.0:
		_target = null
		return false
	var aim: Vector3 = _aim_point()
	if _sidestep != Vector3.INF:
		navigator.move_to(_sidestep)
		if member.body.global_position.distance_to(_sidestep) < 0.7 or not navigator.is_moving():
			_sidestep = Vector3.INF
		return true
	var flat: Vector3 = aim - member.body.global_position
	flat.y = 0.0
	if flat.length() > reach_distance:
		navigator.move_to(aim)
		return true
	navigator.stop()
	if navigator.face(aim, delta, 2.0) < 0.08:
		if member.gaze_target != null and (member.gaze_target == _target or _target.is_ancestor_of(member.gaze_target)):
			_blocked_time = 0.0
			actions.interact()
		else:
			_blocked_time += delta
			if _blocked_time > 1.0:
				# Цель загорожена — обойти сбоку.
				_blocked_time = 0.0
				var side: Vector3 = flat.normalized().cross(Vector3.UP) * GameState.rng.randf_range(-1.5, 1.5)
				_sidestep = member.body.global_position + side
	return true


func _pick_target(delta: float) -> void:
	var squad: Squad = get_tree().get_first_node_in_group(&"squad") as Squad
	if squad:
		for other in squad.members:
			if other != member and other.is_active() and other.is_sleeping \
					and _distance(other.body) < wake_radius:
				_set_target(other.body, &"wake")
				return
	if member.has_status(&"ate_dinner"):
		return
	for node in get_tree().get_nodes_in_group(&"npc_temptation"):
		var item: Node3D = node as Node3D
		if item == null or _distance(item) > temptation_radius:
			continue
		var strength: float = float(item.call(&"get_temptation", member))
		if strength > 0.3 and GameState.rng.randf() < temptation_chance * strength * (0.2 + member.panic) * delta:
			_set_target(item, &"temptation")
			return


func _set_target(target: Node3D, kind: StringName) -> void:
	_blocked_time = 0.0
	_sidestep = Vector3.INF
	_target = target
	_target_kind = kind
	_give_up_timer = 15.0


func _target_still_valid() -> bool:
	if _target_kind == &"wake":
		var other: ExpeditionMember = ExpeditionMember.find_on(_target)
		return other != null and other.is_active() and other.is_sleeping
	return _target.visible and float(_target.call(&"get_temptation", member)) > 0.0


func _aim_point() -> Vector3:
	if _target_kind == &"wake":
		return _target.global_position + Vector3(0, 0.9, 0)
	return _target.global_position


func _distance(node: Node3D) -> float:
	return member.body.global_position.distance_to(node.global_position)
