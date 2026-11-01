class_name LaundryZone
extends AnomalyZone
## «Стирка» (Район 4): бельё во дворах. Надевший через 5–8 игровых часов
## получает необратимый статус — кожа с текстурой и швами ткани.

@export var laundry_root: Node


func _ready() -> void:
	super()
	for child in laundry_root.find_children("*", "LaundryItem", true, false):
		child.zone = self


func _on_member_entered(member: ExpeditionMember) -> void:
	observe(member)


func wear(member: ExpeditionMember, item: LaundryItem) -> void:
	if not NetAuthority.is_authority() or not member.can_act() or member.has_status(&"wore_laundry"):
		return
	item.set_present.rpc(false)
	member.add_status(&"wore_laundry")
	DelayedPunishment.attach(member, data, "LaundryEffect", "onset_min_hours", "onset_max_hours")


func get_debug_text(member: ExpeditionMember) -> String:
	var effect: DelayedPunishment = member.body.get_node_or_null("LaundryEffect") as DelayedPunishment
	if effect:
		return "Стирка: надел бельё, до проявления %.1f ч" % effect.hours_left()
	return "Стирка: бельё на верёвках"
