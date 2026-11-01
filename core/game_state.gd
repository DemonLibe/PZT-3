extends Node
## Текущая экспедиция и общий генератор случайных чисел.
## Вся случайность в игре — только через GameState.rng.

var rng: RandomNumberGenerator = RandomNumberGenerator.new()
var expedition_seed: int = 0


func _ready() -> void:
	start_expedition(0)
	print("[GameState] готов, сид экспедиции: ", expedition_seed)


## Начать новую экспедицию. seed_value = 0 — взять случайный сид.
func start_expedition(seed_value: int) -> void:
	if seed_value == 0:
		rng.randomize()
		seed_value = rng.randi()
	expedition_seed = seed_value
	rng.seed = expedition_seed
