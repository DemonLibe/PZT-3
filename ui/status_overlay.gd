extends CanvasLayer
## Состояния локального участника: экранный эффект и список «что со мной».
## Скрытые статусы (ate_dinner, wore_laundry и др.) не показываются — по правилам аномалий.

## статус -> [название, пояснение, цвет краёв, сила, пульс, обесцвечивание, текстура ткани]
const EFFECTS: Dictionary = {
	&"fabric_skin": ["Кожа как ткань", "Плотная, со швами. Бег невозможен.", Color(0.55, 0.5, 0.45), 0.55, 0.0, 0.1, true],
	&"burns": ["Ожоги", "Огня не касались — а жжёт.", Color(0.8, 0.25, 0.1), 0.6, 3.0, 0.0, false],
	&"smiled": ["Лицо сводит улыбкой", "Мышцы не расслабляются.", Color(0.6, 0.15, 0.15), 0.35, 1.2, 0.0, false],
	&"smile_fixed": ["Улыбка навсегда", "Лицо больше не слушается.", Color(0.7, 0.1, 0.1), 0.55, 0.8, 0.2, false],
	&"nameless": ["Без имени", "Вы не помните, как вас зовут.", Color(0.4, 0.4, 0.45), 0.5, 0.0, 0.55, false],
	&"lost_purpose": ["Нет цели", "Зачем куда-то идти? Здесь тепло.", Color(0.85, 0.65, 0.35), 0.45, 0.4, 0.3, false],
	&"marked": ["Меченый", "Кто-то собирает ваши вещи. И ходит рядом.", Color(0.1, 0.1, 0.1), 0.7, 0.6, 0.15, false],
	&"memory_gap": ["Провал в памяти", "Несколько часов — как вырезаны.", Color(0.2, 0.2, 0.3), 0.45, 0.0, 0.4, false],
	&"wall_pulse": ["Чужой пульс", "Сердце бьётся в ритме стены.", Color(0.6, 0.2, 0.2), 0.5, 2.2, 0.0, false],
	&"read_letter": ["Письмо", "Не выходит из головы.", Color(0.3, 0.3, 0.35), 0.25, 0.0, 0.1, false],
	&"silence": ["Тишина", "Слышно только своё сердце.", Color(0.05, 0.05, 0.08), 0.5, 0.0, 0.65, false],
	&"hallucinating": ["Галлюцинации", "Вы видите то, чего нет.", Color(0.45, 0.2, 0.45), 0.4, 1.5, 0.0, false],
	&"own_clock": ["Свои часы", "Ваши часы показывают своё время.", Color(0.2, 0.25, 0.3), 0.2, 0.0, 0.0, false],
	&"compelled": ["Ноги несут сами", "Вас тянет к кругу.", Color(0.25, 0.25, 0.3), 0.65, 1.0, 0.5, false],
	&"has_useless_key": ["Ключ", "Не подходит ни к одной двери.", Color(0.7, 0.6, 0.2), 0.2, 0.0, 0.0, false],
	&"lost_memory": ["Отданное воспоминание", "Что-то тёплое — исчезло.", Color(0.3, 0.3, 0.35), 0.35, 0.0, 0.35, false],
	&"lost_finger": ["Нет пальца", "Отдан за ключ.", Color(0.5, 0.15, 0.1), 0.3, 0.0, 0.0, false],
	&"struck_double": ["Удар дублю", "Он вернётся.", Color(0.5, 0.1, 0.1), 0.3, 0.7, 0.0, false],
}

@onready var _rect: ColorRect = $Effect
@onready var _list: Label = %StatusList
@onready var _list_panel: Control = %StatusPanel


func _process(_delta: float) -> void:
	var member: ExpeditionMember = get_tree().get_first_node_in_group(&"local_member") as ExpeditionMember
	var active: Array = []
	if member and member.is_active():
		for id in member.statuses.keys():
			if EFFECTS.has(id):
				active.append(EFFECTS[id])
	_apply(active)


func _apply(active: Array) -> void:
	var material: ShaderMaterial = _rect.material as ShaderMaterial
	_rect.visible = not active.is_empty()
	_list_panel.visible = not active.is_empty()
	if active.is_empty():
		return
	# Самый сильный эффект задаёт край экрана, обесцвечивание берём максимальное.
	active.sort_custom(func(a: Array, b: Array) -> bool: return a[3] > b[3])
	var top: Array = active[0]
	material.set_shader_parameter(&"edge_color", top[2])
	material.set_shader_parameter(&"edge_strength", top[3])
	material.set_shader_parameter(&"pulse_speed", top[4])
	material.set_shader_parameter(&"texture_mix", 1.0 if top[6] else 0.0)
	var gray: float = 0.0
	var lines: PackedStringArray = []
	for effect in active:
		gray = maxf(gray, effect[5])
		lines.append("%s — %s" % [effect[0], effect[1]])
	material.set_shader_parameter(&"desaturate", gray)
	_list.text = "\n".join(lines)
