class_name KeyMasterZone
extends AnomalyZone
## «Хозяин ключей» (Секция 40): единственная сущность, вступающая в диалог.
## Предлагает ключ от любой двери в обмен на нечто нематериальное. Любой обмен запрещён:
## отданное теряется навсегда, а ключ не подходит ни к одной двери.

const PRICES: Array = [
	{"text": "твоё имя", "status": &"nameless"},
	{"text": "одно воспоминание — самое тёплое", "status": &"lost_memory"},
	{"text": "мизинец", "status": &"lost_finger"},
]

@export var master: KeyMaster

## member -> {"price": индекс, "until": до какого времени действует предложение}
var _offers: Dictionary = {}


func _ready() -> void:
	super()
	master.zone = self


func _on_member_entered(member: ExpeditionMember) -> void:
	observe(member)


func talk(member: ExpeditionMember) -> void:
	if not NetAuthority.is_authority() or not member.can_act():
		return
	var now: float = Time.get_ticks_msec() / 1000.0
	if _offers.has(member) and now < float(_offers[member]["until"]):
		_trade(member, PRICES[_offers[member]["price"]])
		_offers.erase(member)
		return
	var index: int = GameState.rng.randi_range(0, PRICES.size() - 1)
	_offers[member] = {"price": index, "until": now + float(param("offer_time", 10.0))}
	_say("Ключ откроет любую запертую дверь секции. Взамен — %s. Согласен? [E]" % PRICES[index]["text"])


func get_debug_text(member: ExpeditionMember) -> String:
	return "Хозяин ключей: %s" % ("ждёт ответа" if _offers.has(member) else ("ключ взят" if member.has_status(&"has_useless_key") else "молчит"))


func _trade(member: ExpeditionMember, price: Dictionary) -> void:
	member.add_status(price["status"])
	member.add_status(&"has_useless_key")
	member.fate_cause = data.id
	EventBus.rule_violated.emit(member, data.id)
	_say("Договорились.")


func _say(text: String) -> void:
	_broadcast.rpc(text)


@rpc("authority", "call_local", "reliable")
func _broadcast(text: String) -> void:
	EventBus.radio_message.emit("Хозяин ключей", text)
