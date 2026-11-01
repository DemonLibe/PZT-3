class_name MemberActions
extends Node
## Действия участника по просьбе управляющего (игрок или NPC).
## Если вызвано не на авторитетной стороне — просьба уходит хосту по сети.

@export var member: ExpeditionMember
@export var interact_distance: float = 2.5


func toggle_flashlight() -> void:
	_request(&"_do_toggle_flashlight")


func interact() -> void:
	_request(&"_do_interact")


func wake_tap() -> void:
	_request(&"_do_wake_tap")


func toggle_rest() -> void:
	_request(&"_do_toggle_rest")


func _request(method: StringName) -> void:
	if NetAuthority.is_authority():
		call(method)
	else:
		rpc_id(1, method)


func _is_sender_owner() -> bool:
	var sender: int = multiplayer.get_remote_sender_id()
	return sender == 0 or sender == member.get_parent().get_multiplayer_authority()


@rpc("any_peer", "call_remote", "reliable")
func _do_toggle_flashlight() -> void:
	if _is_sender_owner() and member.can_act():
		member.flashlight_on = not member.flashlight_on


@rpc("any_peer", "call_remote", "reliable")
func _do_interact() -> void:
	if not _is_sender_owner() or not member.can_act():
		return
	var target: Node = member.gaze_target
	if target == null:
		return
	if member.get_gaze_origin().distance_to(member.gaze_point) > interact_distance:
		return
	var other: ExpeditionMember = ExpeditionMember.find_on(target)
	if other and other.is_sleeping:
		other.wake_taps = ExpeditionMember.WAKE_BY_OTHER_TAPS
		return
	var interactable: Node = _find_interactable(target)
	if interactable:
		interactable.call(&"interact", member)


@rpc("any_peer", "call_remote", "reliable")
func _do_wake_tap() -> void:
	if _is_sender_owner() and member.is_active() and member.is_sleeping:
		member.wake_taps += 1


@rpc("any_peer", "call_remote", "reliable")
func _do_toggle_rest() -> void:
	if not _is_sender_owner() or not member.is_active() or member.is_eating:
		return
	# Во сне, навязанном аномалией, так просто не проснуться.
	if member.is_sleeping and member.has_status(&"forced_sleep"):
		return
	member.set_sleeping(not member.is_sleeping)


## Ищем у цели или её родителей метод interact(member).
func _find_interactable(node: Node) -> Node:
	var current: Node = node
	for i in 3:
		if current == null:
			return null
		if current.has_method(&"interact"):
			return current
		current = current.get_parent()
	return null
