class_name BreathingWall
extends StaticBody3D
## Тёплая, слегка пульсирующая стена. E — приложить ладонь (держать рядом).

var zone: BreathingWallsZone


func interact(member: ExpeditionMember) -> void:
	if zone:
		zone.touch(member, self)
