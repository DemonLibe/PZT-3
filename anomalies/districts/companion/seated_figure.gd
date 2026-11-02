class_name SeatedFigure
extends StaticBody3D
## Фигура за накрытым столом, всегда спиной к входу. E — окликнуть.

var zone: CompanionZone


func interact(member: ExpeditionMember) -> void:
	if zone:
		zone.call_out(member)


func get_prompt() -> String:
	return "Окликнуть"
