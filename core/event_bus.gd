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
## Реплика по рации или вслух (Дорохов, Мельников) — для интерфейса.
@warning_ignore("unused_signal")
signal radio_message(speaker: String, text: String)
## Участник ответил по рации (клавиша R).
@warning_ignore("unused_signal")
signal radio_replied(member: Node)


func _ready() -> void:
	rule_violated.connect(func(m: Node, id: StringName) -> void: _log("нарушено правило '%s'" % id, m))
	member_died.connect(func(m: Node) -> void: _log("погиб", m))
	member_vanished.connect(func(m: Node) -> void: _log("пропал", m))
	anomaly_observed.connect(func(m: Node, id: StringName) -> void: _log("наблюдает аномалию '%s'" % id, m))
	print("[EventBus] готов")


func _log(text: String, member: Node) -> void:
	var who: String = String(member.get(&"display_name")) if member else "?"
	print("[EventBus] %s: %s" % [who, text])
