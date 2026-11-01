class_name DinnerFood
extends StaticBody3D
## Тарелка с тёплой едой. E — съесть. Соблазн для уставших напарников.

@export var zone: DinnerZone

var is_eaten: bool = false


func _ready() -> void:
	add_to_group(&"npc_temptation")
	add_to_group(&"attention_point")


func interact(member: ExpeditionMember) -> void:
	if not is_eaten and visible and zone:
		zone.eat(member, self)


## Насколько эта еда соблазнительна для участника (0–1).
func get_temptation(member: ExpeditionMember) -> float:
	if not visible or is_eaten or member.has_status(&"ate_dinner"):
		return 0.0
	return member.drowsiness


@rpc("authority", "call_local", "reliable")
func set_present(value: bool) -> void:
	visible = value
	set_collision_layer_value(1, value)
	if not value:
		is_eaten = true
