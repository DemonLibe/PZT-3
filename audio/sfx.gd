class_name Sfx
## Короткие звуки в мире: одноразовый источник, удаляется после проигрывания.


static func play_at(context: Node, stream: AudioStream, position: Vector3, volume_db: float = 0.0, pitch: float = 1.0) -> void:
	if context == null or not context.is_inside_tree() or stream == null:
		return
	var player: AudioStreamPlayer3D = AudioStreamPlayer3D.new()
	player.stream = stream
	player.bus = &"SFX"
	player.volume_db = volume_db
	player.pitch_scale = pitch
	player.unit_size = 6.0
	player.position = position  # прямой потомок корня: локальная позиция = мировая
	player.autoplay = true
	player.finished.connect(player.queue_free)
	# Добавляем отложенно: звук могут попросить из физики, когда дерево занято.
	context.get_tree().root.add_child.call_deferred(player)


## Небольшой случайный разброс высоты, чтобы повторы не резали слух.
static func random_pitch(spread: float = 0.08) -> float:
	return GameState.rng.randf_range(1.0 - spread, 1.0 + spread)
