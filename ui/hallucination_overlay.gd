extends CanvasLayer
## Галлюцинации локального участника («Потолок»): плывущая картинка и смещение цветов.

@onready var _rect: ColorRect = $Rect


func _process(_delta: float) -> void:
	var member: ExpeditionMember = get_tree().get_first_node_in_group(&"local_member") as ExpeditionMember
	_rect.visible = member != null and member.is_active() and member.has_status(&"hallucinating")
