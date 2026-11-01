class_name Squad
extends Node
## Отряд: список участников, кто ведёт, кто остался один, приказы и паника от потерь.

signal command_issued(command: StringName, issuer: ExpeditionMember)

const COMMAND_FOLLOW: StringName = &"follow"
const COMMAND_HOLD: StringName = &"hold"

@export var members_root: Node
## Участник считается одним, если рядом нет никого ближе этого радиуса.
@export var alone_radius: float = 8.0
@export var panic_on_loss: float = 0.3
## Насколько паника спадает за секунду.
@export var panic_decay: float = 0.01

var members: Array[ExpeditionMember] = []
var leader: ExpeditionMember
var last_command: StringName = COMMAND_FOLLOW

var _alone_timer: float = 0.0


func _ready() -> void:
	add_to_group(&"squad")
	members_root.child_entered_tree.connect(_on_body_added)
	members_root.child_exiting_tree.connect(_on_body_removed)
	EventBus.member_vanished.connect(_on_member_lost)
	EventBus.member_died.connect(_on_member_lost)


func _physics_process(delta: float) -> void:
	if not NetAuthority.is_authority():
		return
	for member in members:
		if member.is_active() and member.panic > 0.0:
			member.panic = maxf(0.0, member.panic - panic_decay * delta)
	_alone_timer += delta
	if _alone_timer >= 0.5:
		_alone_timer = 0.0
		_update_alone()


func size() -> int:
	return members.size()


func active_members() -> Array[ExpeditionMember]:
	return members.filter(func(m: ExpeditionMember) -> bool: return m.is_active())


func issue_command(command: StringName, issuer: ExpeditionMember) -> void:
	if not NetAuthority.is_authority():
		return
	last_command = command
	if command == COMMAND_FOLLOW:
		leader = issuer
	command_issued.emit(command, issuer)


func _update_alone() -> void:
	for member in members:
		if not member.is_active():
			continue
		var alone: bool = true
		for other in members:
			if other != member and other.is_active() and \
					other.body.global_position.distance_to(member.body.global_position) < alone_radius:
				alone = false
				break
		member.is_alone = alone


func _on_body_added(body: Node) -> void:
	# Узел тела ещё не готов — ждём, пока появятся дочерние.
	await get_tree().process_frame
	var member: ExpeditionMember = ExpeditionMember.find_on(body)
	if member and not members.has(member):
		members.append(member)
		if leader == null and body.name == "1":
			leader = member


func _on_body_removed(body: Node) -> void:
	var member: ExpeditionMember = ExpeditionMember.find_on(body)
	members.erase(member)
	if leader == member:
		leader = null


func _on_member_lost(lost: Node) -> void:
	if not members.has(lost):
		return
	for member in members:
		if member != lost and member.is_active():
			member.add_panic(panic_on_loss)
