class_name GuestDouble
extends StaticBody3D
## Двойник участника: та же фигура, но без тени. Подходит и зовёт «домой».
## E — согласиться (участник уходит с ним). Для напарников — соблазн.

@export var speed: float = 1.2

var zone: GuestsZone
var original: ExpeditionMember
var target: ExpeditionMember


func _ready() -> void:
	add_to_group(&"npc_temptation")
	add_to_group(&"attention_point")


func _physics_process(delta: float) -> void:
	if not NetAuthority.is_authority() or target == null or not is_instance_valid(target):
		return
	var to: Vector3 = target.body.global_position - global_position
	to.y = 0.0
	if to.length() > 1.6:
		global_position += to.normalized() * speed * delta
		look_at(global_position + to.normalized(), Vector3.UP)


func interact(member: ExpeditionMember) -> void:
	if zone:
		zone.go_home(member, self)


func get_temptation(member: ExpeditionMember) -> float:
	return 0.3 + member.panic * 0.6 if member == target else 0.0
