class_name ClocksZone
extends AnomalyZone
## «Часы» (Район 13): у каждого участника свои часы — со своим постоянным сдвигом.
## Чем дольше отряд в районе, тем ближе показания; при полной синхронизации — потеря группы.

@export var wall_clocks_root: Node

var _time_inside: float = 0.0
var _synced: bool = false


func _physics_process(delta: float) -> void:
	super(delta)
	if not NetAuthority.is_authority() or members.is_empty():
		return
	_time_inside += delta
	var sync_time: float = float(param("sync_time", 240.0))
	var left: float = maxf(0.0, 1.0 - _time_inside / sync_time)
	for member in members:
		member.watch_offset_min = _base_offset(member) * left
	_update_wall_clocks.rpc(left)
	if left <= 0.0 and not _synced:
		_synced = true
		for member in members.duplicate():
			violate(member)


func _on_member_entered(member: ExpeditionMember) -> void:
	member.add_status(&"own_clock")
	member.watch_offset_min = _base_offset(member)
	observe(member)


func _on_member_exited(member: ExpeditionMember) -> void:
	member.remove_status(&"own_clock")
	member.watch_offset_min = 0.0


func get_debug_text(member: ExpeditionMember) -> String:
	return "Часы: сдвиг %+.0f мин, до синхронизации %.0f с" % [member.watch_offset_min,
		maxf(0.0, float(param("sync_time", 240.0)) - _time_inside)]


## Сдвиг строго индивидуальный и повторяется при повторном входе — от имени участника.
func _base_offset(member: ExpeditionMember) -> float:
	var spread: float = float(param("max_offset_min", 90.0))
	return float(absi(hash(member.display_name)) % 1000) / 1000.0 * spread * 2.0 - spread


@rpc("authority", "call_local", "unreliable_ordered")
func _update_wall_clocks(left: float) -> void:
	if wall_clocks_root == null:
		return
	var i: int = 0
	for clock in wall_clocks_root.get_children():
		var label: Label3D = clock as Label3D
		if label:
			var minutes: float = fmod((ExpeditionJournal.START_HOUR + GameState.game_hours) * 60.0 + (i * 37 % 120 - 60) * left, 1440.0)
			label.text = "%02d:%02d" % [int(minutes / 60.0), int(fmod(minutes, 60.0))]
		i += 1
