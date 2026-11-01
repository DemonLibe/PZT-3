class_name RadioVoicesZone
extends AnomalyZone
## «Голоса в рации» (Район 24): рация принимает голоса пропавших участников прошлых
## экспедиций. Они зовут на помощь и точно называют координаты группы.
## Ответить ([R]) можно — в ответ тот же вызов, с другой интонацией.

const FALLBACK: PackedStringArray = ["Ковалёв", "Сидоренко", "Ермаков", "Лапина"]
const CALLS: PackedStringArray = [
	"Помогите... Мы во дворе, X %d, Z %d. Вы нас видите?",
	"Приём! Я рядом с вами, X %d, Z %d. Не уходите!",
	"Слышите? Мы тут, X %d, Z %d. Здесь кто-нибудь есть?",
]

var _timer: float = 0.0
var _last: Dictionary = {}


func _ready() -> void:
	super()
	EventBus.radio_replied.connect(_on_replied)


func _physics_process(delta: float) -> void:
	super(delta)
	if not NetAuthority.is_authority() or members.is_empty():
		return
	_timer += delta
	if _timer >= float(param("call_interval", 20.0)):
		_timer = 0.0
		var target: ExpeditionMember = members[GameState.rng.randi_range(0, members.size() - 1)]
		var names: PackedStringArray = _lost_names()
		_last = {"name": names[GameState.rng.randi_range(0, names.size() - 1)],
			"call": CALLS[GameState.rng.randi_range(0, CALLS.size() - 1)], "target": target}
		_say(_last, false)


func _check_rule(member: ExpeditionMember, _delta: float) -> void:
	if not _last.is_empty():
		observe(member)


func get_debug_text(_member: ExpeditionMember) -> String:
	return "Голоса: следующий вызов через %.0f с" % (float(param("call_interval", 20.0)) - _timer)


func _on_replied(_member: Node) -> void:
	if NetAuthority.is_authority() and not _last.is_empty():
		await get_tree().create_timer(2.5).timeout
		_say(_last, true)


func _say(call: Dictionary, again: bool) -> void:
	var target: ExpeditionMember = call["target"]
	if not is_instance_valid(target):
		return
	var pos: Vector3 = target.body.global_position
	var text: String = String(call["call"]) % [int(pos.x), int(pos.z)]
	if again:
		text = text.replace("...", "!").replace("?", "...")
	for member in members:
		member.add_panic(float(param("panic_call", 0.06)))
	_broadcast.rpc("%s (рация)" % call["name"], text)


@rpc("authority", "call_local", "reliable")
func _broadcast(speaker: String, text: String) -> void:
	EventBus.radio_message.emit(speaker, text)


## Имена погибших и пропавших в прошлых экспедициях (из записей Энциклопедии).
func _lost_names() -> PackedStringArray:
	var names: PackedStringArray = []
	for records in Encyclopedia.incidents.values():
		for record in records:
			var parts: PackedStringArray = String(record).split(": ", false, 1)
			if parts.size() == 2:
				var who: String = parts[1].split(" ", false, 1)[0]
				if not names.has(who):
					names.append(who)
	return names if not names.is_empty() else FALLBACK
