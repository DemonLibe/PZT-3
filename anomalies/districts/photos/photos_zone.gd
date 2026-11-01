class_name PhotosZone
extends AnomalyZone
## «Фотографии» (Район 18): семейные снимки на стенах. С каждым визитом в район
## ещё одно лицо меняется на лицо участника — в порядке, в каком они входили.

@export var photos_root: Node

var _seen_self: Dictionary = {}


func _ready() -> void:
	super()
	if NetAuthority.is_authority():
		Encyclopedia.add_visit(data.id)
	_refresh.call_deferred()


func _check_rule(member: ExpeditionMember, _delta: float) -> void:
	for photo in photos_root.get_children():
		var at: Vector3 = (photo as Node3D).global_position
		if at.distance_to(member.get_gaze_origin()) < 6.0 and member.is_in_view_cone(at, 15.0):
			observe(member)
			var label: Label3D = photo.get_node_or_null("Caption") as Label3D
			if label and label.text.contains(member.display_name) and not _seen_self.has(member):
				_seen_self[member] = true
				member.add_panic(float(param("panic_self", 0.25)))


func get_debug_text(_member: ExpeditionMember) -> String:
	return "Фотографии: визит %d" % Encyclopedia.visits_of(data.id)


## Сколько снимков уже «переписано»: на один меньше, чем визитов.
func _refresh() -> void:
	await get_tree().create_timer(1.0).timeout
	var squad: Squad = get_tree().get_first_node_in_group(&"squad") as Squad
	var names: PackedStringArray = []
	if squad:
		for member in squad.members:
			names.append(member.display_name)
	var changed: int = mini(Encyclopedia.visits_of(data.id) - 1, photos_root.get_child_count())
	var i: int = 0
	for photo in photos_root.get_children():
		var label: Label3D = photo.get_node_or_null("Caption") as Label3D
		if label:
			label.text = ("На снимке: %s" % names[i % names.size()]) if i < changed and not names.is_empty() else "Семья, 1987"
		i += 1
