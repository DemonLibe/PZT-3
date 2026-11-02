class_name KeyMaster
extends StaticBody3D
## Хозяин ключей. E — выслушать предложение, второй раз E — согласиться на обмен.

var zone: KeyMasterZone


func interact(member: ExpeditionMember) -> void:
	if zone:
		zone.talk(member)


func get_prompt() -> String:
	return "Говорить"
