"""Genera assets/mapa_decision.png (one-pager ejecutivo, §1.2).

Árbol de decisión basado en la jerarquía de palancas (Tabla 10.3): primero la
información disponible (historia y covariables ex-ante), después la naturaleza
de la decisión (puntual o de riesgo).
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY = "#0D1B2E"
TEAL = "#0E7490"
ORANGE = "#B45309"
GRAY = "#475569"
MUTED = "#64748B"

fig, ax = plt.subplots(figsize=(9.6, 6.9), dpi=200)
fig.patch.set_facecolor("white")
ax.set_xlim(0, 12)
ax.set_ylim(-0.4, 11.0)
ax.axis("off")

DEC = dict(boxstyle="round,pad=0.55", fc=NAVY, ec="none")
REC = dict(boxstyle="round,pad=0.55", fc=TEAL, ec="none")
RSK = dict(boxstyle="round,pad=0.55", fc=ORANGE, ec="none")
PLN = dict(boxstyle="round,pad=0.55", fc=GRAY, ec="none")

boxes = [
    ((3.2, 10.0), "¿Historia del target\nde la entidad?", DEC),
    ((9.5, 10.0), "Perfil hora × día\n(baseline transparente)", REC),
    ((3.2, 7.4), "¿Covariables disponibles\nex-ante (no oracle)?", DEC),
    ((9.5, 7.4), "LightGBM con lags\ny embargo temporal", REC),
    ((3.2, 4.9), "LightGBM con\ncovariables legítimas", REC),
    ((6.35, 2.4), "¿La decisión gestiona\nriesgo o stock?", DEC),
    ((3.2, 0.4), "Añadir cuantiles\n(P10–P90, cobertura)", RSK),
    ((9.5, 0.4), "Pronóstico puntual\n(MAE/MASE) basta", PLN),
]

arrows = [
    ((3.2, 10.0), (9.5, 10.0), "NO"),
    ((3.2, 10.0), (3.2, 7.4), "SÍ"),
    ((3.2, 7.4), (9.5, 7.4), "NO"),
    ((3.2, 7.4), (3.2, 4.9), "SÍ"),
    ((9.5, 7.4), (6.35, 2.4), None),
    ((3.2, 4.9), (6.35, 2.4), None),
    ((6.35, 2.4), (3.2, 0.4), "SÍ"),
    ((6.35, 2.4), (9.5, 0.4), "NO"),
]

for src, dst, lab in arrows:
    ax.annotate(
        "",
        xy=dst,
        xytext=src,
        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1, shrinkA=2, shrinkB=2),
        zorder=1,
    )
    if lab:
        mx, my = (src[0] + dst[0]) / 2, (src[1] + dst[1]) / 2
        ax.text(mx + 0.15, my, lab, color=MUTED, fontsize=8.5, weight="bold",
                ha="left", va="center", zorder=3)

for (x, y), text, style in boxes:
    ax.text(x, y, text, fontsize=9.4, color="white", ha="center", va="center",
            bbox=style, zorder=2)

ax.text(6.35, 5.9, "sobre el modelo elegido", color=MUTED, fontsize=8, style="italic",
        ha="center", va="center")

fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mapa_decision.png")
fig.savefig(out, facecolor="white")
print("escrito:", out)
