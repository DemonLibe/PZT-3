"""Фасад панельной пятиэтажки: одна ячейка 3×3 м (панель с окном), на основе CC0-штукатурки."""
import os
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEX = os.path.join(ROOT, "world", "textures")
N = 128


def facade(name, base_file, tint, glass, lit=False):
    base = Image.open(os.path.join(TEX, base_file)).convert("RGB").resize((N, N))
    arr = np.asarray(base, dtype=float) / 255.0
    gray = arr.mean(axis=2, keepdims=True)
    arr = (gray * 0.6 + arr * 0.4) * np.array(tint)
    img = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    # швы между панелями
    seam = tuple(int(c * 255 * 0.55) for c in tint)
    d.rectangle([0, 0, N - 1, 1], fill=seam)
    d.rectangle([0, 0, 1, N - 1], fill=seam)
    # окно: рама, стекло, переплёт, подоконник
    x0, x1, y0, y1 = int(N * 0.22), int(N * 0.78), int(N * 0.25), int(N * 0.70)
    d.rectangle([x0 - 3, y0 - 3, x1 + 3, y1 + 3], fill=(200, 196, 186))
    d.rectangle([x0, y0, x1, y1], fill=glass)
    mid = (x0 + x1) // 2
    d.rectangle([mid - 1, y0, mid + 1, y1], fill=(190, 186, 176))
    d.rectangle([x0, y0 + (y1 - y0) // 3 - 1, x1, y0 + (y1 - y0) // 3 + 1], fill=(190, 186, 176))
    d.rectangle([x0 - 5, y1 + 3, x1 + 5, y1 + 6], fill=(150, 148, 142))
    if not lit:
        # блик на стекле
        d.line([x0 + 4, y1 - 4, x0 + 14, y0 + 8], fill=tuple(min(255, c + 25) for c in glass), width=2)
    img.save(os.path.join(TEX, name + ".png"))


facade("facade_panel", "plaster_grey.png", (0.95, 0.95, 0.93), (22, 26, 34))
facade("facade_panel_beige", "plaster.png", (1.0, 0.94, 0.85), (22, 26, 34))
print("ok")
