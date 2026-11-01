class_name GazeSensor
extends RayCast3D
## Взгляд участника: что у него прямо перед глазами и сколько секунд он туда смотрит.

@export var member: ExpeditionMember


func _ready() -> void:
	var body: CollisionObject3D = member.get_parent() as CollisionObject3D
	if body:
		add_exception(body)


func _physics_process(delta: float) -> void:
	if not NetAuthority.is_authority():
		return
	if not member.can_act():
		_set_target(null)
		return
	var target: Node = get_collider() as Node if is_colliding() else null
	if target != null and target == member.gaze_target:
		member.gaze_time += delta
	else:
		_set_target(target)
	if target:
		member.gaze_point = get_collision_point()


func _set_target(target: Node) -> void:
	member.gaze_target = target
	member.gaze_time = 0.0
	member.gaze_label = String(target.name) if target else ""
