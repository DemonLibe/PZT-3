class_name KitchenFridge
extends StaticBody3D
## Холодильник со свежим мясом. E — съесть. По виду, запаху и вкусу — обычное мясо.

@export var zone: KitchenZone


func _ready() -> void:
	add_to_group(&"npc_temptation")


func interact(member: ExpeditionMember) -> void:
	if zone:
		zone.eat(member)


func get_temptation(member: ExpeditionMember) -> float:
	return 0.0 if member.has_status(&"ate_kitchen_meat") else member.drowsiness * 0.8
