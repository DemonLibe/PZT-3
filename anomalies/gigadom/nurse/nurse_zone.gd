class_name NurseZone
extends AnomalyZone
## «Кормилица» (Секция 46): заботливая женщина появляется только перед тем, кто остался
## один, вне поля зрения группы. Найденного в одиночестве «уводит» — будто ушёл сам.

@export var nurse: Node3D

## member -> секунд в одиночестве
var _alone: Dictionary = {}


func _ready() -> void:
	super()
	nurse.visible = false


func _check_rule(member: ExpeditionMember, delta: float) -> void:
	if not member.is_alone:
		_alone.erase(member)
		return
	_alone[member] = float(_alone.get(member, 0.0)) + delta
	if _alone[member] >= float(param("alone_time", 6.0)):
		_alone.erase(member)
		observe(member)
		_appear.rpc(member.body.global_position + member.body.global_basis.x * 1.2)
		violate(member)


func get_debug_text(member: ExpeditionMember) -> String:
	return "Кормилица: %s" % ("ОДИН %.0f с" % float(_alone.get(member, 0.0)) if member.is_alone else "рядом свои")


@rpc("authority", "call_local", "reliable")
func _appear(at: Vector3) -> void:
	nurse.visible = true
	nurse.global_position = Vector3(at.x, 0.0, at.z)
	await get_tree().create_timer(2.5).timeout
	nurse.visible = false
