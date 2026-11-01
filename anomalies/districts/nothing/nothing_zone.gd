class_name NothingZone
extends AnomalyZone
## «Ничего» (Район 30): аномалий не зафиксировано. Все журналы обрываются записью о входе.
## В глубине двора застройка переходит в бетонный коридор — дальше Гигадом.

@export var threshold: Area3D
## Чем заканчивается журнал и какое направление отметить пройденным.
@export var outcome_text: String = "запись о входе в Район 30. Дальнейших записей нет"
@export var completed_title: String = "Район 30"

var _done: bool = false


func _ready() -> void:
	super()
	threshold.collision_layer = 0
	threshold.collision_mask = 2
	threshold.body_entered.connect(_on_threshold)


func _on_member_entered(member: ExpeditionMember) -> void:
	observe(member)


func _on_threshold(body: Node3D) -> void:
	var member: ExpeditionMember = ExpeditionMember.find_on(body)
	if _done or member == null or not member.is_in_group(&"local_member") and body.name != "1":
		return
	if not NetAuthority.is_authority():
		return
	_done = true
	Encyclopedia.open_article(data.id, Encyclopedia.LEVEL_FULL)
	Encyclopedia.mark_completed(completed_title)
	var squad: Squad = get_tree().get_first_node_in_group(&"squad") as Squad
	var everyone: Array[ExpeditionMember] = squad.active_members() if squad else [member]
	GameState.end_expedition(outcome_text, everyone, [])
