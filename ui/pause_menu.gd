extends CanvasLayer
## Пауза по Esc: продолжить, настройки, прервать вылазку.
## В сетевой игре мир не останавливается.

var _connected: bool = false


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	visible = false
	%ResumeButton.pressed.connect(close)
	%AbortButton.pressed.connect(_abort)
	%SettingsToggle.pressed.connect(func() -> void: $Center/Card/Box/SettingsPanel.visible = not $Center/Card/Box/SettingsPanel.visible)


func _process(_delta: float) -> void:
	if _connected:
		return
	var controller: PlayerController = get_tree().get_first_node_in_group(&"local_controller") as PlayerController
	if controller:
		controller.pause_requested.connect(open)
		_connected = true


func _unhandled_input(event: InputEvent) -> void:
	if visible and event.is_action_pressed(&"ui_cancel"):
		get_viewport().set_input_as_handled()
		close()


func open() -> void:
	visible = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	if not NetAuthority.is_networked():
		get_tree().paused = true
	%ResumeButton.grab_focus()


func close() -> void:
	visible = false
	get_tree().paused = false
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED


## Прервать вылазку: все, кто ещё в районе, считаются не вернувшимися.
func _abort() -> void:
	get_tree().paused = false
	visible = false
	if not NetAuthority.is_authority():
		NetAuthority.end_session()
		get_tree().change_scene_to_file(GameState.BASE_SCENE)
		return
	var squad: Squad = get_tree().get_first_node_in_group(&"squad") as Squad
	var remaining: Array[ExpeditionMember] = squad.active_members() if squad else []
	GameState.end_expedition("вылазка прервана", [], remaining)
