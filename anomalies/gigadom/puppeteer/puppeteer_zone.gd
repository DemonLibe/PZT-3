class_name PuppeteerZone
extends AnomalyZone
## «Кукольник» (Секция 42): издали управляет дублями — резкими, будто на нитях.
## Не атаковать дублей. Ударивший получает те же повреждения зеркально, через несколько часов.

@export var doubles_root: Node

var _jerk: float = 0.0


func _ready() -> void:
	super()
	for child in doubles_root.find_children("*", "PuppetDouble", true, false):
		child.zone = self


func _physics_process(delta: float) -> void:
	super(delta)
	if not NetAuthority.is_authority():
		return
	_jerk -= delta
	if _jerk <= 0.0:
		_jerk = GameState.rng.randf_range(0.4, 1.4)
		for double in doubles_root.get_children():
			var step: Vector3 = Vector3(GameState.rng.randf_range(-0.6, 0.6), 0, GameState.rng.randf_range(-0.6, 0.6))
			_twitch.rpc(double.name, step, GameState.rng.randf_range(-1.5, 1.5))


func _check_rule(member: ExpeditionMember, _delta: float) -> void:
	for double in doubles_root.get_children():
		if (double as Node3D).global_position.distance_to(member.body.global_position) < 10.0:
			observe(member)
			return


func attack(member: ExpeditionMember, double: PuppetDouble) -> void:
	if not NetAuthority.is_authority() or not member.can_act():
		return
	_twitch.rpc(double.name, Vector3.ZERO, PI)
	member.add_status(&"struck_double")
	EventBus.rule_violated.emit(member, data.id)
	DelayedPunishment.attach(member, data, "MirrorWounds", "onset_min_hours", "onset_max_hours")


func get_debug_text(member: ExpeditionMember) -> String:
	var effect: DelayedPunishment = member.body.get_node_or_null("MirrorWounds") as DelayedPunishment
	return "Кукольник: %s" % ("удар вернётся через %.1f ч" % effect.hours_left() if effect else "дубли дёргаются")


@rpc("authority", "call_local", "unreliable")
func _twitch(double_name: String, step: Vector3, turn: float) -> void:
	var double: Node3D = doubles_root.get_node_or_null(double_name) as Node3D
	if double:
		double.global_position += step
		double.rotate_y(turn)
