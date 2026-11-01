class_name MemberProps
extends Node
## Что участник держит в руках: оружие (Q) и зажигалку (G). Только отображение.

@export var member: ExpeditionMember

var _weapon: MeshInstance3D
var _fire: OmniLight3D


func _ready() -> void:
	var holder: Node3D = member.head if member.head else member.get_parent() as Node3D
	_weapon = MeshInstance3D.new()
	var box: BoxMesh = BoxMesh.new()
	box.size = Vector3(0.06, 0.1, 0.4)
	_weapon.mesh = box
	_weapon.position = Vector3(0.22, -0.3, -0.35)
	holder.add_child.call_deferred(_weapon)
	_fire = OmniLight3D.new()
	_fire.light_color = Color(1.0, 0.6, 0.25)
	_fire.light_energy = 1.4
	_fire.omni_range = 5.0
	_fire.position = Vector3(-0.2, -0.25, -0.35)
	holder.add_child.call_deferred(_fire)


func _process(_delta: float) -> void:
	var active: bool = member.is_active()
	_weapon.visible = active and member.weapon_out
	_fire.visible = active and member.fire_on
