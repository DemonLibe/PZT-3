class_name SilentZone
extends AnomalyZone
## «Тихий» (Секция 45): невидимое существо; признак — расширяющаяся зона полной тишины,
## где пропадают даже свои шаги и дыхание. Почувствовал тишину — отступай туда, откуда пришёл.
## Остался внутри дольше минуты — не обнаружен.

@export var creature: Node3D

var _radius: float = 0.0
## member -> секунд в тишине
var _inside: Dictionary = {}


func _physics_process(delta: float) -> void:
	super(delta)
	if not NetAuthority.is_authority():
		return
	_radius = minf(float(param("max_radius", 7.0)), _radius + float(param("grow_speed", 0.3)) * delta)
	var squad: Squad = get_tree().get_first_node_in_group(&"squad") as Squad
	if squad and squad.leader:
		var to: Vector3 = squad.leader.body.global_position - creature.global_position
		to.y = 0.0
		if to.length() > 1.0:
			creature.global_position += to.normalized() * float(param("speed", 0.6)) * delta


func _check_rule(member: ExpeditionMember, delta: float) -> void:
	var inside: bool = creature.global_position.distance_to(member.body.global_position) < _radius
	if not inside:
		if member.has_status(&"silence"):
			member.remove_status(&"silence")
		_inside.erase(member)
		return
	observe(member)
	member.add_status(&"silence")
	_inside[member] = float(_inside.get(member, 0.0)) + delta
	if _inside[member] >= float(param("vanish_after", 60.0)):
		_inside.erase(member)
		member.remove_status(&"silence")
		violate(member)


func get_debug_text(member: ExpeditionMember) -> String:
	return "Тихий: тишина %.1f м, внутри %.0f / %.0f с" % [_radius, float(_inside.get(member, 0.0)), float(param("vanish_after", 60.0))]
