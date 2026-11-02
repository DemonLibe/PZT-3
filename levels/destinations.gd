class_name Destinations
## Куда можно отправить экспедицию с базы. Проход строго по порядку списка:
## следующее направление открывается, когда задание в предыдущем выполнено.

const LIST: Array = [
	{"title": "Район 1", "path": "res://levels/district_01_dinner.tscn", "anomaly": "dinner"},
	{"title": "Район 2", "path": "res://levels/district_02_windows.tscn", "anomaly": "windows"},
	{"title": "Район 3", "path": "res://levels/district_03_radio.tscn", "anomaly": "radio"},
	{"title": "Район 4", "path": "res://levels/district_04_laundry.tscn", "anomaly": "laundry"},
	{"title": "Район 5", "path": "res://levels/district_05_mirror.tscn", "anomaly": "mirror"},
	{"title": "Район 6", "path": "res://levels/district_06_shadow.tscn", "anomaly": "shadow"},
	{"title": "Район 7", "path": "res://levels/district_07_guests.tscn", "anomaly": "guests"},
	{"title": "Район 8", "path": "res://levels/district_08_sleep.tscn", "anomaly": "sleep"},
	{"title": "Район 9", "path": "res://levels/district_09_smile.tscn", "anomaly": "smile"},
	{"title": "Район 10", "path": "res://levels/district_10_kitchen.tscn", "anomaly": "kitchen"},
	{"title": "Район 11", "path": "res://levels/district_11_silence.tscn", "anomaly": "silence"},
	{"title": "Район 12", "path": "res://levels/district_12_reflection.tscn", "anomaly": "reflection"},
	{"title": "Район 13", "path": "res://levels/district_13_clocks.tscn", "anomaly": "clocks"},
	{"title": "Район 14", "path": "res://levels/district_14_mail.tscn", "anomaly": "mail"},
	{"title": "Район 16", "path": "res://levels/district_16_lullaby.tscn", "anomaly": "lullaby"},
	{"title": "Район 18", "path": "res://levels/district_18_photos.tscn", "anomaly": "photos"},
	{"title": "Район 20", "path": "res://levels/district_20_steps.tscn", "anomaly": "steps"},
	{"title": "Район 21", "path": "res://levels/district_21_door.tscn", "anomaly": "door"},
	{"title": "Район 24", "path": "res://levels/district_24_voices.tscn", "anomaly": "voices"},
	{"title": "Район 25", "path": "res://levels/district_25_ceiling.tscn", "anomaly": "ceiling"},
	{"title": "Район 27", "path": "res://levels/district_27_companion.tscn", "anomaly": "companion"},
	{"title": "Район 28", "path": "res://levels/district_28_walls.tscn", "anomaly": "walls"},
	{"title": "Район 30", "path": "res://levels/district_30_nothing.tscn", "anomaly": "nothing"},
	{"title": "Гигадом, секция 30", "path": "res://levels/section_30_threshold.tscn", "anomaly": "threshold"},
	{"title": "Гигадом, секция 31", "path": "res://levels/section_31_shatun.tscn", "anomaly": "shatun"},
	{"title": "Гигадом, секция 32", "path": "res://levels/section_32_cradle.tscn", "anomaly": "cradle"},
	{"title": "Гигадом, секция 33", "path": "res://levels/section_33_barracks.tscn", "anomaly": "barracks"},
	{"title": "Гигадом, секция 34", "path": "res://levels/section_34_weaver.tscn", "anomaly": "weaver"},
	{"title": "Гигадом, секция 35", "path": "res://levels/section_35_choir.tscn", "anomaly": "choir"},
	{"title": "Гигадом, секция 36", "path": "res://levels/section_36_warden.tscn", "anomaly": "warden"},
	{"title": "Гигадом, секция 37", "path": "res://levels/section_37_butcher.tscn", "anomaly": "butcher"},
	{"title": "Гигадом, секция 38", "path": "res://levels/section_38_mourners.tscn", "anomaly": "mourners"},
	{"title": "Гигадом, секция 39", "path": "res://levels/section_39_grinder.tscn", "anomaly": "grinder"},
	{"title": "Гигадом, секция 40", "path": "res://levels/section_40_keymaster.tscn", "anomaly": "keymaster"},
	{"title": "Гигадом, секция 41", "path": "res://levels/section_41_firemen.tscn", "anomaly": "firemen"},
	{"title": "Гигадом, секция 42", "path": "res://levels/section_42_puppeteer.tscn", "anomaly": "puppeteer"},
	{"title": "Гигадом, секция 43", "path": "res://levels/section_43_echo.tscn", "anomaly": "echo"},
	{"title": "Гигадом, секция 44", "path": "res://levels/section_44_collector.tscn", "anomaly": "collector"},
	{"title": "Гигадом, секция 45", "path": "res://levels/section_45_silent.tscn", "anomaly": "silent"},
	{"title": "Гигадом, секция 46", "path": "res://levels/section_46_nurse.tscn", "anomaly": "nurse"},
	{"title": "Гигадом, секция 47", "path": "res://levels/section_47_judge.tscn", "anomaly": "judge"},
	{"title": "Гигадом, секция 48", "path": "res://levels/section_48_convoy.tscn", "anomaly": "convoy"},
	{"title": "Гигадом, секция 49", "path": "res://levels/section_49_shaft.tscn", "anomaly": "shaft"},
	{"title": "Гигадом, секция 50", "path": "res://levels/section_50_threshold.tscn", "anomaly": "threshold2"},
]


static func is_unlocked(index: int) -> bool:
	return index == 0 or Encyclopedia.is_completed(LIST[index - 1]["title"])


## Первое невыполненное направление (или последнее, если всё пройдено).
static func current_index() -> int:
	for i in LIST.size():
		if not Encyclopedia.is_completed(LIST[i]["title"]):
			return i
	return LIST.size() - 1
