class_name Warden
extends Creature
## «Смотритель» (Секция 36): обходит коридор по Path3D и проверяет комнаты.
## Дверь открыта и внутри человек — забирает.

@export var path: Path3D
@export var rooms_root: Node
## Шаг между точками маршрута, м.
@export var waypoint_spacing: float = 2.0
@export var check_radius: float = 1.0

var _waypoints: PackedVector3Array = []
var _index: int = 0
var _rooms: Array[WardenRoom] = []
## Комнаты, проверенные при текущем проходе мимо них.
var _checked: Dictionary = {}
var _checking: WardenRoom
var _pause_left: float = 0.0


func _ready() -> void:
	super()
	for child in rooms_root.find_children("*", "WardenRoom", true, false):
		_rooms.append(child)
	var curve: Curve3D = path.curve
	var length: float = curve.get_baked_length()
	var d: float = 0.0
	while d < length:
		_waypoints.append(path.global_transform * curve.sample_baked(d))
		d += waypoint_spacing
	state = State.PATROL


func _think(delta: float) -> void:
	if _checking:
		_do_check(delta)
		return
	for room in _rooms:
		var distance: float = _flat_distance(room.check_point.global_position)
		if _checked.has(room) and distance > check_radius * 3.0:
			_checked.erase(room)  # отошёл — при следующем проходе проверит снова
		if not _checked.has(room) and distance < check_radius:
			_checking = room
			_pause_left = float(param("check_pause", 2.0))
			state = State.INVESTIGATE
			stop()
			return
	state = State.PATROL
	if _waypoints.is_empty():
		return
	if _flat_distance(_waypoints[_index]) < 0.8:
		_index += 1
		if _index >= _waypoints.size():
			_index = 0
	move_to(_waypoints[_index], float(param("patrol_speed", 2.0)))


func get_debug_text(_member: ExpeditionMember) -> String:
	var where: String = " (комната %s)" % _checking.name if _checking else ""
	return "Смотритель: %s%s" % [State.keys()[state], where]


func _do_check(delta: float) -> void:
	face_point(_checking.door.global_position, delta)
	_pause_left -= delta
	if _pause_left > 0.0:
		return
	if _checking.door.is_open:
		for member in _checking.occupants():
			punish(member)
	_checked[_checking] = true
	_checking = null


func _flat_distance(point: Vector3) -> float:
	return Vector2(global_position.x - point.x, global_position.z - point.z).length()
