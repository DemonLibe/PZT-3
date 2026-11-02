class_name LaundryItem
extends StaticBody3D
## Бельё на верёвке — всегда точно по размеру смотрящего. E — надеть.
## Через 5–8 игровых часов кожа в местах контакта становится тканью.

@export var zone: LaundryZone


func _ready() -> void:
	add_to_group(&"npc_temptation")
	add_to_group(&"attention_point")


func interact(member: ExpeditionMember) -> void:
	if zone and visible:
		zone.wear(member, self)


## Соблазн для напарника: чем страшнее, тем сильнее хочется закутаться во что-то домашнее.
func get_temptation(member: ExpeditionMember) -> float:
	if not visible or member.has_status(&"wore_laundry"):
		return 0.0
	return 0.35 + member.panic * 0.6


@rpc("authority", "call_local", "reliable")
func set_present(value: bool) -> void:
	visible = value
	set_collision_layer_value(1, value)


func get_prompt() -> String:
	return "Надеть"
