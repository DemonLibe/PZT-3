import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District04Laundry", "Район 4", beige=True)
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 41)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 42)
rope = material(sc, (0.85, 0.85, 0.8))
cloths = [material(sc, (1, 1, 1), tex=t, scale=1.5) for t in ("cloth_blue", "cloth_red", "cloth_white", "cloth_plaid")]
item_shape = sc.sub_res("BoxShape3D", size=V3(0.1, 0.9, 0.7))
meshes = [sc.sub_res("BoxMesh", material=c, size=V3(0.03, 0.9, 0.7)) for c in cloths]
sc.node("Laundry", "Node3D", ".")
k = 0
for x in (-3.5, 3.5):
    for zz in (-12.0, 4.0):
        cylinder(sc, f"LinePost{x}{zz}", (x, 1.1, zz), 0.05, 2.2, m.metal)
    box(sc, f"Rope{x}", (x, 2.1, -4.0), (0.02, 0.02, 16.0), rope, collision=False)
    for j, z in enumerate((-10.5, -8.0, -5.5, -3.0, -0.5, 2.0)):
        k += 1
        it = f"Laundry{k}"
        sc.node(it, "StaticBody3D", "Laundry", transform=T(x, 1.62, z),
                script=sc.ext_res("Script", "res://anomalies/districts/laundry/laundry_item.gd"))
        sc.node("Mesh", "MeshInstance3D", f"Laundry/{it}", mesh=meshes[k % 4])
        sc.node("CollisionShape3D", "CollisionShape3D", f"Laundry/{it}", shape=item_shape)
sc.node("LaundryZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/laundry/laundry_zone.gd"),
        data=sc.ext_res("Resource", "res://data/laundry.tres"), laundry_root=NP("../Laundry"))
zone_shape(sc, "LaundryZone", (18, 6, 44), (0, 3, 0))
survey(sc, 1, (0.0, 0, -7.0))
survey(sc, 2, (-6.0, 0.1, 6.0))
survey(sc, 3, (5.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_04_laundry.tscn")
