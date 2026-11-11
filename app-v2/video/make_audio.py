# Synthesizes the explainer's music bed and sound effects (no samples, no licences needed) -> audio.wav
import numpy as np, wave, os
SR = 44100
DUR = 14.5
N = int(SR * DUR)
rng = np.random.default_rng(3)
mix = np.zeros((N, 2))

def add(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N: return
    sig = sig[: N - i] * gain
    mix[i:i + len(sig), 0] += sig * (1 - max(0, pan))
    mix[i:i + len(sig), 1] += sig * (1 + min(0, pan))

def t(d): return np.arange(int(SR * d)) / SR
def hz(n): return 440 * 2 ** ((n - 69) / 12)
def env(d, a=0.005, r=0.05):
    x = t(d); e = np.minimum(1, x / a) * np.minimum(1, (d - x) / r); return np.clip(e, 0, 1)

def pluck(n, d=0.45):
    x = t(d); f = hz(n)
    w = np.sin(2 * np.pi * f * x) + 0.35 * np.sin(4 * np.pi * f * x) + 0.12 * np.sin(6 * np.pi * f * x)
    return w * np.exp(-x * 7) * env(d, 0.004, 0.03)
def bass(n, d=0.5):
    x = t(d); f = hz(n)
    return (np.sin(2 * np.pi * f * x) + 0.25 * np.sin(4 * np.pi * f * x)) * np.exp(-x * 3.5) * env(d, 0.01, 0.06)
def pad(notes, d):
    x = t(d); w = sum(np.sin(2 * np.pi * hz(n) * x + i) for i, n in enumerate(notes)) / len(notes)
    return w * env(d, 0.25, 0.5)
def hat(d=0.05):
    x = t(d); n = rng.standard_normal(len(x)); n = np.diff(n, prepend=0)  # crude high-pass
    return n * np.exp(-x * 90)
def kick(d=0.22):
    x = t(d); f = 110 * np.exp(-x * 26) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 14)
def pop(n, d=0.16):
    x = t(d); f = hz(n) * (1 + 0.6 * np.exp(-x * 60))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 28)
def whoosh(d=0.45, up=True):
    x = t(d); n = rng.standard_normal(len(x))
    k = np.linspace(0.02, 0.5, len(x)) if up else np.linspace(0.5, 0.02, len(x))
    y = np.zeros(len(x)); acc = 0.0
    for i in range(len(x)): acc += k[i] * (n[i] - acc); y[i] = acc
    return y * np.sin(np.pi * x / d) ** 2
def whistle(d):
    x = t(d); trem = 0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 38 * x))
    w = np.sin(2 * np.pi * 2750 * x + 0.9 * np.sin(2 * np.pi * 38 * x)) + 0.5 * np.sin(2 * np.pi * 3350 * x)
    air = rng.standard_normal(len(x)) * 0.08
    return (w * trem + air) * env(d, 0.008, 0.04)
def coin():
    a = t(0.09); b = t(0.5)
    one = np.sin(2 * np.pi * 1318.5 * a) * env(0.09, 0.002, 0.02)
    two = (np.sin(2 * np.pi * 1975.5 * b) + 0.4 * np.sin(2 * np.pi * 3951 * b)) * np.exp(-b * 9)
    return np.concatenate([one, two])
def brass(n, d):
    x = t(d); f = hz(n); w = sum(np.sin(2 * np.pi * f * k * x) / k for k in range(1, 7))
    return w * env(d, 0.02, 0.08) * (0.8 + 0.2 * np.sin(2 * np.pi * 5.5 * x))

# ---- music: 120 bpm, 2s bars. A minor for the "problem", C major once Subi arrives ----
BARS = [(0, [57, 60, 64], 45), (2, [53, 57, 60], 41), (4, [60, 64, 67], 48), (6, [55, 59, 62], 43), (8, [53, 57, 60], 41), (9, [55, 59, 62], 43), (10, [60, 64, 67], 48), (12, [60, 64, 67], 48)]
ENDS = [2, 4, 6, 8, 9, 10, 12, 14.5]
for (start, ch, b), end in zip(BARS, ENDS):
    d = end - start
    add(pad([n - 12 for n in ch], d + 0.3), start, 0.10)
    steps = int(round(d / 0.25))
    arp = [ch[0], ch[1], ch[2], ch[1] + 12, ch[2], ch[1], ch[0] + 12, ch[2]]
    for s in range(steps):
        at = start + s * 0.25
        if at < 3.2 and s % 2: continue          # sparser while the bills pile up
        if at >= 13.5: break
        add(pluck(arp[s % 8] + 12), at, 0.16, pan=(-0.3 if s % 2 else 0.3))
    for s in range(int(round(d / 0.5))):
        at = start + s * 0.5
        if at >= 13.5: break
        add(bass(b - 12 if s % 2 == 0 else b - 5), at, 0.26)
        if at >= 3.2:
            add(kick(), at, 0.30)
            add(hat(), at + 0.25, 0.05)
add(pad([72, 76, 79, 84], 2.4), 12.0, 0.10)

# ---- sound effects, on the animation's beats ----
for i in range(6): add(pop(62 + i * 2), 0.3 + i * 0.3 + 0.2, 0.45, pan=(-0.4, 0, 0.4)[i % 3])
add(brass(50, 0.22), 2.3, 0.10); add(brass(46, 0.4), 2.52, 0.10)          # "ouch" sting on the yearly total
for cut in (3.2, 6.2, 10.0): add(whoosh(), cut - 0.12, 0.55)
add(whistle(0.16), 3.85, 0.22); add(whistle(0.42), 4.06, 0.22)             # coach whistle
add(pop(79), 4.35, 0.3)
for i in range(3): add(whoosh(0.25), 6.8 + i * 0.3, 0.25)
for i, c in enumerate((7.9, 8.6, 9.3)): add(coin(), c, 0.30, pan=(-0.2, 0, 0.2)[i])
for i, n in enumerate((60, 64, 67, 72)): add(brass(n, 0.14 if i < 3 else 0.5), 10.15 + i * 0.13, 0.11)   # fanfare
for i in range(3): add(pop(72 + i * 2), 10.35 + i * 0.2, 0.35, pan=(-0.4, 0, 0.4)[i])
add(coin(), 10.7, 0.22); add(brass(72, 0.7), 10.7, 0.07); add(brass(76, 0.7), 10.7, 0.05); add(brass(79, 0.7), 10.7, 0.05)
add(coin(), 13.38, 0.26)

fade = int(SR * 0.7); mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
mix = np.tanh(mix * 1.15)
mix *= 0.85 / np.abs(mix).max()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio.wav")
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype("<i2").tobytes())
print("wrote", out)
