class_name PuppetDouble
extends StaticBody3D
## Дубль на нитях Кукольника: дёргается резко и неестественно. Не трогать.
## E с оружием в руках — ударить (запрещено).

var zone: PuppeteerZone


func interact(member: ExpeditionMember) -> void:
	if zone and member.weapon_out:
		zone.attack(member, self)


func get_prompt() -> String:
	return "Ударить"
