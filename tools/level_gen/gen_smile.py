"""Текстура «Улыбки»: бледное лицо, улыбка шире анатомической нормы."""
import os
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
N = 128
img = Image.new("RGB", (N, N), (14, 14, 18))
d = ImageDraw.Draw(img)
d.ellipse([28, 10, 100, 118], fill=(196, 188, 176))
d.ellipse([44, 44, 58, 52], fill=(20, 18, 18))
d.ellipse([70, 44, 84, 52], fill=(20, 18, 18))
d.chord([20, 52, 108, 104], 10, 170, fill=(60, 18, 18))
for x in range(26, 104, 7):
    d.rectangle([x, 74, x + 4, 80], fill=(222, 216, 200))
d.arc([20, 52, 108, 104], 10, 170, fill=(90, 30, 30), width=2)
img = img.filter(ImageFilter.GaussianBlur(0.6))
img.save(os.path.join(ROOT, "world", "textures", "smile_face.png"))
print("ok")
