import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from moscow import *

sc = Scene()
m, left, right = standard_yard(sc, "District14Mail", "Район 14", beige=True)
lit_windows(sc, m, "GlowWest", left, 1, -15, 15, 141)
lit_windows(sc, m, "GlowEast", right, -1, -15, 15, 142)
box_mat = material(sc, (0.4, 0.5, 0.65), tex="metal_clean", scale=1.5)
box_mesh = sc.sub_res("BoxMesh", material=box_mat, size=V3(0.25, 0.3, 0.45))
box_shape = sc.sub_res("BoxShape3D", size=V3(0.25, 0.3, 0.45))
sc.node("Mailboxes", "Node3D", ".")
k = 0
for front, facing, ez in ((left, 1, -10.5), (left, 1, 1.5), (right, -1, -10.5), (right, -1, 1.5)):
    for row in range(2):
        for col in range(3):
            k += 1
            b = f"Mailbox{k}"
            sc.node(b, "StaticBody3D", "Mailboxes", transform=T(front + facing * 0.13, 1.2 + row * 0.32, ez - 1.6 + col * 0.47),
                    script=sc.ext_res("Script", "res://anomalies/districts/mail/mailbox.gd"))
            sc.node("Mesh", "MeshInstance3D", f"Mailboxes/{b}", mesh=box_mesh)
            sc.node("CollisionShape3D", "CollisionShape3D", f"Mailboxes/{b}", shape=box_shape)
sc.node("MailZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/districts/mail/mail_zone.gd"),
        data=sc.ext_res("Resource", "res://data/mail.tres"), mailboxes_root=NP("../Mailboxes"))
zone_shape(sc, "MailZone", (18, 6, 44), (0, 3, 0))
survey(sc, 1, (-6.0, 0.1, -6.0))
survey(sc, 2, (6.0, 0.1, 5.0))
survey(sc, 3, (0.0, 0, -15.5))
ui(sc)
sc.save(ROOT + "/levels/district_14_mail.tscn")
