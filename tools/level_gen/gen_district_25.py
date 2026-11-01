import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District25Ceiling", "Район 25", room=(6.0, 6.0), entrances_left=(-10.5, -1.5))
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 251)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 252)
apartment(sc, wall_tex="plaster_grey", lamp_energy=0.7)
stain = sc.sub_res("StandardMaterial3D", shading_mode=0, albedo_color=C(0.18, 0.04, 0.03))
for i, (dx, dz, s) in enumerate(((-0.8, -1.2, 1.4), (1.1, 0.6, 0.9), (-1.6, 1.5, 0.7), (0.4, -0.2, 0.5))):
    sc.node(f"Stain{i+1}", "MeshInstance3D", ".", transform=T(-11.4 + dx, 2.84, 6.0 + dz, pitch=90),
            mesh=sc.sub_res("QuadMesh", material=stain, size=V2(s, s * 0.8)))
sc.node("CeilingZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/ceiling/ceiling_zone.gd"),
        data=sc.ext_res("Resource", "res://data/ceiling.tres"))
zone_shape(sc, "CeilingZone", (5.8, 2.8, 5.8), (-11.4, 1.45, 6.0))
survey(sc, 1, (-13.2, 0.11, 4.0))
survey(sc, 2, (6.0, 0.1, -8.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_25_ceiling.tscn")
