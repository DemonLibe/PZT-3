extends Node
## Текущая экспедиция, общий генератор случайных чисел и игровое время.
## Вся случайность в игре — только через GameState.rng.

const BASE_SCENE: String = "res://ui/base_menu.tscn"
const JOURNAL_SCENE: String = "res://ui/journal.tscn"

## Сколько игровых часов проходит за одну реальную секунду.
@export var hours_per_second: float = 1.0 / 60.0

var rng: RandomNumberGenerator = RandomNumberGenerator.new()
var expedition_seed: int = 0
## Игровое время экспедиции в часах.
var game_hours: float = 0.0
## Журнал идущей экспедиции (null — экспедиции нет).
var journal: ExpeditionJournal
## Журнал последней завершённой экспедиции — для экрана журнала.
var last_journal: ExpeditionJournal


func _ready() -> void:
	start_expedition(0)
	EventBus.member_died.connect(func(m: Node) -> void: _on_member_lost(m, false))
	EventBus.member_vanished.connect(func(m: Node) -> void: _on_member_lost(m, true))
	EventBus.anomaly_observed.connect(_on_anomaly_observed)
	print("[GameState] готов, сид экспедиции: ", expedition_seed)


func _process(delta: float) -> void:
	if NetAuthority.is_authority():
		game_hours += delta * hours_per_second


## Отладка: промотать игровое время.
func debug_skip_hours(hours: float) -> void:
	if NetAuthority.is_authority():
		game_hours += hours


## Начать новую экспедицию. seed_value = 0 — взять случайный сид.
func start_expedition(seed_value: int) -> void:
	if seed_value == 0:
		rng.randomize()
		seed_value = rng.randi()
	expedition_seed = seed_value
	rng.seed = expedition_seed
	game_hours = 0.0


## Выйти с базы в район или секцию: {"title": ..., "path": ...}.
func begin_expedition(destination: Dictionary) -> void:
	start_expedition(0)
	journal = ExpeditionJournal.new(Encyclopedia.expedition_count + 1, destination["title"])
	get_tree().change_scene_to_file(destination["path"])


## Уровень запущен напрямую (F6, сетевой тест) — завести журнал на ходу.
func ensure_expedition(title: String) -> void:
	if journal == null and NetAuthority.is_authority():
		journal = ExpeditionJournal.new(Encyclopedia.expedition_count + 1, title)


func is_expedition_active() -> bool:
	return journal != null


## Конец вылазки: survivors вернулись, left_behind остались в районе.
func end_expedition(result: String, survivors: Array[ExpeditionMember], left_behind: Array[ExpeditionMember]) -> void:
	if journal == null or not NetAuthority.is_authority():
		return
	for member in left_behind:
		if not is_instance_valid(member) or not member.is_active():
			continue  # уже записан как погибший или пропавший
		var cause: AnomalyData = Encyclopedia.get_data(member.fate_cause) if member.has_status(&"lost_purpose") else null
		journal.record_left_behind(member.display_name, cause)
	var names: PackedStringArray = []
	for member in survivors:
		names.append(member.display_name)
	journal.finish(result, names)
	Encyclopedia.expedition_count = journal.number
	for incident in journal.incidents:
		Encyclopedia.add_incident(incident[0], incident[1])
	Encyclopedia.save_to_disk()
	last_journal = journal
	journal = null
	print("[GameState] экспедиция №%d завершена: %s" % [last_journal.number, result])
	if NetAuthority.is_networked():
		NetAuthority.end_session()
	get_tree().change_scene_to_file.call_deferred(JOURNAL_SCENE)


func _on_member_lost(member: Node, vanished: bool) -> void:
	var expedition_member: ExpeditionMember = member as ExpeditionMember
	if journal and expedition_member:
		journal.record_loss(expedition_member.display_name, vanished, Encyclopedia.get_data(expedition_member.fate_cause))


func _on_anomaly_observed(member: Node, anomaly_id: StringName) -> void:
	var expedition_member: ExpeditionMember = member as ExpeditionMember
	if journal and expedition_member and not Encyclopedia.HIDDEN_IDS.has(String(anomaly_id)):
		journal.record_observed(expedition_member.display_name, Encyclopedia.get_data(anomaly_id))
