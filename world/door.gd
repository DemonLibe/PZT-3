class_name Door
extends StaticBody3D
## Дверь: открыта или закрыта. E — открыть/закрыть.
## Напарники с auto_doors открывают её сами и закрывают за собой —
## если не забудут в панике.

signal opened_changed(is_open: bool)

## Створка, которая поворачивается (её центр вращения — петли).
@export var leaf: Node3D
## Форма столкновения створки — поворачивается вместе с ней.
@export var shape: CollisionShape3D
## Зона у двери, где напарники открывают её сами.
@export var trigger: Area3D
## Данные «Смотрителя»: оттуда шанс забыть закрыть дверь.
@export var forget_data: AnomalyData
@export var open_angle_deg: float = 95.0

var is_open: bool = false

var _opened_by_auto: bool = false
var _hinge_angle: float = 0.0
var _shape_offset: Transform3D


func _ready() -> void:
	collision_layer = 4
	collision_mask = 0
	if leaf and shape:
		_shape_offset = Transform3D(Basis(), leaf.position).affine_inverse() * shape.transform
	if trigger:
		trigger.collision_layer = 0
		trigger.collision_mask = 2
		trigger.body_entered.connect(_on_trigger_entered)
		trigger.body_exited.connect(_on_trigger_exited)


func interact(_member: ExpeditionMember) -> void:
	if NetAuthority.is_authority():
		_opened_by_auto = false
		set_open.rpc(not is_open)


@rpc("authority", "call_local", "reliable")
func set_open(value: bool) -> void:
	is_open = value
	var tween: Tween = create_tween()
	tween.tween_method(_set_hinge_angle, _hinge_angle, deg_to_rad(open_angle_deg) if value else 0.0, 0.35)
	opened_changed.emit(value)


func _set_hinge_angle(angle: float) -> void:
	_hinge_angle = angle
	if leaf:
		leaf.rotation.y = angle
		if shape:
			shape.transform = Transform3D(Basis(Vector3.UP, angle), leaf.position) * _shape_offset


func _on_trigger_entered(body: Node3D) -> void:
	var member: ExpeditionMember = ExpeditionMember.find_on(body)
	if not NetAuthority.is_authority() or member == null or not member.auto_doors or not member.can_act():
		return
	if not is_open:
		_opened_by_auto = true
		set_open.rpc(true)


func _on_trigger_exited(body: Node3D) -> void:
	var member: ExpeditionMember = ExpeditionMember.find_on(body)
	if not NetAuthority.is_authority() or member == null or not member.auto_doors:
		return
	if not is_open or not _opened_by_auto or not body.is_inside_tree():
		return
	for other in trigger.get_overlapping_bodies():
		if other != body and ExpeditionMember.find_on(other):
			return  # кто-то ещё в проходе
	var chance: float = float(forget_data.param("npc_forget_door_chance", 0.1)) if forget_data else 0.0
	if GameState.rng.randf() < chance * member.panic:
		return  # забыл закрыть
	_opened_by_auto = false
	set_open.rpc(false)
