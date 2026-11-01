class_name WardenRoom
extends Area3D
## Комната, которую проверяет «Смотритель»: дверь и участники внутри.

@export var door: Door
## Точка в коридоре, где Смотритель останавливается проверить комнату.
@export var check_point: Node3D

var members: Array[ExpeditionMember] = []


func _ready() -> void:
	collision_layer = 0
	collision_mask = 2
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)


func occupants() -> Array[ExpeditionMember]:
	return members.filter(func(m: ExpeditionMember) -> bool: return is_instance_valid(m) and m.is_active())


func _on_body_entered(body: Node3D) -> void:
	var member: ExpeditionMember = ExpeditionMember.find_on(body)
	if member and not members.has(member):
		members.append(member)


func _on_body_exited(body: Node3D) -> void:
	members.erase(ExpeditionMember.find_on(body))
