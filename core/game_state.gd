extends Node
## Текущая экспедиция и общий генератор случайных чисел.
## Вся случайность в игре — только через GameState.rng.

## Сколько игровых часов проходит за одну реальную секунду.
@export var hours_per_second: float = 1.0 / 60.0

var rng: RandomNumberGenerator = RandomNumberGenerator.new()
var expedition_seed: int = 0
## Игровое время экспедиции в часах.
var game_hours: float = 0.0


func _ready() -> void:
	start_expedition(0)
	print("[GameState] готов, сид экспедиции: ", expedition_seed)


func _process(delta: float) -> void:
	if NetAuthority.is_authority():
		game_hours += delta * hours_per_second


## Отладка: промотать игровое время.
func debug_skip_hours(hours: float) -> void:
	if NetAuthority.is_authority():
		game_hours += hours


## Начать новую экспедицию. seed_value = 0 — взять случайный сид.
func start_expedition(seed_value: int) -> void:
	if seed_value == 0:
		rng.randomize()
		seed_value = rng.randi()
	expedition_seed = seed_value
	rng.seed = expedition_seed
	game_hours = 0.0
