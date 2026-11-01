class_name ExpeditionJournal
extends RefCounted
## Журнал одной экспедиции: что произошло, с кем и когда.

## Во сколько начинается вылазка по часам района.
const START_HOUR: float = 22.0
## Одинаковый для всех обрыв отчёта (для аномалий с journal_cut).
const CUT_REPORT: String = "Отчёт: «Всё в порядке. Сейчас посмотрю, что там за сп"

var number: int = 0
var destination: String = ""
var outcome: String = ""
var entries: PackedStringArray = []
## имя участника -> итог («вернулся», «пропал», ...)
var fates: Dictionary = {}
## для Энциклопедии: [[id аномалии, текст записи]]
var incidents: Array = []


func _init(expedition_number: int, destination_title: String) -> void:
	number = expedition_number
	destination = destination_title
	add_entry("Экспедиция №%d вышла: %s." % [number, destination])


func add_entry(text: String) -> void:
	entries.append("%s  %s" % [_clock(), text])


func record_observed(member_name: String, data: AnomalyData) -> void:
	add_entry("%s: зафиксировано — %s." % [member_name, data.display_name if data else "не задокументировано"])


func record_loss(member_name: String, vanished: bool, data: AnomalyData) -> void:
	var what: String = "пропал" if vanished else "погиб"
	fates[member_name] = what
	if data and bool(data.params.get("journal_cut", false)):
		entries.append("%s  %s. %s" % [_clock(), member_name, CUT_REPORT])
	else:
		var signal_text: String = "связь потеряна" if vanished else "пульс не фиксируется"
		var cause: String = data.display_name if data else "причина не задокументирована"
		add_entry("%s: %s. %s." % [member_name, signal_text, cause])
	if data:
		incidents.append([data.id, "Экспедиция №%d: %s — %s." % [number, member_name, what]])


func record_left_behind(member_name: String, data: AnomalyData) -> void:
	if data:
		fates[member_name] = "остался в районе"
		add_entry("%s отказался уходить." % member_name)
		incidents.append([data.id, "Экспедиция №%d: %s отказался покинуть район." % [number, member_name]])
	else:
		fates[member_name] = "не вернулся"
		add_entry("%s не вернулся на базу." % member_name)


func finish(result: String, survivors: PackedStringArray) -> void:
	outcome = result
	for member_name in survivors:
		fates[member_name] = "вернулся"
	add_entry("Экспедиция завершена: %s." % result)


func _clock() -> String:
	var hours: float = fmod(START_HOUR + GameState.game_hours, 24.0)
	return "%02d:%02d" % [int(hours), int(fmod(hours * 60.0, 60.0))]
