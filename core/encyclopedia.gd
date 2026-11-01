extends Node
## Энциклопедия: какие статьи открыты и записи о пропавших.
## Наблюдение открывает статью частично, нарушение правила — полностью.
## Сохраняется в user://encyclopedia.json.

signal article_opened(anomaly_id: StringName, level: int)

const SAVE_PATH: String = "user://encyclopedia.json"
const DATA_DIR: String = "res://data"
const LEVEL_NONE: int = 0
const LEVEL_OBSERVED: int = 1
const LEVEL_FULL: int = 2
## Отладочные аномалии в Энциклопедию не попадают.
const HIDDEN_IDS: PackedStringArray = ["test_cube"]

## id аномалии -> степень открытия статьи
var opened_articles: Dictionary = {}
## id аномалии -> список записей о пропавших и погибших
var incidents: Dictionary = {}
var expedition_count: int = 0

var _data_cache: Dictionary = {}


func _ready() -> void:
	load_from_disk()
	EventBus.anomaly_observed.connect(func(_m: Node, id: StringName) -> void: open_article(id, LEVEL_OBSERVED))
	EventBus.rule_violated.connect(func(_m: Node, id: StringName) -> void: open_article(id, LEVEL_FULL))
	print("[Encyclopedia] готов, статей открыто: ", opened_articles.size())


func open_article(anomaly_id: StringName, level: int) -> void:
	var key: String = String(anomaly_id)
	if HIDDEN_IDS.has(key) or int(opened_articles.get(key, LEVEL_NONE)) >= level:
		return
	opened_articles[key] = level
	article_opened.emit(anomaly_id, level)
	save_to_disk()


func article_level(anomaly_id: StringName) -> int:
	return int(opened_articles.get(String(anomaly_id), LEVEL_NONE))


func add_incident(anomaly_id: StringName, text: String) -> void:
	var key: String = String(anomaly_id)
	if not incidents.has(key):
		incidents[key] = []
	incidents[key].append(text)


## Все аномалии среза (по файлам в res://data).
func list_ids() -> PackedStringArray:
	var ids: PackedStringArray = []
	for file in DirAccess.get_files_at(DATA_DIR):
		var clean: String = file.trim_suffix(".remap")
		if clean.ends_with(".tres") and not HIDDEN_IDS.has(clean.get_basename()):
			ids.append(clean.get_basename())
	ids.sort()
	return ids


func get_data(anomaly_id: StringName) -> AnomalyData:
	var key: String = String(anomaly_id)
	if not _data_cache.has(key):
		var path: String = "%s/%s.tres" % [DATA_DIR, key]
		_data_cache[key] = load(path) if ResourceLoader.exists(path) else null
	return _data_cache[key]


func get_title(anomaly_id: StringName) -> String:
	var data: AnomalyData = get_data(anomaly_id)
	if data == null or article_level(anomaly_id) == LEVEL_NONE:
		return "Запись не открыта"
	return "%s — %s" % [data.display_name, data.location]


## Текст статьи с учётом того, насколько она открыта.
func get_article_text(anomaly_id: StringName) -> String:
	var data: AnomalyData = get_data(anomaly_id)
	var level: int = article_level(anomaly_id)
	if data == null or level == LEVEL_NONE:
		return "Данные отсутствуют."
	var parts: PackedStringArray = data.encyclopedia_text.split("---", false, 1)
	var text: String = "Опасность: %d из 5\n\n%s" % [data.danger_level, parts[0].strip_edges()]
	if level >= LEVEL_FULL and parts.size() > 1:
		text += "\n\n" + parts[1].strip_edges()
	else:
		text += "\n\nПравило: не задокументировано."
	var records: Array = incidents.get(String(anomaly_id), [])
	if not records.is_empty():
		text += "\n\nЗаписи экспедиций:\n— " + "\n— ".join(PackedStringArray(records))
	return text


func save_to_disk() -> void:
	var file: FileAccess = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file == null:
		push_warning("[Encyclopedia] не удалось сохранить: %d" % FileAccess.get_open_error())
		return
	file.store_string(JSON.stringify({
		"articles": opened_articles, "incidents": incidents, "expedition_count": expedition_count}, "\t"))


func load_from_disk() -> void:
	if not FileAccess.file_exists(SAVE_PATH):
		return
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(SAVE_PATH))
	if parsed is Dictionary:
		opened_articles = parsed.get("articles", {})
		incidents = parsed.get("incidents", {})
		expedition_count = int(parsed.get("expedition_count", 0))


## Отладка: стереть всё.
func reset() -> void:
	opened_articles = {}
	incidents = {}
	expedition_count = 0
	save_to_disk()
