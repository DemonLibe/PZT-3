class_name EchoZone
extends AnomalyZone
## «Эхо» (Секция 43): любой звук голоса повторяется бесконечно, каждый раз громче
## и с другого направления, уводя внимание. Не идти на эхо — только по оставленным меткам.
## Ушедший на эхо возвращается к началу через часы или сутки — если возвращается.

const VOICE: AudioStream = preload("res://audio/sfx/count_tick.wav")

@export var spots_root: Node
@export var start: Node3D

## Активные источники эха: [{"pos": Vector3, "left": повторов, "phrase": String, "timer": float}]
var _echoes: Array[Dictionary] = []


func _ready() -> void:
	super()
	EventBus.member_spoke.connect(_on_spoke)


func _physics_process(delta: float) -> void:
	super(delta)
	if not NetAuthority.is_authority():
		return
	for echo in _echoes.duplicate():
		echo["timer"] -= delta
		if echo["timer"] <= 0.0:
			echo["timer"] = 2.5
			echo["left"] -= 1
			var spots: Array[Node] = spots_root.get_children()
			echo["pos"] = (spots[GameState.rng.randi_range(0, spots.size() - 1)] as Node3D).global_position
			_repeat.rpc(echo["pos"], echo["phrase"], 4.0 - echo["left"] * 2.0)
			if echo["left"] <= 0:
				_echoes.erase(echo)


func _check_rule(member: ExpeditionMember, _delta: float) -> void:
	for echo in _echoes:
		if member.body.global_position.distance_to(echo["pos"]) < float(param("lure_distance", 2.0)):
			_get_lost(member)
			return


func get_debug_text(_member: ExpeditionMember) -> String:
	return "Эхо: звучит %d" % _echoes.size()


func _on_spoke(member: Node, phrase: String) -> void:
	var expedition_member: ExpeditionMember = member as ExpeditionMember
	if not NetAuthority.is_authority() or expedition_member == null or not members.has(expedition_member):
		return
	observe(expedition_member)
	_echoes.append({"pos": expedition_member.body.global_position, "left": int(param("repeats", 6)), "phrase": phrase, "timer": 1.5})


## Блуждание: участник возвращается к началу через часы — или не возвращается.
func _get_lost(member: ExpeditionMember) -> void:
	EventBus.rule_violated.emit(member, data.id)
	if GameState.rng.randf() < float(param("lost_chance", 0.3)):
		violate(member)
		return
	GameState.debug_skip_hours(GameState.rng.randf_range(float(param("wander_min_hours", 2.0)), float(param("wander_max_hours", 24.0))))
	member.body.global_position = start.global_position
	member.add_panic(0.4)


@rpc("authority", "call_local", "reliable")
func _repeat(at: Vector3, phrase: String, volume_db: float) -> void:
	EventBus.radio_message.emit("Эхо", phrase)
	Sfx.play_at(self, VOICE, at, volume_db, 0.7)
