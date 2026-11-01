extends Node
## Открытые статьи Энциклопедии. Заглушка: сохранение — на этапе 9.

const SAVE_PATH: String = "user://encyclopedia.json"

## id аномалии -> степень открытия статьи
var opened_articles: Dictionary = {}


func _ready() -> void:
	print("[Encyclopedia] готов, статей открыто: ", opened_articles.size())
