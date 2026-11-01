class_name LullabyZone
extends AnomalyZone
## «Колыбельная» (Район 16): из одного дома звучит знакомая всем колыбельная.
## Дослушал до конца (~6 мин) — забыл своё имя навсегда. Прерывать до 5-й минуты.

@export var source: Node3D

## member -> {"heard": секунд подряд, "away": секунд вне слышимости}
var _listen: Dictionary = {}
var _warned: Dictionary = {}


func _check_rule(member: ExpeditionMember, delta: float) -> void:
	if member.has_status(&"nameless"):
		return
	var state: Dictionary = _listen.get(member, {"heard": 0.0, "away": 0.0})
	if source.global_position.distance_to(member.body.global_position) < float(param("listen_radius", 12.0)):
		observe(member)
		state["heard"] += delta
		state["away"] = 0.0
	else:
		state["away"] += delta
		if state["away"] > float(param("reset_after", 15.0)):
			state["heard"] = 0.0
	_listen[member] = state
	if state["heard"] >= float(param("warn_time", 300.0)) and not _warned.has(member):
		_warned[member] = true
		EventBus.radio_message.emit("Мельников", "%s, уходи от этого дома! Не дослушивай!" % member.display_name)
	if state["heard"] >= float(param("song_length", 360.0)):
		_listen.erase(member)
		violate(member)


func get_debug_text(member: ExpeditionMember) -> String:
	var state: Dictionary = _listen.get(member, {"heard": 0.0})
	return "Колыбельная: слушает %.0f / %.0f с" % [state["heard"], float(param("song_length", 360.0))]
