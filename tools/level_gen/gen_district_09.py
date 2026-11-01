import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District09Smile", "Район 9", beige=True)
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 91, count=8)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 92, count=8)
face_mat = sc.sub_res("StandardMaterial3D", shading_mode=0,
                      albedo_texture=sc.ext_res("Texture2D", "res://world/textures/smile_face.png"), texture_filter=0)
face_quad = sc.sub_res("QuadMesh", material=face_mat, size=V2(0.9, 0.9))
photo_quad = sc.sub_res("QuadMesh", material=face_mat, size=V2(0.3, 0.3))
board = material(sc, (0.7, 0.65, 0.55), tex="wood_door", scale=2.0)
sc.node("Faces", "Node3D", ".")
k = 0
for front, facing, slots in ((left, 1, ((-7.5, 1), (4.5, 2), (13.5, 0))), (right, -1, ((-13.5, 0), (-4.5, 3), (7.5, 1)))):
    for wz, fl in slots:
        k += 1
        x, y, z, yaw = window_slot(front, facing, wz, floor=fl)
        sc.node(f"WindowFace{k}", "MeshInstance3D", "Faces", transform=T(x + facing * 0.01, y, z, yaw=yaw), mesh=face_quad,
                script=sc.ext_res("Script", "res://anomalies/districts/smile/smile_face.gd"))
# Доска объявлений с фотографиями у подъезда
box(sc, "Board", (left + 0.12, 1.5, -4.0), (0.08, 1.0, 1.4), board, collision=False)
for i, dz in enumerate((-0.4, 0.0, 0.4)):
    sc.node(f"Photo{i+1}", "MeshInstance3D", "Faces", transform=T(left + 0.17, 1.55, -4.0 + dz, yaw=90), mesh=photo_quad,
            script=sc.ext_res("Script", "res://anomalies/districts/smile/smile_face.gd"))
sc.node("SmileZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/smile/smile_zone.gd"),
        data=sc.ext_res("Resource", "res://data/smile.tres"))
zone_shape(sc, "SmileZone", (18, 8, 44), (0, 4, 0))
survey(sc, 1, (-6.0, 0.1, -1.5))
survey(sc, 2, (6.0, 0.1, -9.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_09_smile.tscn")
