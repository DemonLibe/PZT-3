class_name KitchenZone
extends AnomalyZone
## «Кухня» (Район 10): в холодильниках свежее мясо. Формально — животное.
## Последствия не задокументированы: съевший получает скрытый статус, статья открывается полностью.

@export var fridges_root: Node


func _ready() -> void:
	super()
	for child in fridges_root.find_children("*", "KitchenFridge", true, false):
		child.zone = self


func _on_member_entered(member: ExpeditionMember) -> void:
	observe(member)


func eat(member: ExpeditionMember) -> void:
	if not NetAuthority.is_authority() or not member.can_act() or member.is_eating or member.has_status(&"ate_kitchen_meat"):
		return
	member.is_eating = true
	await get_tree().create_timer(float(param("eat_duration", 3.0))).timeout
	if not is_instance_valid(member):
		return
	member.is_eating = false
	member.drowsiness = maxf(0.0, member.drowsiness - float(param("drowsiness_relief", 0.3)))
	member.add_status(&"ate_kitchen_meat")
	Encyclopedia.open_article(data.id, Encyclopedia.LEVEL_FULL)


func get_debug_text(member: ExpeditionMember) -> String:
	return "Кухня: %s" % ("ел мясо" if member.has_status(&"ate_kitchen_meat") else "не ел")
