class_name RadioZone
extends AnomalyZone
## «Радио» (Район 3): из домов звучат передачи на сутки вперёд, и они сбываются.
## Слушать запрещено, но тишина пугает сильнее. Иногда передача называет время и способ
## гибели участника — и в это время он погибает, если отряд ещё в районе.

const FORECASTS: PackedStringArray = [
	"Прогноз на завтра: облачно, без существенных осадков, ночью до минус трёх.",
	"Завтра с девяти до восемнадцати — отключение горячей воды по улице Ангарской.",
	"Завтра на Каширском шоссе в сторону центра затруднено движение.",
	"Универсам на Вешняковской завтра работает до двадцати двух часов.",
	"Завтра ожидается гололедица. Будьте осторожны на дорогах.",
	"В эфире «Радио Москва». Завтра, двадцать третьего марта, восход в шесть сорок две.",
]
const CAUSES: PackedStringArray = ["остановка сердца", "падение с высоты", "удушье", "причина не названа"]

@export var radios_root: Node

## member -> время (по часам зоны), когда предсказанное случится
var _prophecies: Dictionary = {}
var _clock: float = 0.0
var _broadcast_timer: float = 0.0
var _radios: Array[Node3D] = []


func _ready() -> void:
	super()
	for child in radios_root.get_children():
		_radios.append(child)


func _physics_process(delta: float) -> void:
	_clock += delta
	super(delta)
	if not NetAuthority.is_authority():
		return
	_broadcast_timer += delta
	if _broadcast_timer >= float(param("broadcast_interval", 12.0)):
		_broadcast_timer = 0.0
		_broadcast()
	for member in _prophecies.keys():
		if is_instance_valid(member) and member.is_active() and _clock >= float(_prophecies[member]):
			_prophecies.erase(member)
			violate(member)


func _check_rule(member: ExpeditionMember, delta: float) -> void:
	if is_listening(member):
		observe(member)
		member.add_panic(float(param("panic_listen", 0.008)) * delta)
	else:
		# Отказ слушать пугает сильнее, чем сами передачи.
		member.add_panic(float(param("panic_silence", 0.03)) * delta)


func is_listening(member: ExpeditionMember) -> bool:
	var radius: float = float(param("listen_radius", 6.0))
	for radio in _radios:
		if radio.global_position.distance_to(member.body.global_position) < radius:
			return true
	return false


func get_debug_text(member: ExpeditionMember) -> String:
	var text: String = "Радио: %s" % ("слушает" if is_listening(member) else "не слушает")
	if _prophecies.has(member):
		text += ", предсказано через %.0f с" % (float(_prophecies[member]) - _clock)
	return text


func _broadcast() -> void:
	var listeners: Array[ExpeditionMember] = members.filter(func(m: ExpeditionMember) -> bool:
		return m.is_active() and is_listening(m))
	if listeners.is_empty():
		return
	var text: String = FORECASTS[GameState.rng.randi_range(0, FORECASTS.size() - 1)]
	var targets: Array[ExpeditionMember] = members.filter(func(m: ExpeditionMember) -> bool:
		return m.is_active() and not _prophecies.has(m))
	if not targets.is_empty() and GameState.rng.randf() < float(param("prophecy_chance", 0.15)):
		var target: ExpeditionMember = targets[GameState.rng.randi_range(0, targets.size() - 1)]
		var delay: float = float(param("prophecy_delay", 90.0))
		_prophecies[target] = _clock + delay
		var hours: float = fmod(ExpeditionJournal.START_HOUR + GameState.game_hours + delay * GameState.hours_per_second, 24.0)
		text = "Сегодня в %02d:%02d погибнет %s. Причина: %s." % [int(hours), int(fmod(hours * 60.0, 60.0)),
			target.display_name, CAUSES[GameState.rng.randi_range(0, CAUSES.size() - 1)]]
	for listener in listeners:
		var peer: int = listener.get_parent().get_multiplayer_authority()
		if listener.is_in_group(&"local_member"):
			_tell(text)
		elif NetAuthority.is_networked() and peer != 1:
			_tell.rpc_id(peer, text)


## Передачу слышит только тот, кто стоит у приёмника.
@rpc("authority", "call_remote", "reliable")
func _tell(text: String) -> void:
	EventBus.radio_message.emit("Радио", text)
