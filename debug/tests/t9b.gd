extends TestHarness
## Отдельный запуск игры: Энциклопедия должна загрузиться с диска.

func _ready() -> void:
	check(Encyclopedia.expedition_count >= 2, "после перезапуска: экспедиций %d" % Encyclopedia.expedition_count)
	check(Encyclopedia.article_level(&"mirror") == 2, "после перезапуска: «Зеркало» открыто")
	check(Encyclopedia.get_article_text(&"mirror").contains("Безопасно при взгляде до 4 секунд"), "текст правила виден")
	check(Encyclopedia.get_article_text(&"cradle").contains("Данные отсутствуют"), "неоткрытая статья скрыта")
	finish()
