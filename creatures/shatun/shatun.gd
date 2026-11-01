class_name Shatun
extends Creature
## «Шатун» (Секция 31): безостановочно бродит шатающейся походкой, маршрут без логики,
## иногда заходит в комнаты. Оказался в створе его движения — разорван.

@export var waypoints_root: Node

var _points: Array[Vector3] = []
var _repick: float = 0.0
var _clock: float = 0.0


func _ready() -> void:
	super()
	for point in waypoints_root.get_children():
		_points.append((point as Node3D).global_position)
	state = State.PATROL


func _think(delta: float) -> void:
	_clock += delta
	_repick -= delta
	if _repick <= 0.0 or not is_moving():
		_repick = GameState.rng.randf_range(2.0, float(param("repick_time", 6.0)))
		if not _points.is_empty():
			# Шатающаяся скорость: то быстрее, то медленнее.
			move_to(_points[GameState.rng.randi_range(0, _points.size() - 1)], float(param("walk_speed", 1.8)))
	_speed = float(param("walk_speed", 1.8)) * (0.6 + 0.6 * absf(sin(_clock * 2.3)))
	var forward: Vector3 = -global_basis.z
	for member in all_members():
		var to: Vector3 = member.body.global_position - global_position
		to.y = 0.0
		if to.length() < float(param("path_distance", 3.5)) and \
				rad_to_deg(forward.angle_to(to.normalized())) < float(param("path_cone_deg", 40.0)) * 0.5:
			punish(member)
