"""Genera assets/fundamento_distribucion.png (figura de la subsección §1.2).

Esquema conceptual, no datos reales: historial observado hasta el corte t,
abanico de cuantiles anidados P25-P75 dentro de P10-P90, esperanza condicional
como resumen puntual y densidad predictiva al borde del horizonte.
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

NAVY = "#0D1B2E"
TEAL = "#0E7490"
CRIMSON = "#A61E2B"
GRAY = "#475569"
MUTED = "#64748B"

rng = np.random.default_rng(42)


def signal(x):
    return 1.0 + 0.9 * np.sin(2 * np.pi * x / 24.0) + 0.010 * x


t = np.linspace(-60.0, 60.0, 481)
cut = 0.0

hist = t <= cut
y_hist = signal(t) + rng.normal(0.0, 0.16, t.size)

y_center = signal(t)
h = np.clip(t - cut, 0.0, None)
sd = 0.16 + 0.028 * h

q10, q90 = y_center - 1.2816 * sd, y_center + 1.2816 * sd
q25, q75 = y_center - 0.6745 * sd, y_center + 0.6745 * sd

fig, ax = plt.subplots(figsize=(9.2, 4.2), dpi=200)
fig.patch.set_facecolor("white")

fut = t >= cut

ax.fill_between(t[fut], q10[fut], q90[fut], color=TEAL, alpha=0.15, lw=0)
ax.fill_between(t[fut], q25[fut], q75[fut], color=TEAL, alpha=0.28, lw=0)
ax.plot(t[fut], q10[fut], color=TEAL, lw=0.6, alpha=0.75)
ax.plot(t[fut], q90[fut], color=TEAL, lw=0.6, alpha=0.75)

ax.plot(t, y_center, color=NAVY, lw=1.9, zorder=5)
ax.plot(t[hist], y_hist[hist], color=GRAY, lw=0.9, marker="o", ms=1.4, zorder=4)

ax.axvline(cut, color=CRIMSON, lw=1.0, ls="--", zorder=6)

ymin, ymax = float((q10 - 0.35).min()), float((q90 + 0.35).max())
ax.set_ylim(ymin, ymax)
ax.set_xlim(-60, 60)

ax.text(cut + 1.0, ymax - 0.18, "hoy (t)", color=CRIMSON, fontsize=9, va="top")
ax.text(-58, ymax - 0.18, "historial observado", color=MUTED, fontsize=9.5, va="top")
ax.text(58, ymax - 0.18, "horizonte de pronóstico (t+h)", color=TEAL,
        fontsize=9.5, va="top", ha="right")
ax.text(2.0, q90[-1] + 0.06, "P10–P90", color=TEAL, fontsize=8.5)
ax.text(2.0, q75[-1] + 0.05, "P25–P75", color=TEAL, fontsize=8.5)
ax.text(-58, y_center[0] - 0.30, "esperanza condicional", color=NAVY, fontsize=9)

ax.set_yticks([])
ax.set_xticks([])
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color("#d8dde3")
ax.set_xlabel("tiempo", color=MUTED, fontsize=9.5)

inset = ax.inset_axes([0.83, 0.16, 0.15, 0.66])
mu = float(signal(60.0))
sd_h = float(sd[-1])
yg = np.linspace(mu - 3.1 * sd_h, mu + 3.1 * sd_h, 240)
dens = np.exp(-0.5 * ((yg - mu) / sd_h) ** 2)
inset.fill_betweenx(yg, 0.0, dens, color=TEAL, alpha=0.22, lw=0)
inset.plot(dens, yg, color=TEAL, lw=1.0)
inset.axhline(mu, color=NAVY, lw=1.4)
inset.plot([0.0], [mu], "o", color=NAVY, ms=3.5)
inset.text(0.05, mu + 0.05, "media: caso particular", color=NAVY, fontsize=7.4, va="bottom")
inset.set_xlim(0.0, 1.35)
inset.set_ylim(ymin, ymax)
inset.axis("off")

fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fundamento_distribucion.png")
fig.savefig(out, facecolor="white")
print("escrito:", out)
