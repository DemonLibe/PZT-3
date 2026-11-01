import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tscn import *
from level_common import *
from gigadom import *

sc = Scene()
m = section_base(sc, "Section42Puppeteer", "Гигадом, секция 42")
puppet = sc.sub_res("StandardMaterial3D", albedo_color=C(0.42, 0.38, 0.3))
body = sc.sub_res("CapsuleMesh", material=puppet, radius=0.35, height=1.8)
shape = sc.sub_res("CapsuleShape3D", radius=0.35, height=1.8)
sc.node("Doubles", "Node3D", ".")
for i, (x, z) in enumerate(((0.8, 4.0), (-0.8, -6.0), (5.5, -10.0))):
    d = f"Double{i+1}"
    sc.node(d, "StaticBody3D", "Doubles", transform=T(x, 0, z), script=sc.ext_res("Script", "res://anomalies/gigadom/puppeteer/puppet_double.gd"))
    sc.node("Body", "MeshInstance3D", f"Doubles/{d}", transform=T(0, 0.9, 0), mesh=body)
    sc.node("CollisionShape3D", "CollisionShape3D", f"Doubles/{d}", transform=T(0, 0.9, 0), shape=shape)
sc.node("Puppeteer", "MeshInstance3D", ".", transform=T(0, 1.2, -23.0),
        mesh=sc.sub_res("CapsuleMesh", material=sc.sub_res("StandardMaterial3D", albedo_color=C(0.1, 0.1, 0.1)), radius=0.4, height=2.4))
sc.node("PuppeteerZone", "Area3D", ".", script=sc.ext_res("Script", "res://anomalies/gigadom/puppeteer/puppeteer_zone.gd"),
        data=sc.ext_res("Resource", "res://data/puppeteer.tres"), doubles_root=NP("../Doubles"))
zone_shape(sc, "PuppeteerZone", (18, 3.5, 44), (0, 1.75, -2))
for i, (x, z) in enumerate(((-6.5, 10.0), (6.5, 0.0), (-6.5, -10.0))):
    survey(sc, i + 1, (x, 0, z))
ui(sc)
sc.save(ROOT + "/levels/section_42_puppeteer.tscn")
