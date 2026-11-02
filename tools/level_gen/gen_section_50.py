import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section50Threshold", "Гигадом, секция 50", north_maze=False)
food = sc.ext_res("PackedScene", "res://world/food_item.tscn")
sc.node("Food1", None, ".", instance=food, transform=T(-6.0, 0, 0.0))
sc.node("Threshold", "Area3D", ".", transform=T(0, 1.5, -24.0))
zone_shape(sc, "Threshold", (4, 3, 1.5))
sc.node("NothingZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/nothing/nothing_zone.gd"),
        data=sc.ext_res("Resource", "res://data/threshold2.tres"), threshold=NP("../Threshold"),
        outcome_text="запись о входе в 51-ю секцию. Дальнейших записей нет", completed_title="Гигадом, секция 50")
zone_shape(sc, "NothingZone", (4, 3.5, 44), (0, 1.75, -2))
for i, (x, z) in enumerate(((-6.5, 10.0), (6.5, 0.0), (-6.5, -10.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_50_threshold.tscn")
