extends Node
## Кто управляет логикой мира. SOLO — одиночная игра, HOST — хост по сети,
## CLIENT — подключённый игрок (логику мира не считает, только показывает).

signal session_failed(reason: String)

enum Mode { SOLO, HOST, CLIENT }

const DEFAULT_PORT: int = 24565
const MAX_CLIENTS: int = 3

var mode: Mode = Mode.SOLO
## Причина последнего сбоя сети — для меню.
var last_error: String = ""

var _pending_mode: Mode = Mode.SOLO
var _pending_address: String = "127.0.0.1"


func _ready() -> void:
	multiplayer.connection_failed.connect(_on_connection_failed)
	multiplayer.server_disconnected.connect(_on_server_disconnected)
	print("[NetAuthority] готов, режим: ", Mode.keys()[mode])


## true — этот экземпляр игры вправе менять состояние мира.
func is_authority() -> bool:
	return mode != Mode.CLIENT


func is_networked() -> bool:
	return mode != Mode.SOLO


## Запомнить, как запустить сессию. Сама сессия стартует, когда загрузится уровень.
func prepare(new_mode: Mode, address: String = "127.0.0.1") -> void:
	_pending_mode = new_mode
	_pending_address = address


## Вызывается уровнем в _ready: создаёт сетевое соединение по подготовленному режиму.
func begin_session() -> void:
	if _pending_mode == mode and mode != Mode.SOLO and multiplayer.multiplayer_peer is ENetMultiplayerPeer:
		return  # сессия уже идёт (смена уровня в сети)
	match _pending_mode:
		Mode.SOLO:
			_set_peer(OfflineMultiplayerPeer.new(), Mode.SOLO)
		Mode.HOST:
			var peer: ENetMultiplayerPeer = ENetMultiplayerPeer.new()
			var err: Error = peer.create_server(DEFAULT_PORT, MAX_CLIENTS)
			if err != OK:
				_fail("Не удалось открыть порт %d (ошибка %d)" % [DEFAULT_PORT, err])
				return
			_set_peer(peer, Mode.HOST)
		Mode.CLIENT:
			var peer: ENetMultiplayerPeer = ENetMultiplayerPeer.new()
			var err: Error = peer.create_client(_pending_address, DEFAULT_PORT)
			if err != OK:
				_fail("Не удалось подключиться к %s (ошибка %d)" % [_pending_address, err])
				return
			_set_peer(peer, Mode.CLIENT)
	print("[NetAuthority] сессия: ", Mode.keys()[mode])


## Закрыть соединение и вернуться в одиночный режим.
func end_session() -> void:
	_pending_mode = Mode.SOLO
	_set_peer(OfflineMultiplayerPeer.new(), Mode.SOLO)


func _set_peer(peer: MultiplayerPeer, new_mode: Mode) -> void:
	if multiplayer.multiplayer_peer and not multiplayer.multiplayer_peer is OfflineMultiplayerPeer:
		multiplayer.multiplayer_peer.close()
	multiplayer.multiplayer_peer = peer
	mode = new_mode


func _fail(reason: String) -> void:
	push_warning("[NetAuthority] " + reason)
	last_error = reason
	end_session()
	session_failed.emit(reason)


func _on_connection_failed() -> void:
	_fail("Хост не отвечает")


func _on_server_disconnected() -> void:
	_fail("Хост отключился")
