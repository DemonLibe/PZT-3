class_name ButcherZone
extends AnomalyZone
## «Мясник» (Секция 37): помещение с крюками, крупная фигура в фартуке.
## Не трогает безоружных. Вошёл с оружием в руках — мгновенная атака.

@export var butcher: Node3D


func _check_rule(member: ExpeditionMember, _delta: float) -> void:
	observe(member)
	if member.weapon_out:
		_strike.rpc(member.body.global_position)
		violate(member)


func get_debug_text(member: ExpeditionMember) -> String:
	return "Мясник: %s" % ("ОРУЖИЕ В РУКАХ" if member.weapon_out else "безоружен")


@rpc("authority", "call_local", "reliable")
func _strike(at: Vector3) -> void:
	if butcher:
		butcher.look_at(Vector3(at.x, butcher.global_position.y, at.z), Vector3.UP)
