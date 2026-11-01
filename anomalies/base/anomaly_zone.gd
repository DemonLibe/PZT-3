class_name AnomalyZone
extends Area3D
## Зона аномалии: следит за участниками внутри и проверяет правило каждый кадр.
## Наследники переопределяют _check_rule(member, delta).

@export var data: AnomalyData

var members: Array[ExpeditionMember] = []
var _observed: Dictionary = {}


func _ready() -> void:
	collision_layer = 0
	collision_mask = 2
	monitorable = false
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)
	add_to_group(&"debug_info")


func _physics_process(delta: float) -> void:
	if not NetAuthority.is_authority():
		return
	for member in members.duplicate():
		if is_instance_valid(member) and member.is_active():
			_check_rule(member, delta)


## Проверка правила для одного участника. Переопределяется в наследниках.
func _check_rule(_member: ExpeditionMember, _delta: float) -> void:
	pass


## Участник вошёл в зону (вызывается только на авторитетной стороне).
func _on_member_entered(_member: ExpeditionMember) -> void:
	pass


## Участник вышел из зоны (вызывается только на авторитетной стороне).
func _on_member_exited(_member: ExpeditionMember) -> void:
	pass


func violate(member: ExpeditionMember) -> void:
	if data:
		data.punish(member)


## Участник впервые заметил аномалию — статья Энциклопедии откроется частично.
func observe(member: ExpeditionMember) -> void:
	if _observed.has(member) or data == null:
		return
	_observed[member] = true
	EventBus.anomaly_observed.emit(member, data.id)


func param(key: String, default: Variant = null) -> Variant:
	return data.param(key, default) if data else default


## Строка для отладочного HUD. Переопределяется в наследниках.
func get_debug_text(_member: ExpeditionMember) -> String:
	return ""


func _on_body_entered(body: Node3D) -> void:
	var member: ExpeditionMember = ExpeditionMember.find_on(body)
	if member and not members.has(member):
		members.append(member)
		if NetAuthority.is_authority():
			_on_member_entered(member)


func _on_body_exited(body: Node3D) -> void:
	var member: ExpeditionMember = ExpeditionMember.find_on(body)
	if member and members.has(member):
		members.erase(member)
		# Тело удаляют со сцены (выход с уровня, отключение) — реагировать не нужно.
		if NetAuthority.is_authority() and body.is_inside_tree() and member.is_inside_tree() and is_inside_tree():
			_on_member_exited(member)
