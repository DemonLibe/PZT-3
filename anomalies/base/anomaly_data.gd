class_name AnomalyData
extends Resource
## Данные аномалии: все числа правила живут здесь, в .tres, а не в коде.

@export var id: StringName = &""
@export var display_name: String = ""
@export var location: String = ""
@export_range(1, 5) var danger_level: int = 1
## Числа правила: пороги, времена, радиусы, шансы.
@export var params: Dictionary = {}
## null — правило без наказания (например, только паника).
@export var punishment: Punishment
## Текст статьи. Часть до строки "---" открывается при наблюдении, всё — после нарушения.
@export_multiline var encyclopedia_text: String = ""


func param(key: String, default: Variant = null) -> Variant:
	if not params.has(key):
		push_warning("AnomalyData '%s': нет параметра '%s'" % [id, key])
		return default
	return params[key]


## Нарушение правила: сообщить всем и наказать участника.
func punish(member: ExpeditionMember) -> void:
	if not NetAuthority.is_authority() or member == null or not member.is_active():
		return
	EventBus.rule_violated.emit(member, id)
	if punishment:
		punishment.apply(member, id)
