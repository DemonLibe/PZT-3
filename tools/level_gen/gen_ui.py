"""Экраны интерфейса ПЗМ-3. Оформление — общая тема res://ui/theme.tres."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *

FULL = dict(layout_mode=3, anchors_preset=15, anchor_right=1.0, anchor_bottom=1.0, grow_horizontal=2, grow_vertical=2)
FULL1 = dict(layout_mode=1, anchors_preset=15, anchor_right=1.0, anchor_bottom=1.0, grow_horizontal=2, grow_vertical=2)
ACCENT = C(0.86, 0.62, 0.3)
TEXT = C(0.87, 0.85, 0.79)
DIM = C(0.55, 0.54, 0.5)


def screen(name, script, grain=True):
    sc = Scene()
    sc.node(name, "Control", None, script=sc.ext_res("Script", script), **FULL)
    props = dict(color=C(0.03, 0.032, 0.036), mouse_filter=2, **FULL1)
    if grain:
        props["material"] = sc.sub_res("ShaderMaterial", shader=sc.ext_res("Shader", "res://ui/grain.gdshader"))
    sc.node("Background", "ColorRect", ".", **props)
    return sc


def label(sc, name, parent, text, size=18, color=TEXT, unique=False, align=0, **kw):
    props = dict(layout_mode=2, text=text, horizontal_alignment=align)
    props["theme_override_colors/font_color"] = color
    props["theme_override_font_sizes/font_size"] = size
    if unique:
        props = {"unique_name_in_owner": True, **props}
    props.update(kw)
    sc.node(name, "Label", parent, **props)


def button(sc, name, parent, text, size=19, **kw):
    sc.node(name, "Button", parent, unique_name_in_owner=True, layout_mode=2, text=text, alignment=0,
            **{"theme_override_font_sizes/font_size": size}, **kw)


def margin(sc, name, parent, m=48):
    sc.node(name, "MarginContainer", parent, **FULL1, **{f"theme_override_constants/margin_{s}": m for s in ("left", "top", "right", "bottom")})


def vbox(sc, name, parent, sep=12, **kw):
    sc.node(name, "VBoxContainer", parent, layout_mode=2, **{"theme_override_constants/separation": sep}, **kw)


def hbox(sc, name, parent, sep=12, **kw):
    sc.node(name, "HBoxContainer", parent, layout_mode=2, **{"theme_override_constants/separation": sep}, **kw)


# ---------- Главное меню ----------
sc = screen("MainMenu", "res://ui/main_menu.gd")
margin(sc, "Margin", ".", 72)
vbox(sc, "Box", "Margin", 14, size_flags_vertical=4, size_flags_horizontal=0, custom_minimum_size=V2(420, 0))
label(sc, "Title", "Margin/Box", "ПЗМ-3", 72, C(0.9, 0.88, 0.82))
label(sc, "Subtitle", "Margin/Box", "Паранормальная зона Москва-3", 20, DIM)
sc.node("Gap", "Control", "Margin/Box", custom_minimum_size=V2(0, 36), layout_mode=2)
button(sc, "StartButton", "Margin/Box", "Продолжить экспедиции", 22)
button(sc, "SettingsButton", "Margin/Box", "Настройки")
button(sc, "QuitButton", "Margin/Box", "Выход")
label(sc, "Footer", ".", "Заключённым разрешено сокращать срок прохождением районов. Закон «Москва-3».", 14, DIM,
      unique=True, anchors_preset=3, anchor_left=1.0, anchor_top=1.0, anchor_right=1.0, anchor_bottom=1.0,
      offset_left=-760.0, offset_top=-48.0, offset_right=-32.0, offset_bottom=-20.0, grow_horizontal=0, grow_vertical=0, align=2)
sc.save(ROOT + "/ui/main_menu.tscn")

# ---------- База: кампания ----------
sc = screen("BaseMenu", "res://ui/base_menu.gd")
margin(sc, "Margin", ".", 40)
vbox(sc, "Root", "Margin", 18)
hbox(sc, "Header", "Margin/Root", 18)
label(sc, "Title", "Margin/Root/Header", "Пункт сбора у периметра", 30, C(0.9, 0.88, 0.82), size_flags_horizontal=3)
label(sc, "Subtitle", "Margin/Root/Header", "", 17, DIM, unique=True, align=2, size_flags_vertical=8)
hbox(sc, "Body", "Margin/Root", 20, size_flags_vertical=3)
vbox(sc, "Left", "Margin/Root/Body", 10, custom_minimum_size=V2(380, 0))
label(sc, "ListTitle", "Margin/Root/Body/Left", "Маршрут экспедиций", 16, DIM)
sc.node("Destinations", "ItemList", "Margin/Root/Body/Left", unique_name_in_owner=True, layout_mode=2, size_flags_vertical=3,
        **{"theme_override_font_sizes/font_size": 18})
sc.node("Card", "PanelContainer", "Margin/Root/Body", layout_mode=2, size_flags_horizontal=3)
vbox(sc, "CardBox", "Margin/Root/Body/Card", 12)
label(sc, "DestTitle", "Margin/Root/Body/Card/CardBox", "", 34, C(0.92, 0.9, 0.84), unique=True)
label(sc, "DestState", "Margin/Root/Body/Card/CardBox", "", 17, ACCENT, unique=True)
sc.node("Info", "RichTextLabel", "Margin/Root/Body/Card/CardBox", unique_name_in_owner=True, layout_mode=2, size_flags_vertical=3,
        **{"theme_override_font_sizes/normal_font_size": 17})
button(sc, "StartButton", "Margin/Root/Body/Card/CardBox", "Выйти в экспедицию", 22)
hbox(sc, "Footer", "Margin/Root", 12)
for n, t in (("EncyclopediaButton", "Энциклопедия"), ("JournalButton", "Журнал последней экспедиции"), ("SettingsButton", "Настройки"),
             ("NetButton", "Отладка сети"), ("BackButton", "Главное меню")):
    button(sc, n, "Margin/Root/Footer", t, 17)
sc.save(ROOT + "/ui/base_menu.tscn")

# ---------- Энциклопедия ----------
sc = screen("EncyclopediaView", "res://ui/encyclopedia_view.gd")
margin(sc, "Margin", ".", 40)
vbox(sc, "Root", "Margin", 16)
label(sc, "Title", "Margin/Root", "Энциклопедия аномалий", 30, C(0.9, 0.88, 0.82))
label(sc, "Hint", "Margin/Root", "Расшифровано по записям экспедиций. Статья открывается частично при наблюдении и полностью — после нарушения правила.", 15, DIM, autowrap_mode=2)
hbox(sc, "Body", "Margin/Root", 20, size_flags_vertical=3)
sc.node("Articles", "ItemList", "Margin/Root/Body", unique_name_in_owner=True, custom_minimum_size=V2(380, 0), layout_mode=2)
sc.node("Card", "PanelContainer", "Margin/Root/Body", layout_mode=2, size_flags_horizontal=3)
sc.node("Text", "RichTextLabel", "Margin/Root/Body/Card", unique_name_in_owner=True, layout_mode=2,
        **{"theme_override_font_sizes/normal_font_size": 18})
button(sc, "BackButton", "Margin/Root", "Назад", 18, size_flags_horizontal=0)
sc.save(ROOT + "/ui/encyclopedia_view.tscn")

# ---------- Журнал ----------
sc = screen("JournalView", "res://ui/journal.gd")
margin(sc, "Margin", ".", 56)
vbox(sc, "Root", "Margin", 14)
label(sc, "Header", "Margin/Root", "Журнал экспедиции", 30, C(0.9, 0.88, 0.82), unique=True)
label(sc, "Outcome", "Margin/Root", "", 19, ACCENT, unique=True, autowrap_mode=2)
sc.node("Card", "PanelContainer", "Margin/Root", layout_mode=2, size_flags_vertical=3)
sc.node("Text", "RichTextLabel", "Margin/Root/Card", unique_name_in_owner=True, layout_mode=2,
        **{"theme_override_font_sizes/normal_font_size": 17})
button(sc, "BackButton", "Margin/Root", "На базу", 20, size_flags_horizontal=0)
sc.save(ROOT + "/ui/journal.tscn")

# ---------- Панель настроек ----------
sc = Scene()
sc.node("SettingsPanel", "VBoxContainer", None, script=sc.ext_res("Script", "res://ui/settings_panel.gd"),
        custom_minimum_size=V2(460, 0), **{"theme_override_constants/separation": 8})
def slider(name, text, lo, hi, step):
    label(sc, name + "Label", ".", text, 16, DIM)
    sc.node(name, "HSlider", ".", unique_name_in_owner=True, layout_mode=2, min_value=lo, max_value=hi, step=step)
slider("Sensitivity", "Чувствительность мыши", 0.2, 3.0, 0.05)
slider("Brightness", "Яркость", 0.6, 3.0, 0.05)
slider("Master", "Общая громкость", 0.0, 1.0, 0.01)
slider("Ambient", "Фон", 0.0, 1.0, 0.01)
slider("Sfx", "Звуки", 0.0, 1.0, 0.01)
sc.node("Ps1", "CheckBox", ".", unique_name_in_owner=True, layout_mode=2, text="PS1-графика (крупные пиксели)")
sc.node("Fullscreen", "CheckBox", ".", unique_name_in_owner=True, layout_mode=2, text="Полный экран")
sc.save(ROOT + "/ui/settings_panel.tscn")

# ---------- Экран настроек ----------
sc = screen("SettingsMenu", "res://ui/settings_menu.gd")
sc.node("Center", "CenterContainer", ".", **FULL1)
sc.node("Card", "PanelContainer", "Center", layout_mode=2)
vbox(sc, "Box", "Center/Card", 16)
label(sc, "Title", "Center/Card/Box", "Настройки", 28)
sc.node("SettingsPanel", None, "Center/Card/Box", instance=sc.ext_res("PackedScene", "res://ui/settings_panel.tscn"))
button(sc, "BackButton", "Center/Card/Box", "Назад")
sc.save(ROOT + "/ui/settings_menu.tscn")

# ---------- Пауза ----------
sc = Scene()
sc.node("PauseMenu", "CanvasLayer", None, layer=60, script=sc.ext_res("Script", "res://ui/pause_menu.gd"))
sc.node("Dim", "ColorRect", ".", color=C(0, 0, 0, 0.72), **FULL1)
sc.node("Center", "CenterContainer", ".", **FULL1)
sc.node("Card", "PanelContainer", "Center", layout_mode=2)
vbox(sc, "Box", "Center/Card", 12, custom_minimum_size=V2(480, 0))
label(sc, "Title", "Center/Card/Box", "Пауза", 30)
label(sc, "Controls", "Center/Card/Box",
      "WASD — идти · Shift — бег · Ctrl — присед · E — действие · F — фонарь\nZ — лечь/встать · Q — оружие · V — сказать вслух · G — огонь · R — ответить по рации",
      14, DIM, autowrap_mode=2)
button(sc, "ResumeButton", "Center/Card/Box", "Продолжить")
button(sc, "SettingsToggle", "Center/Card/Box", "Настройки")
sc.node("SettingsPanel", None, "Center/Card/Box", instance=sc.ext_res("PackedScene", "res://ui/settings_panel.tscn"), visible=False)
button(sc, "AbortButton", "Center/Card/Box", "Прервать вылазку")
sc.save(ROOT + "/ui/pause_menu.tscn")

# ---------- HUD ----------
sc = Scene()
sc.node("HUD", "CanvasLayer", None, layer=20, script=sc.ext_res("Script", "res://ui/hud.gd"))
sc.node("ObjectivePanel", "PanelContainer", ".", unique_name_in_owner=True, offset_left=20.0, offset_top=20.0,
        offset_right=340.0, offset_bottom=120.0, mouse_filter=2)
hbox(sc, "Row", "ObjectivePanel", 14)
sc.node("Arrow", "Control", "ObjectivePanel/Row", unique_name_in_owner=True, custom_minimum_size=V2(48, 48), layout_mode=2,
        size_flags_vertical=4, script=sc.ext_res("Script", "res://ui/compass_arrow.gd"))
vbox(sc, "Text", "ObjectivePanel/Row", 2)
label(sc, "Location", "ObjectivePanel/Row/Text", "", 14, DIM, unique=True)
label(sc, "Objective", "ObjectivePanel/Row/Text", "", 18, TEXT, unique=True)
label(sc, "Distance", "ObjectivePanel/Row/Text", "", 15, ACCENT, unique=True)
sc.node("Progress", "ProgressBar", "ObjectivePanel/Row/Text", unique_name_in_owner=True, visible=False, layout_mode=2,
        custom_minimum_size=V2(200, 8), show_percentage=False)
sc.node("Crosshair", "ColorRect", ".", anchors_preset=8, anchor_left=0.5, anchor_top=0.5, anchor_right=0.5, anchor_bottom=0.5,
        offset_left=-2.0, offset_top=-2.0, offset_right=2.0, offset_bottom=2.0, mouse_filter=2, color=C(0.9, 0.86, 0.75, 0.7))
sc.node("PromptPanel", "PanelContainer", ".", unique_name_in_owner=True, visible=False, anchors_preset=7, anchor_left=0.5,
        anchor_top=1.0, anchor_right=0.5, anchor_bottom=1.0, offset_left=-220.0, offset_top=-180.0, offset_right=220.0,
        offset_bottom=-130.0, grow_horizontal=2, grow_vertical=0, mouse_filter=2)
label(sc, "Prompt", "PromptPanel", "", 18, TEXT, unique=True, align=1)
sc.node("ToastPanel", "PanelContainer", ".", unique_name_in_owner=True, visible=False, anchors_preset=5, anchor_left=0.5,
        anchor_right=0.5, offset_left=-330.0, offset_top=130.0, offset_right=330.0, offset_bottom=180.0, grow_horizontal=2,
        mouse_filter=2)
label(sc, "Toast", "ToastPanel", "", 18, ACCENT, unique=True, align=1, autowrap_mode=2)
label(sc, "Help", ".", "Esc — пауза и управление", 13, DIM, anchors_preset=3, anchor_left=1.0, anchor_top=1.0, anchor_right=1.0,
      anchor_bottom=1.0, offset_left=-260.0, offset_top=-34.0, offset_right=-16.0, offset_bottom=-12.0, align=2)
sc.save(ROOT + "/ui/hud.tscn")
print("ok")
