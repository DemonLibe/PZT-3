class_name ShadowFigure
extends Node3D
## Отдельная копия тени участника. Пока указывает — не повторяет поворотов,
## а рука тянется за спину участника.

@export var arm: Node3D

var follow: Node3D


func _process(_delta: float) -> void:
	if follow and is_instance_valid(follow):
		global_position = follow.global_position + Vector3(0, 0.02, 0)


## Начать «указывать»: застыть, вытянув руку за спину участника.
func point_behind(body: Node3D, light_position: Vector3) -> void:
	follow = body
	visible = true
	# Тень ложится от источника света...
	var away: Vector3 = body.global_position - light_position
	away.y = 0.0
	if away.length_squared() > 0.001:
		look_at(global_position + away.normalized(), Vector3.UP)
	# ...а рука показывает туда, куда участник стоит спиной.
	var behind: Vector3 = body.global_basis.z
	behind.y = 0.0
	if arm and behind.length_squared() > 0.001:
		arm.look_at(arm.global_position + behind.normalized(), Vector3.UP)


func stop() -> void:
	visible = false
	follow = null
