class_name CompanionZone
extends AnomalyZone
## «Спутник за столом» (Район 27): за накрытым столом сидит фигура спиной к входу.
## Не двигается, пока к ней не обратятся. Единственная окликнувшая группа на связь не вышла.

@export var figure: SeatedFigure


func _ready() -> void:
	super()
	figure.zone = self


func _on_member_entered(member: ExpeditionMember) -> void:
	observe(member)


func call_out(member: ExpeditionMember) -> void:
	if not NetAuthority.is_authority() or not member.can_act():
		return
	_turn.rpc()
	await get_tree().create_timer(1.5).timeout
	var squad: Squad = get_tree().get_first_node_in_group(&"squad") as Squad
	for other in (squad.active_members() if squad else [member]):
		violate(other)


@rpc("authority", "call_local", "reliable")
func _turn() -> void:
	create_tween().tween_property(figure, "rotation:y", figure.rotation.y + PI, 1.2)
