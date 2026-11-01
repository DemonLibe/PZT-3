extends TestHarness
## Район 18 «Фотографии»: снимки меняются от визита к визиту.

func _ready() -> void:
	Encyclopedia.reset()
	var level := await load_level("res://levels/district_18_photos.tscn", 2)
	await wait(1.5)
	var caption: Label3D = level.get_node("Photos/Photo1/Caption")
	check(Encyclopedia.visits_of(&"photos") == 1 and caption.text == "Семья, 1987", "первый визит — чужая семья")
	level.queue_free()
	await frames(3)
	level = await load_level("res://levels/district_18_photos.tscn", 2)
	await wait(1.5)
	caption = level.get_node("Photos/Photo1/Caption")
	var caption2: Label3D = level.get_node("Photos/Photo2/Caption")
	check(caption.text.begins_with("На снимке:") and caption2.text == "Семья, 1987", "второй визит — одно лицо сменилось: " + caption.text)
	finish()
