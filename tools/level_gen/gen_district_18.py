import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District18Photos", "Район 18", beige=True)
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 181)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 182)
photo_mat = material(sc, (0.75, 0.7, 0.6), tex="plaster_warm", scale=4.0)
frame_mesh = sc.sub_res("BoxMesh", material=material(sc, (0.6, 0.45, 0.3), tex="wood_door", scale=3.0), size=V3(0.05, 0.6, 0.5))
photo_mesh = sc.sub_res("QuadMesh", material=photo_mat, size=V2(0.42, 0.52))
sc.node("Photos", "Node3D", ".")
k = 0
for front, facing, zs in ((left, 1, (-7.0, -4.0, 4.0, 7.0)), (right, -1, (-7.0, -4.0, 4.0, 7.0))):
    for z in zs:
        k += 1
        p = f"Photo{k}"
        yaw = 90 if facing > 0 else -90
        sc.node(p, "Node3D", "Photos", transform=T(front + facing * 0.05, 1.6, z, yaw=yaw))
        sc.node("Frame", "MeshInstance3D", f"Photos/{p}", transform=T(0, 0, -0.02, yaw=90), mesh=frame_mesh)
        sc.node("Picture", "MeshInstance3D", f"Photos/{p}", transform=T(0, 0, 0.01), mesh=photo_mesh)
        sc.node("Caption", "Label3D", f"Photos/{p}", transform=T(0, -0.42, 0.02), text="Семья, 1987", font_size=20,
                pixel_size=0.004, modulate=C(0.85, 0.82, 0.75))
sc.node("PhotosZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/photos/photos_zone.gd"),
        data=sc.ext_res("Resource", "res://data/photos.tres"), photos_root=NP("../Photos"))
zone_shape(sc, "PhotosZone", (18, 6, 44), (0, 3, 0))
survey(sc, 1, (-6.0, 0.1, -10.0))
survey(sc, 2, (6.0, 0.1, 9.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_18_photos.tscn")
