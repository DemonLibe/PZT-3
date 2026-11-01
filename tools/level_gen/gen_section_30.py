import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section30Threshold", "Гигадом, секция 30")
# Начало: панельная стена двора без шва переходит в бетон
box(sc, "PanelSeam", (0, 2, 19.95), (4, 4, 0.1), material(sc, (1, 1, 1), tex="facade_panel", scale=1.0 / 3.0), collision=False)
observe_zone(sc, "threshold")
for i, (x, z) in enumerate(((-6.5, 10.0), (6.5, -10.0), (0.0, -20.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_30_threshold.tscn")
