"""Синтез звуков ПЗТ-3 (только стандартная библиотека)."""
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

import math, random, struct, wave
SR = 22050
OUT = ROOT + "/audio/sfx/"
random.seed(7)

def save(name, samples):
    peak = max(1e-9, max(abs(s) for s in samples))
    k = 0.9 / peak if peak > 0.9 else 1.0
    with wave.open(OUT + name, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, s * k)) * 32767)) for s in samples))

def lowpass(x, a):
    y, out = 0.0, []
    for s in x:
        y += a * (s - y); out.append(y)
    return out

def noise(n): return [random.uniform(-1, 1) for _ in range(n)]

def env(n, attack, decay):
    return [min(1.0, i / max(1, attack * SR)) * math.exp(-i / (decay * SR)) for i in range(n)]

def footstep():
    n = int(0.22 * SR)
    x = lowpass(noise(n), 0.08)
    thump = [math.sin(2 * math.pi * 70 * i / SR) * 0.6 for i in range(n)]
    e = env(n, 0.004, 0.045)
    return [(a * 2.2 + b) * c for a, b, c in zip(x, thump, e)]

def heartbeat():
    n = int(0.7 * SR); out = [0.0] * n
    for start, amp in ((0.0, 1.0), (0.22, 0.7)):
        s0 = int(start * SR)
        for i in range(int(0.16 * SR)):
            t = i / SR
            out[s0 + i] += amp * math.sin(2 * math.pi * (55 - 60 * t) * t) * math.exp(-t / 0.05)
    return out

def count_tick():
    n = int(0.15 * SR)
    e = env(n, 0.001, 0.025)
    return [(math.sin(2 * math.pi * 420 * i / SR) * 0.5 + math.sin(2 * math.pi * 860 * i / SR) * 0.2) * e[i]
            + lowpass(noise(1), 0.3)[0] * 0.05 * e[i] for i in range(n)]

def lullaby():
    # Тихий напев в миноре, без слов
    notes = [69, 72, 76, 74, 72, 71, 69, 0, 69, 72, 71, 67, 69, 0, 0, 0]
    beat = 0.55; out = []
    for m in notes:
        n = int(beat * SR)
        f = 440 * 2 ** ((m - 69) / 12) if m else 0
        for i in range(n):
            t = i / SR
            vib = 1 + 0.004 * math.sin(2 * math.pi * 5 * t)
            a = math.sin(2 * math.pi * f * vib * t) + 0.3 * math.sin(4 * math.pi * f * t) if f else 0
            out.append(a * 0.35 * min(1, t / 0.08) * math.exp(-t / 0.9))
    return lowpass(out, 0.25)

def ambient(base, buzz, seconds=10.0, wind=0.25):
    n = int(seconds * SR)
    w = lowpass(noise(n), 0.01)
    out = []
    for i in range(n):
        t = i / SR
        lfo = 0.6 + 0.4 * math.sin(2 * math.pi * t / seconds)  # целое число периодов — шов без щелчка
        s = 0.25 * math.sin(2 * math.pi * base * t) + 0.12 * math.sin(2 * math.pi * base * 2.01 * t)
        if buzz: s += 0.05 * math.sin(2 * math.pi * buzz * t) * (0.8 + 0.2 * math.sin(2 * math.pi * 0.3 * t))
        out.append(s * lfo + w[i] * wind * 4)
    fade = int(0.05 * SR)
    for i in range(fade):  # мягкий шов петли
        k = i / fade
        out[i] *= k; out[-1 - i] *= k
    return out

def light_off():
    n = int(0.25 * SR)
    click = env(n, 0.0005, 0.01)
    return [click[i] * random.uniform(-1, 1) * 0.8 + 0.15 * math.sin(2 * math.pi * 100 * i / SR) * math.exp(-i / (0.08 * SR)) for i in range(n)]

def door():
    n = int(0.45 * SR)
    x = lowpass(noise(n), 0.05); e = env(n, 0.003, 0.12)
    return [(x[i] * 2 + 0.5 * math.sin(2 * math.pi * 90 * i / SR)) * e[i] for i in range(n)]

def vanish():
    n = int(2.2 * SR); out = []
    for i in range(n):
        t = i / SR
        a = math.sin(math.pi * t / 2.2)
        out.append(a * (0.4 * math.sin(2 * math.pi * (40 + 8 * t) * t) + 0.25 * math.sin(2 * math.pi * 61.7 * t)))
    w = lowpass(noise(n), 0.02)
    return [o + w[i] * 1.5 * math.sin(math.pi * i / n) for i, o in enumerate(out)]

def heavy_step():
    n = int(0.35 * SR)
    x = lowpass(noise(n), 0.03); e = env(n, 0.01, 0.09)
    return [(x[i] * 3 + 0.8 * math.sin(2 * math.pi * 45 * i / SR)) * e[i] for i in range(n)]

save("footstep.wav", footstep())
save("heartbeat.wav", heartbeat())
save("count_tick.wav", count_tick())
save("lullaby.wav", lullaby())
save("ambient_district.wav", ambient(55, 0, wind=0.35))
save("ambient_gigadom.wav", ambient(48, 100, wind=0.12))
save("light_off.wav", light_off())
save("door.wav", door())
save("vanish.wav", vanish())
save("heavy_step.wav", heavy_step())
