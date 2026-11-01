class_name DinnerZone
extends AnomalyZone
## «Ужин» (Район 1): тёплый стол накрыт на число участников + 1.
## Еда снимает сонливость, но через 3–9 игровых часов съевший теряет цель.

## Узел со всеми тарелками DinnerFood (их должно быть с запасом).
@export var plates_root: Node

var _plates: Array[DinnerFood] = []
var _table_set: bool = false


func _ready() -> void:
	super()
	for child in plates_root.find_children("*", "DinnerFood", true, false):
		_plates.append(child)
		child.zone = self


func _physics_process(delta: float) -> void:
	super(delta)
	if not _table_set and NetAuthority.is_authority():
		_try_set_table()


func _on_member_entered(member: ExpeditionMember) -> void:
	if NetAuthority.is_authority():
		observe(member)


## Участник ест. Вызывается тарелкой на авторитетной стороне.
func eat(member: ExpeditionMember, plate: DinnerFood) -> void:
	if not NetAuthority.is_authority() or not member.can_act() or member.is_eating:
		return
	plate.set_present.rpc(false)
	member.is_eating = true
	await get_tree().create_timer(float(param("eat_duration", 3.0))).timeout
	if not is_instance_valid(member):
		return
	member.is_eating = false
	if not member.is_active():
		return
	member.drowsiness = maxf(0.0, member.drowsiness - float(param("drowsiness_relief", 0.4)))
	if member.has_status(&"ate_dinner"):
		return
	member.add_status(&"ate_dinner")
	var effect: DinnerEffect = DinnerEffect.new()
	effect.name = "DinnerEffect"
	effect.member = member
	effect.data = data
	effect.start_hours = GameState.game_hours
	effect.onset_hours = GameState.rng.randf_range(float(param("onset_min_hours", 3.0)), float(param("onset_max_hours", 9.0)))
	member.body.add_child(effect)


func get_debug_text(member: ExpeditionMember) -> String:
	var effect: DinnerEffect = member.body.get_node_or_null("DinnerEffect") as DinnerEffect
	var places: int = _plates.filter(func(p: DinnerFood) -> bool: return p.visible).size()
	var text: String = "Ужин: тарелок на столе %d, игровое время %.1f ч" % [places, GameState.game_hours]
	if effect:
		text += ", до потери цели %.1f ч" % effect.hours_left()
	return text


## Стол накрывается, когда отряд уже на месте: Squad.size() + 1 тарелок.
func _try_set_table() -> void:
	var squad: Squad = get_tree().get_first_node_in_group(&"squad") as Squad
	if squad == null or squad.size() == 0:
		return
	await get_tree().create_timer(0.5).timeout
	if _table_set:
		return
	_table_set = true
	var places: int = squad.size() + 1
	for i in _plates.size():
		_plates[i].set_present.rpc(i < places)
