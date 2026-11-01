class_name GapDoor
extends StaticBody3D
## Дверь, всегда приоткрытая на несколько сантиметров; за ней темнота.
## E — закрыть. К следующему обходу щель снова открыта — и шире прежней.

@export var leaf: Node3D

var zone: DoorGapZone


func interact(member: ExpeditionMember) -> void:
	if zone:
		zone.close_door(member)


@rpc("authority", "call_local", "reliable")
func set_gap(angle_deg: float) -> void:
	create_tween().tween_property(leaf, "rotation:y", deg_to_rad(angle_deg), 0.6)
