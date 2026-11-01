class_name ObserveZone
extends AnomalyZone
## Зона без правила: только отмечает, что участник её видел (для Энциклопедии).


func _on_member_entered(member: ExpeditionMember) -> void:
	observe(member)
