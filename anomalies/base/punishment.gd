class_name Punishment
extends Resource
## Наказание за нарушение правила аномалии.

enum Type { DEATH, VANISH, STATUS_EFFECT, EVENT }

@export var type: Type = Type.VANISH
## Задержка в секундах между нарушением и наказанием.
@export var delay: float = 0.0
## Для STATUS_EFFECT — какой статус выдать.
@export var status_id: StringName = &""
## Для EVENT — какое событие отправить участнику.
@export var event_id: StringName = &""


func apply(member: ExpeditionMember, anomaly_id: StringName) -> void:
	if not NetAuthority.is_authority() or member == null:
		return
	if delay > 0.0:
		await member.get_tree().create_timer(delay).timeout
		if not is_instance_valid(member) or not member.is_active():
			return
	match type:
		Type.DEATH:
			member.kill(anomaly_id)
		Type.VANISH:
			member.vanish(anomaly_id)
		Type.STATUS_EFFECT:
			member.add_status(status_id)
		Type.EVENT:
			member.event_received.emit(event_id)
