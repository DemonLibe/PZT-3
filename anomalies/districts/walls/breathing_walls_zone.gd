class_name BreathingWallsZone
extends AnomalyZone
## «Дыхание стен» (Район 28): стены тёплые и пульсируют. При контакте ладонью дольше
## минуты пульс наблюдателя синхронизируется со стеной и начинает следовать за ней.

@export var walls_root: Node
@export var glow_material: StandardMaterial3D

## member -> {"wall": стена, "time": секунд контакта}
var _touch: Dictionary = {}
var _clock: float = 0.0


func _ready() -> void:
	super()
	for child in walls_root.find_children("*", "BreathingWall", true, false):
		child.zone = self


func _process(delta: float) -> void:
	_clock += delta
	if glow_material:
		glow_material.emission_energy_multiplier = 0.25 + 0.2 * sin(_clock * 1.3)


func _check_rule(member: ExpeditionMember, delta: float) -> void:
	observe(member)
	if member.has_status(&"wall_pulse"):
		# Пульс теперь идёт за «пульсом» стены.
		member.pulse_bpm = 70.0 + 30.0 * sin(_clock * 0.4)
		return
	if not _touch.has(member):
		return
	var state: Dictionary = _touch[member]
	var wall: Node3D = state["wall"]
	if not member.can_act() or wall.global_position.distance_to(member.body.global_position) > 1.6:
		_touch.erase(member)
		return
	state["time"] += delta
	if state["time"] >= float(param("touch_limit", 60.0)):
		_touch.erase(member)
		member.add_status(&"wall_pulse")
		member.add_panic(float(param("panic_sync", 0.3)))
		EventBus.rule_violated.emit(member, data.id)


func touch(member: ExpeditionMember, wall: BreathingWall) -> void:
	if NetAuthority.is_authority() and member.can_act() and not member.has_status(&"wall_pulse"):
		_touch[member] = {"wall": wall, "time": 0.0}


func get_debug_text(member: ExpeditionMember) -> String:
	if member.has_status(&"wall_pulse"):
		return "Стены: пульс следует за стеной (%.0f)" % member.pulse_bpm
	if _touch.has(member):
		return "Стены: ладонь на стене %.0f / %.0f с" % [_touch[member]["time"], float(param("touch_limit", 60.0))]
	return "Стены: тёплые"
