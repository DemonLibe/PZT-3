class_name Mailbox
extends StaticBody3D
## Почтовый ящик с письмом, адресованным лично участнику. E — прочесть.

@export var zone: MailZone


func _ready() -> void:
	add_to_group(&"npc_temptation")
	add_to_group(&"attention_point")


func interact(member: ExpeditionMember) -> void:
	if zone:
		zone.read_letter(member)


func get_temptation(member: ExpeditionMember) -> float:
	return 0.0 if member.has_status(&"read_letter") else 0.3 + member.panic * 0.3
