extends Node
## PS1-вид: обычные материалы при загрузке меняются на «дрожащий» шейдер,
## поверх мира — слой пикселизации и дизеринга. Интерфейс остаётся чётким.

const SURFACE_SHADER: Shader = preload("res://core/render/ps1_surface.gdshader")
const POST_SHADER: Shader = preload("res://core/render/ps1_post.gdshader")
## Слой постобработки: выше мира, ниже HUD (у HUD слои 20+).
const POST_LAYER: int = 5

var enabled: bool = true

var _cache: Dictionary = {}
var _post: CanvasLayer


func _ready() -> void:
	_post = CanvasLayer.new()
	_post.layer = POST_LAYER
	var rect: ColorRect = ColorRect.new()
	rect.set_anchors_preset(Control.PRESET_FULL_RECT)
	rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var material: ShaderMaterial = ShaderMaterial.new()
	material.shader = POST_SHADER
	rect.material = material
	_post.add_child(rect)
	add_child(_post)
	get_tree().node_added.connect(_on_node_added)


func _process(_delta: float) -> void:
	# Пиксели — только поверх 3D-мира; меню остаются чёткими.
	_post.visible = enabled and get_tree().current_scene is Node3D


func set_enabled(value: bool) -> void:
	enabled = value


func _on_node_added(node: Node) -> void:
	if not enabled:
		return
	if node is CSGPrimitive3D:
		node.material = _convert(node.material)
	elif node is MeshInstance3D:
		_convert_mesh(node)


func _convert_mesh(mesh_instance: MeshInstance3D) -> void:
	if mesh_instance.material_override:
		mesh_instance.material_override = _convert(mesh_instance.material_override)
		return
	if mesh_instance.mesh == null:
		return
	for i in mesh_instance.mesh.get_surface_count():
		var source: Material = mesh_instance.get_surface_override_material(i)
		if source == null:
			source = mesh_instance.mesh.surface_get_material(i)
		var converted: Material = _convert(source)
		if converted != source:
			mesh_instance.set_surface_override_material(i, converted)


## Меняем только непрозрачные освещаемые материалы; стекло, свечение и тени не трогаем.
func _convert(source: Material) -> Material:
	var standard: StandardMaterial3D = source as StandardMaterial3D
	if standard == null or standard.transparency != BaseMaterial3D.TRANSPARENCY_DISABLED \
			or standard.shading_mode == BaseMaterial3D.SHADING_MODE_UNSHADED:
		return source
	if not _cache.has(standard):
		var material: ShaderMaterial = ShaderMaterial.new()
		material.shader = SURFACE_SHADER
		material.set_shader_parameter(&"albedo", standard.albedo_color)
		if standard.albedo_texture:
			material.set_shader_parameter(&"albedo_texture", standard.albedo_texture)
			material.set_shader_parameter(&"use_texture", true)
			if standard.uv1_triplanar:
				material.set_shader_parameter(&"use_triplanar", true)
				material.set_shader_parameter(&"triplanar_scale", standard.uv1_scale.x)
		if standard.emission_enabled:
			# Свечение окон и ламп приглушаем, чтобы не уходило в белый пересвет.
			material.set_shader_parameter(&"emission", standard.emission * Color(1.0, 0.88, 0.7))
			material.set_shader_parameter(&"emission_energy", minf(standard.emission_energy_multiplier, 0.45))
		_cache[standard] = material
	return _cache[standard]
