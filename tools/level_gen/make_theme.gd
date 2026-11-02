extends SceneTree
## Собирает тему интерфейса res://ui/theme.tres. Запуск: godot --headless --path . -s tools/level_gen/make_theme.gd

const BG := Color(0.055, 0.06, 0.065, 0.94)
const BG_HOVER := Color(0.1, 0.11, 0.11, 0.97)
const BG_PRESSED := Color(0.13, 0.12, 0.09, 1.0)
const BORDER := Color(0.32, 0.36, 0.32, 1.0)
const ACCENT := Color(0.86, 0.62, 0.3, 1.0)
const TEXT := Color(0.87, 0.85, 0.79, 1.0)
const TEXT_DIM := Color(0.55, 0.54, 0.5, 1.0)


func box(bg: Color, border: Color, left: int = 1, radius: int = 3) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = bg
	s.border_color = border
	s.set_border_width_all(1)
	s.border_width_left = left
	s.set_corner_radius_all(radius)
	s.content_margin_left = 16
	s.content_margin_right = 16
	s.content_margin_top = 9
	s.content_margin_bottom = 9
	return s


func _initialize() -> void:
	var t := Theme.new()
	t.default_font_size = 18
	for c in ["Button", "OptionButton", "CheckBox", "MenuButton"]:
		t.set_stylebox("normal", c, box(BG, BORDER))
		t.set_stylebox("hover", c, box(BG_HOVER, ACCENT, 4))
		t.set_stylebox("pressed", c, box(BG_PRESSED, ACCENT, 4))
		t.set_stylebox("focus", c, box(Color(0, 0, 0, 0), ACCENT, 4))
		t.set_stylebox("disabled", c, box(Color(0.04, 0.04, 0.045, 0.8), Color(0.18, 0.18, 0.18)))
		t.set_color("font_color", c, TEXT)
		t.set_color("font_hover_color", c, Color(1, 0.95, 0.85))
		t.set_color("font_pressed_color", c, ACCENT)
		t.set_color("font_focus_color", c, Color(1, 0.95, 0.85))
		t.set_color("font_disabled_color", c, Color(0.35, 0.35, 0.33))
	var cb_empty := StyleBoxEmpty.new()
	for st in ["normal", "hover", "pressed", "focus"]:
		t.set_stylebox(st, "CheckBox", cb_empty)
	var panel := box(BG, BORDER, 1, 4)
	panel.content_margin_left = 22
	panel.content_margin_right = 22
	panel.content_margin_top = 18
	panel.content_margin_bottom = 18
	t.set_stylebox("panel", "PanelContainer", panel)
	t.set_stylebox("panel", "Panel", panel)
	t.set_color("font_color", "Label", TEXT)
	var list := box(Color(0.04, 0.045, 0.05, 0.9), BORDER)
	t.set_stylebox("panel", "ItemList", list)
	t.set_stylebox("focus", "ItemList", StyleBoxEmpty.new())
	t.set_stylebox("selected", "ItemList", box(BG_PRESSED, ACCENT, 4))
	t.set_stylebox("selected_focus", "ItemList", box(BG_PRESSED, ACCENT, 4))
	t.set_stylebox("hovered", "ItemList", box(BG_HOVER, BORDER))
	t.set_color("font_color", "ItemList", TEXT)
	t.set_color("font_selected_color", "ItemList", Color(1, 0.95, 0.85))
	t.set_constant("v_separation", "ItemList", 10)
	t.set_stylebox("normal", "RichTextLabel", StyleBoxEmpty.new())
	t.set_color("default_color", "RichTextLabel", TEXT)
	t.set_stylebox("normal", "LineEdit", box(Color(0.03, 0.035, 0.04, 0.95), BORDER))
	t.set_stylebox("focus", "LineEdit", box(Color(0.03, 0.035, 0.04, 0.95), ACCENT, 4))
	t.set_color("font_color", "LineEdit", TEXT)
	var track := StyleBoxFlat.new()
	track.bg_color = Color(0.2, 0.21, 0.2)
	track.content_margin_top = 3
	track.content_margin_bottom = 3
	t.set_stylebox("slider", "HSlider", track)
	var fill := StyleBoxFlat.new()
	fill.bg_color = ACCENT
	fill.content_margin_top = 3
	fill.content_margin_bottom = 3
	t.set_stylebox("grabber_area", "HSlider", fill)
	t.set_stylebox("grabber_area_highlight", "HSlider", fill)
	var popup := box(Color(0.05, 0.055, 0.06, 0.98), BORDER)
	t.set_stylebox("panel", "PopupMenu", popup)
	t.set_stylebox("hover", "PopupMenu", box(BG_PRESSED, ACCENT, 4))
	t.set_color("font_color", "PopupMenu", TEXT)
	t.set_color("font_hover_color", "PopupMenu", Color(1, 0.95, 0.85))
	t.set_stylebox("panel", "TooltipPanel", popup)
	var err := ResourceSaver.save(t, "res://ui/theme.tres")
	print("theme saved: ", err)
	quit()
