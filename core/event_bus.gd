extends Node
## Общая шина событий: логика сообщает, UI и звук слушают.
## member — узел ExpeditionMember (появится на этапе 2).

@warning_ignore("unused_signal")
signal rule_violated(member: Node, anomaly_id: StringName)
@warning_ignore("unused_signal")
signal member_died(member: Node)
@warning_ignore("unused_signal")
signal member_vanished(member: Node)
@warning_ignore("unused_signal")
signal anomaly_observed(member: Node, anomaly_id: StringName)
@warning_ignore("unused_signal")
signal noise_emitted(member: Node, position: Vector3, level: float)


func _ready() -> void:
	print("[EventBus] готов")
