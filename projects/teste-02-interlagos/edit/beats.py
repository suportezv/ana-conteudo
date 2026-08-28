"""Detecta tempo e grade de batidas da trilha via fluxo de energia + autocorrelação."""
import subprocess, numpy as np

SR = 22050
raw = subprocess.run(
    ["ffmpeg", "-v", "error", "-i", "trilha_full.wav", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
    capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32)

hop, win = 512, 1024
n = (len(x) - win) // hop
frames = np.lib.stride_tricks.as_strided(x, (n, win), (x.strides[0] * hop, x.strides[0]))
energy = (frames ** 2).mean(axis=1)
flux = np.maximum(0, np.diff(energy, prepend=energy[0]))
flux = flux / (flux.max() + 1e-9)
t_frame = hop / SR

# tempo por autocorrelação do fluxo (60 a 180 BPM)
ac = np.correlate(flux, flux, "full")[len(flux) - 1:]
lags = np.arange(len(ac)) * t_frame
mask = (lags >= 60 / 180) & (lags <= 60 / 60)
best_lag = lags[mask][np.argmax(ac[mask])]
bpm = 60 / best_lag
period = best_lag

# fase: desloca a grade para casar com os picos de fluxo
phases = np.arange(0, period, t_frame / 2)
scores = []
for ph in phases:
    grid = np.arange(ph, len(flux) * t_frame, period)
    idx = np.clip((grid / t_frame).astype(int), 0, len(flux) - 1)
    scores.append(flux[idx].sum())
phase = phases[int(np.argmax(scores))]
beats = np.arange(phase, len(flux) * t_frame, period)

# onsets fortes (para impactos): picos de fluxo acima de percentil 97
thr = np.percentile(flux, 97)
peaks = [i for i in range(1, len(flux) - 1) if flux[i] > thr and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1]]
onsets, last = [], -1
for i in peaks:
    t = i * t_frame
    if t - last > 0.25:
        onsets.append(round(t, 3)); last = t

print(f"BPM: {bpm:.1f}  periodo: {period:.3f}s  fase: {phase:.3f}s")
print("beats:", " ".join(f"{b:.2f}" for b in beats[:64]))
print("onsets fortes:", onsets[:40])
