class_name CompassArrow
extends Control
## Стрелка к цели: поворачивается в сторону следующей фиксации или КПП.

@export var color: Color = Color(0.86, 0.62, 0.3)

## Угол в радианах относительно взгляда (0 — прямо, по часовой — вправо).
var angle: float = 0.0: set = _set_angle


func _draw() -> void:
	var c: Vector2 = size * 0.5
	var r: float = minf(size.x, size.y) * 0.45
	var points: PackedVector2Array = [Vector2(0, -r), Vector2(r * 0.6, r * 0.55), Vector2(0, r * 0.2), Vector2(-r * 0.6, r * 0.55)]
	var rotated: PackedVector2Array = []
	for p in points:
		rotated.append(c + p.rotated(angle))
	draw_colored_polygon(rotated, color)


func _set_angle(value: float) -> void:
	angle = value
	queue_redraw()
