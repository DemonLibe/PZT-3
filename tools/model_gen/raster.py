"""Программный рендер .glb с текстурами (z-буфер, nearest, аффинные UV как на PS1) — для превью."""
import io, json, os, struct, sys
import numpy as np
from PIL import Image, ImageDraw

def load_glb(path):
    data = open(path, "rb").read()
    jlen = struct.unpack_from("<I", data, 12)[0]
    gj = json.loads(data[20:20 + jlen]); binary = data[20 + jlen + 8:]
    def view(i):
        bv = gj["bufferViews"][i]; o = bv.get("byteOffset", 0); return binary[o:o + bv["byteLength"]]
    def acc(i):
        a = gj["accessors"][i]; bv = gj["bufferViews"][a["bufferView"]]
        comp = {5126: "f4", 5123: "u2", 5125: "u4", 5121: "u1"}[a["componentType"]]
        n = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[a["type"]]
        st = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
        arr = np.frombuffer(binary, dtype=np.dtype(comp), count=a["count"] * n, offset=st)
        return arr.reshape(-1, n) if n > 1 else arr
    imgs = [np.asarray(Image.open(io.BytesIO(view(im["bufferView"]))).convert("RGB")) / 255.0 for im in gj.get("images", [])]
    parts = []
    for node in gj["nodes"]:
        if "mesh" not in node or "colonly" in node.get("name", ""): continue
        t = np.array(node.get("translation", [0, 0, 0]))
        for prim in gj["meshes"][node["mesh"]]["primitives"]:
            pos = acc(prim["attributes"]["POSITION"]) + t
            uv = acc(prim["attributes"]["TEXCOORD_0"]) if "TEXCOORD_0" in prim["attributes"] else np.zeros((len(pos), 2))
            idx = acc(prim["indices"]).reshape(-1, 3)
            m = gj["materials"][prim.get("material", 0)]; pbr = m.get("pbrMetallicRoughness", {})
            col = np.array(pbr.get("baseColorFactor", [1, 1, 1, 1])[:3])
            em = np.array(m.get("emissiveFactor", [0, 0, 0]))
            tex = None
            if "baseColorTexture" in pbr:
                tex = imgs[gj["textures"][pbr["baseColorTexture"]["index"]]["source"]]
            elif em.max() > 0: col = em
            else: col = col ** (1 / 2.2)
            parts.append((pos[idx][:, :, [0, 2, 1]] * np.array([1, -1, 1]), uv[idx], col, tex, em.max() > 0))
    return parts

def render(parts, size=260, elev=20, azim=-55):
    e, a = np.radians(elev), np.radians(azim)
    fwd = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
    right = np.cross([0, 0, 1], fwd); right /= np.linalg.norm(right); up = np.cross(fwd, right)
    P = np.concatenate([p[0].reshape(-1, 3) for p in parts]); c = (P.min(0) + P.max(0)) / 2
    r = max(np.abs((P - c) @ right).max(), np.abs((P - c) @ up).max()) * 1.06 + 1e-6
    img = np.zeros((size, size, 3)) + np.array([21, 22, 26]) / 255; zb = np.full((size, size), -1e9)
    L = np.array([-0.4, -0.7, 0.6]); L /= np.linalg.norm(L)
    for tris, uvs, col, tex, emis in parts:
        q = tris - c
        px = ((q @ right) / r * 0.5 + 0.5) * (size - 1); py = (0.5 - (q @ up) / r * 0.5) * (size - 1); pz = q @ fwd
        n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-9
        shade = np.ones(len(tris)) if emis else 0.4 + 0.6 * np.abs(n @ L)
        for i in range(len(tris)):
            x0, x1 = int(max(px[i].min(), 0)), int(min(px[i].max() + 1, size))
            y0, y1 = int(max(py[i].min(), 0)), int(min(py[i].max() + 1, size))
            if x1 <= x0 or y1 <= y0: continue
            X, Y = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
            (ax, bx, cx), (ay, by, cy) = px[i], py[i]
            d = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
            if abs(d) < 1e-9: continue
            w0 = ((by - cy) * (X - cx) + (cx - bx) * (Y - cy)) / d; w1 = ((cy - ay) * (X - cx) + (ax - cx) * (Y - cy)) / d; w2 = 1 - w0 - w1
            m = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
            z = w0 * pz[i, 0] + w1 * pz[i, 1] + w2 * pz[i, 2]
            sub = zb[y0:y1, x0:x1]; upd = m & (z > sub)
            if not upd.any(): continue
            sub[upd] = z[upd]
            if tex is not None:
                u = w0 * uvs[i, 0, 0] + w1 * uvs[i, 1, 0] + w2 * uvs[i, 2, 0]
                v = w0 * uvs[i, 0, 1] + w1 * uvs[i, 1, 1] + w2 * uvs[i, 2, 1]
                th, tw = tex.shape[:2]
                tx = (np.floor(u[upd] * tw).astype(int)) % tw; ty = (np.floor(v[upd] * th).astype(int)) % th
                cc = tex[ty, tx] * col
            else:
                cc = col
            img[y0:y1, x0:x1][upd] = np.clip(cc * shade[i], 0, 1)
    return Image.fromarray((img * 255).astype(np.uint8))

def sheet(root, cat, out, names=None, S=260):
    man = [m for m in json.load(open(os.path.join(root, "manifest.json"))) if m["category"] == cat and (not names or m["name"] in names)]
    n = 6; rows = (len(man) + n - 1) // n
    W = Image.new("RGB", (n * S, rows * (S + 18)), (21, 22, 26)); d = ImageDraw.Draw(W)
    for i, m in enumerate(man):
        im = render(load_glb(os.path.join(root, m["file"])), S); x, y = (i % n) * S, (i // n) * (S + 18)
        W.paste(im, (x, y + 18)); d.text((x + 6, y + 3), f'{m["name"]}  {m["triangles"]}t', fill=(230, 225, 210))
    W.save(out)

if __name__ == "__main__":
    sheet(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:] or None)
