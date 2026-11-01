class_name DroppedItem
extends StaticBody3D
## Оброненная участником вещь. E — поднять (запрещено: станешь «меченым»).

var zone: CollectorZone
var owner_member: ExpeditionMember


func _ready() -> void:
	add_to_group(&"npc_temptation")


func interact(member: ExpeditionMember) -> void:
	if zone:
		zone.pick_up(member, self)


func get_temptation(member: ExpeditionMember) -> float:
	return 0.6 if member == owner_member else 0.0
