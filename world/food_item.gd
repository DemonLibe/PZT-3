class_name FoodItem
extends StaticBody3D
## Обычная еда или вода (в Гигадоме безопасны). E — съесть: участник занят едой.

@export var eat_duration: float = 4.0


func interact(member: ExpeditionMember) -> void:
	if not NetAuthority.is_authority() or not visible or member.is_eating:
		return
	_set_present.rpc(false)
	member.is_eating = true
	await get_tree().create_timer(eat_duration).timeout
	if is_instance_valid(member):
		member.is_eating = false


@rpc("authority", "call_local", "reliable")
func _set_present(value: bool) -> void:
	visible = value
	set_collision_layer_value(1, value)
