"""Мини-генератор .tscn для Godot 4."""
import math

def fmt(v):
    if isinstance(v, bool): return "true" if v else "false"
    if isinstance(v, (int,)): return str(v)
    if isinstance(v, float): return repr(round(v, 5))
    if isinstance(v, Raw): return v.s
    if isinstance(v, str): return '"' + v.replace('\\','\\\\').replace('"','\\"') + '"'
    if isinstance(v, (list, tuple)): return "[" + ", ".join(fmt(x) for x in v) + "]"
    if isinstance(v, dict): return "{\n" + ",\n".join(f'"{k}": {fmt(x)}' for k, x in v.items()) + "\n}"
    raise TypeError(v)

class Raw:
    def __init__(self, s): self.s = s

def V3(x, y, z): return Raw(f"Vector3({float(x)}, {float(y)}, {float(z)})")
def V2(x, y): return Raw(f"Vector2({float(x)}, {float(y)})")
def C(r, g, b, a=1.0): return Raw(f"Color({r}, {g}, {b}, {a})")
def NP(p): return Raw(f'NodePath("{p}")')
def SN(s): return Raw(f'&"{s}"')

def T(x=0, y=0, z=0, yaw=0.0, pitch=0.0):
    """Transform3D: поворот yaw (град, вокруг Y), затем pitch (вокруг X)."""
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    # R = Ry * Rx ; столбцы базиса
    xx, xy, xz = cy, 0.0, -sy
    yx, yy, yz = sy*sp, cp, cy*sp
    zx, zy, zz = sy*cp, -sp, cy*cp
    vals = [xx, yx, zx, xy, yy, zy, xz, yz, zz]  # строки матрицы
    # Godot Transform3D(xx, xy, xz, yx, yy, yz, zx, zy, zz, ox, oy, oz) — по столбцам базиса
    cols = [xx, xy, xz, yx, yy, yz, zx, zy, zz]
    return Raw("Transform3D(" + ", ".join(repr(round(c, 5)) for c in vals) + f", {float(x)}, {float(y)}, {float(z)})")

class Scene:
    def __init__(self):
        self.ext = []; self.sub = []; self.nodes = []; self.conns = []
    def ext_res(self, typ, path):
        for i, (t, p, rid) in enumerate(self.ext):
            if p == path: return Raw(f'ExtResource("{rid}")')
        rid = f"{len(self.ext)+1}_r"
        self.ext.append((typ, path, rid))
        return Raw(f'ExtResource("{rid}")')
    def sub_res(self, typ, **props):
        rid = f"{typ}_{len(self.sub)+1}"
        self.sub.append((typ, rid, props))
        return Raw(f'SubResource("{rid}")')
    def node(self, name, typ=None, parent=None, instance=None, groups=None, **props):
        self.nodes.append((name, typ, parent, instance, groups, props))
        return (name if parent in (None, ".") else f"{parent}/{name}") if parent is not None else "."
    def text(self):
        out = ["[gd_scene format=3]", ""]
        for t, p, rid in self.ext:
            out.append(f'[ext_resource type="{t}" path="{p}" id="{rid}"]')
        if self.ext: out.append("")
        for t, rid, props in self.sub:
            out.append(f'[sub_resource type="{t}" id="{rid}"]')
            for k, v in props.items(): out.append(f"{k} = {fmt(v)}")
            out.append("")
        for name, typ, parent, inst, groups, props in self.nodes:
            head = f'[node name="{name}"'
            if typ: head += f' type="{typ}"'
            if parent is not None: head += f' parent="{parent}"'
            nps = [k for k, v in props.items() if isinstance(v, Raw) and v.s.startswith("NodePath(") and k != "root_path" and not k.startswith("properties/")]
            if nps: head += ' node_paths=PackedStringArray(' + ", ".join(f'"{k}"' for k in nps) + ')'
            if inst: head += f" instance={inst.s}"
            if groups: head += " groups=[" + ", ".join(f'"{g}"' for g in groups) + "]"
            out.append(head + "]")
            for k, v in props.items(): out.append(f"{k} = {fmt(v)}")
            out.append("")
        for c in self.conns: out.append(c)
        return "\n".join(out).rstrip() + "\n"
    def save(self, path):
        open(path, "w").write(self.text())
