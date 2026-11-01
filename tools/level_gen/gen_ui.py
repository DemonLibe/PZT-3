import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tscn import *

FULL = dict(layout_mode=3, anchors_preset=15, anchor_right=1.0, anchor_bottom=1.0, grow_horizontal=2, grow_vertical=2)
FULL1 = dict(layout_mode=1, anchors_preset=15, anchor_right=1.0, anchor_bottom=1.0, grow_horizontal=2, grow_vertical=2)
TEXT = C(0.78, 0.75, 0.68)
DIM = C(0.5, 0.48, 0.43)

def screen(name, script):
    sc = Scene()
    sc.node(name, "Control", None, script=sc.ext_res("Script", script), **FULL)
    sc.node("Background", "ColorRect", ".", color=C(0.035, 0.035, 0.04), mouse_filter=2, **FULL1)
    return sc

def label(sc, name, parent, text, size=16, color=TEXT, unique=False, align=1, **kw):
    props = dict(layout_mode=2, text=text, horizontal_alignment=align)
    props["theme_override_colors/font_color"] = color
    props["theme_override_font_sizes/font_size"] = size
    if unique: props = {"unique_name_in_owner": True, **props}
    props.update(kw)
    sc.node(name, "Label", parent, **props)

def button(sc, name, parent, text):
    sc.node(name, "Button", parent, unique_name_in_owner=True, layout_mode=2, text=text,
            **{"theme_override_font_sizes/font_size": 17})

# База
sc = screen("BaseMenu", "res://ui/base_menu.gd")
sc.node("Center", "CenterContainer", ".", **FULL1)
sc.node("Box", "VBoxContainer", "Center", custom_minimum_size=V2(380, 0), layout_mode=2,
        **{"theme_override_constants/separation": 10})
label(sc, "Title", "Center/Box", "ПЗТ-3", 40)
label(sc, "Subtitle", "Center/Box", "База экспедиции", 16, DIM, unique=True)
sc.node("Gap", "Control", "Center/Box", custom_minimum_size=V2(0, 16), layout_mode=2)
sc.node("Destination", "OptionButton", "Center/Box", unique_name_in_owner=True, layout_mode=2)
button(sc, "StartButton", "Center/Box", "Выйти в экспедицию")
button(sc, "EncyclopediaButton", "Center/Box", "Энциклопедия")
button(sc, "JournalButton", "Center/Box", "Журнал последней экспедиции")
button(sc, "SettingsButton", "Center/Box", "Настройки")
button(sc, "NetButton", "Center/Box", "Отладка сети")
button(sc, "QuitButton", "Center/Box", "Выход")
sc.save(ROOT + "/ui/base_menu.tscn")

# Энциклопедия
sc = screen("EncyclopediaView", "res://ui/encyclopedia_view.gd")
sc.node("Margin", "MarginContainer", ".", **FULL1, **{"theme_override_constants/margin_left": 40,
        "theme_override_constants/margin_top": 30, "theme_override_constants/margin_right": 40, "theme_override_constants/margin_bottom": 30})
sc.node("Box", "VBoxContainer", "Margin", layout_mode=2, **{"theme_override_constants/separation": 12})
label(sc, "Title", "Margin/Box", "Энциклопедия экспедиций", 26, align=0)
sc.node("Split", "HSplitContainer", "Margin/Box", layout_mode=2, size_flags_vertical=3, split_offset=40)
sc.node("Articles", "ItemList", "Margin/Box/Split", unique_name_in_owner=True, custom_minimum_size=V2(300, 0), layout_mode=2,
        **{"theme_override_font_sizes/font_size": 16})
sc.node("Text", "RichTextLabel", "Margin/Box/Split", unique_name_in_owner=True, layout_mode=2, size_flags_horizontal=3,
        **{"theme_override_colors/default_color": TEXT, "theme_override_font_sizes/normal_font_size": 17})
button(sc, "BackButton", "Margin/Box", "Назад")
sc.save(ROOT + "/ui/encyclopedia_view.tscn")

# Журнал
sc = screen("JournalView", "res://ui/journal.gd")
sc.node("Margin", "MarginContainer", ".", **FULL1, **{"theme_override_constants/margin_left": 60,
        "theme_override_constants/margin_top": 30, "theme_override_constants/margin_right": 60, "theme_override_constants/margin_bottom": 30})
sc.node("Box", "VBoxContainer", "Margin", layout_mode=2, **{"theme_override_constants/separation": 12})
label(sc, "Header", "Margin/Box", "Журнал экспедиции", 26, unique=True, align=0)
sc.node("Text", "RichTextLabel", "Margin/Box", unique_name_in_owner=True, layout_mode=2, size_flags_vertical=3,
        **{"theme_override_colors/default_color": TEXT, "theme_override_font_sizes/normal_font_size": 17})
button(sc, "BackButton", "Margin/Box", "На базу")
sc.save(ROOT + "/ui/journal.tscn")

def settings_panel_nodes(sc, parent):
    """Панель настроек как вложенная сцена-экземпляр."""
    sc.node("SettingsPanel", None, parent, instance=sc.ext_res("PackedScene", "res://ui/settings_panel.tscn"))

# Панель настроек (отдельная сцена, переиспользуется)
sc = Scene()
sc.node("SettingsPanel", "VBoxContainer", None, script=sc.ext_res("Script", "res://ui/settings_panel.gd"),
        custom_minimum_size=V2(420, 0), **{"theme_override_constants/separation": 8})
def slider(name, text, lo, hi, step):
    label(sc, name + "Label", ".", text, 15, DIM, align=0)
    sc.node(name, "HSlider", ".", unique_name_in_owner=True, layout_mode=2, min_value=lo, max_value=hi, step=step)
slider("Sensitivity", "Чувствительность мыши", 0.2, 3.0, 0.05)
slider("Master", "Общая громкость", 0.0, 1.0, 0.01)
slider("Ambient", "Фон", 0.0, 1.0, 0.01)
slider("Sfx", "Звуки", 0.0, 1.0, 0.01)
sc.node("Ps1", "CheckBox", ".", unique_name_in_owner=True, layout_mode=2, text="PS1-графика")
sc.node("Fullscreen", "CheckBox", ".", unique_name_in_owner=True, layout_mode=2, text="Полный экран")
sc.save(ROOT + "/ui/settings_panel.tscn")

# Экран настроек
sc = screen("SettingsMenu", "res://ui/settings_menu.gd")
sc.node("Center", "CenterContainer", ".", **FULL1)
sc.node("Box", "VBoxContainer", "Center", layout_mode=2, **{"theme_override_constants/separation": 14})
label(sc, "Title", "Center/Box", "Настройки", 28)
settings_panel_nodes(sc, "Center/Box")
button(sc, "BackButton", "Center/Box", "Назад")
sc.save(ROOT + "/ui/settings_menu.tscn")

# Главное меню
sc = screen("MainMenu", "res://ui/main_menu.gd")
sc.node("Center", "CenterContainer", ".", **FULL1)
sc.node("Box", "VBoxContainer", "Center", custom_minimum_size=V2(360, 0), layout_mode=2,
        **{"theme_override_constants/separation": 12})
label(sc, "Title", "Center/Box", "ПЗТ-3", 52)
label(sc, "Subtitle", "Center/Box", "Экспедиция в аномальную зону Токио-3", 16, DIM)
sc.node("Gap", "Control", "Center/Box", custom_minimum_size=V2(0, 24), layout_mode=2)
button(sc, "StartButton", "Center/Box", "Начать")
button(sc, "SettingsButton", "Center/Box", "Настройки")
button(sc, "QuitButton", "Center/Box", "Выход")
sc.save(ROOT + "/ui/main_menu.tscn")

# Пауза
sc = Scene()
sc.node("PauseMenu", "CanvasLayer", None, layer=60, script=sc.ext_res("Script", "res://ui/pause_menu.gd"))
sc.node("Dim", "ColorRect", ".", color=C(0, 0, 0, 0.7), **FULL1)
sc.node("Center", "CenterContainer", ".", **FULL1)
sc.node("Box", "VBoxContainer", "Center", layout_mode=2, **{"theme_override_constants/separation": 12})
label(sc, "Title", "Center/Box", "Пауза", 28)
button(sc, "ResumeButton", "Center/Box", "Продолжить")
settings_panel_nodes(sc, "Center/Box")
button(sc, "AbortButton", "Center/Box", "Прервать вылазку")
sc.save(ROOT + "/ui/pause_menu.tscn")
