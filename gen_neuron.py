import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch
import numpy as np

BG    = '#0d1b2a'
PANEL = '#111f30'
CYAN  = '#22d3ee'
CYAN2 = '#67e8f9'
WHITE = '#e2e8f0'
GRAY  = '#94a3b8'
RED   = '#f87171'
DARK  = '#1e3a5f'

fig = plt.figure(figsize=(16, 7), facecolor=BG)
ax_bio = fig.add_axes([0.01, 0.04, 0.46, 0.90])
ax_art = fig.add_axes([0.50, 0.04, 0.49, 0.90])

for ax in [ax_bio, ax_art]:
    ax.set_facecolor(PANEL)
    ax.axis('off')

# ── BIOLOGICAL NEURON ─────────────────────────────────────────────────────────
ax = ax_bio
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Soma
sx, sy = 5.8, 5.0
ax.add_patch(Ellipse((sx, sy), 2.0, 1.6,
                     facecolor=DARK, edgecolor=CYAN, lw=2.5, zorder=4))
ax.text(sx, sy + 0.12, 'Cell body', color=WHITE, fontsize=8.5, ha='center',
        va='center', fontweight='bold', zorder=6)
ax.text(sx, sy - 0.32, '(soma)', color=GRAY, fontsize=7.5, ha='center',
        va='center', zorder=6)

# Recursive branching dendrites
def draw_branch(ax, x0, y0, angle, length, depth, lw):
    x1 = x0 + length * np.cos(angle)
    y1 = y0 + length * np.sin(angle)
    ax.plot([x0, x1], [y0, y1], color=CYAN2, lw=lw,
            solid_capstyle='round', zorder=3)
    if depth == 0:
        ax.add_patch(Circle((x1, y1), 0.13, color=CYAN2, alpha=0.85, zorder=6))
    else:
        spread = np.radians(30)
        draw_branch(ax, x1, y1, angle - spread, length * 0.62, depth - 1, lw * 0.72)
        draw_branch(ax, x1, y1, angle + spread, length * 0.62, depth - 1, lw * 0.72)

# Three primary trunks from left side of soma
for (ox, oy, angle) in [
    (-0.72, +0.55, np.radians(135)),
    (-0.95, +0.05, np.radians(175)),
    (-0.72, -0.55, np.radians(222)),
]:
    draw_branch(ax, sx + ox, sy + oy, angle, 1.18, depth=2, lw=2.2)

# Labels
ax.text(0.5, 9.0, 'Dendrites\n(inputs)', color=GRAY, fontsize=9,
        ha='left', va='top', linespacing=1.3)

ax.annotate('Synaptic\nweights $w_i$',
            xy=(3.3, 5.1), xytext=(1.3, 2.9),
            color=GRAY, fontsize=8.5, ha='center',
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.0,
                            connectionstyle='arc3,rad=-0.25'))

# Axon
ax.annotate('', xy=(9.3, sy), xytext=(sx + 1.0, sy),
            arrowprops=dict(arrowstyle='-', color=CYAN, lw=2.2), zorder=3)
ax.text(7.4, sy + 0.38, 'Axon', color=GRAY, fontsize=9, ha='center')

# Synaptic terminal boutons
for ty in [6.5, 5.0, 3.5]:
    ax.plot([9.3, 9.52], [sy, ty], color=CYAN, lw=1.8,
            solid_capstyle='round', zorder=3)
    ax.add_patch(Circle((9.52, ty), 0.22,
                        facecolor=DARK, edgecolor=CYAN2, lw=2, zorder=5))

ax.text(9.78, sy, 'Synaptic\nterminals\n(output)', color=GRAY, fontsize=8,
        ha='left', va='center', linespacing=1.3)

ax.text(sx, 1.1, r'fires when  $\sum w_i x_i \geq \theta$',
        color=CYAN, fontsize=10, ha='center', style='italic')

ax.set_title('Biological neuron', color=WHITE, fontsize=13,
             fontweight='bold', pad=6)

# ── ARTIFICIAL NEURON ─────────────────────────────────────────────────────────
ax = ax_art
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

sig_x, sig_y = 4.8, 5.0

for (lbl, ix, iy), wl in zip(
        [('x₃', 1.1, 7.8), ('x₂', 1.1, 5.0), ('x₁', 1.1, 2.2)],
        ['w₃', 'w₂', 'w₁']):
    ax.add_patch(Ellipse((ix, iy), 1.3, 1.1,
                         facecolor=DARK, edgecolor=CYAN2, lw=2, zorder=4))
    ax.text(ix, iy, lbl, color=WHITE, fontsize=11, ha='center', va='center',
            fontweight='bold', zorder=5)
    ax.annotate('', xy=(sig_x - 0.90, sig_y + (iy - sig_y) * 0.13),
                xytext=(ix + 0.65, iy),
                arrowprops=dict(arrowstyle='->', color=CYAN, lw=1.8,
                                mutation_scale=12), zorder=3)
    ax.text((ix + sig_x) / 2 - 0.2, (iy + sig_y) / 2 + 0.05,
            wl, color=GRAY, fontsize=9, ha='center', va='center')

ax.text(1.1, 1.0, 'Binary\ninputs', color=GRAY, fontsize=8.5, ha='center')

ax.add_patch(Ellipse((sig_x, sig_y), 1.8, 1.6,
                     facecolor=DARK, edgecolor=CYAN, lw=2.5, zorder=4))
ax.text(sig_x, sig_y, 'Σ', color=CYAN, fontsize=20, ha='center', va='center',
        fontweight='bold', zorder=5)
ax.text(sig_x, sig_y - 1.35, r'$\Sigma\,w_i x_i$', color=GRAY,
        fontsize=9, ha='center')

ax.annotate('', xy=(7.1, sig_y), xytext=(sig_x + 0.90, sig_y),
            arrowprops=dict(arrowstyle='->', color=CYAN, lw=1.8,
                            mutation_scale=12), zorder=3)

ax.add_patch(FancyBboxPatch((7.1, sig_y - 0.75), 1.60, 1.50,
                            boxstyle='round,pad=0.10',
                            facecolor='#2d1515', edgecolor=RED, lw=2.5, zorder=4))
ax.text(7.90, sig_y + 0.08, 'f(·)', color=RED, fontsize=11.5,
        ha='center', va='center', fontweight='bold', zorder=5)
ax.text(7.90, sig_y - 0.35, '≥ θ ?', color=RED, fontsize=9,
        ha='center', va='center', zorder=5)
ax.text(7.90, sig_y - 1.35, 'Threshold θ', color=RED, fontsize=8.5, ha='center')

ax.annotate('', xy=(9.25, sig_y), xytext=(8.70, sig_y),
            arrowprops=dict(arrowstyle='->', color=CYAN, lw=1.8,
                            mutation_scale=12), zorder=3)

ax.add_patch(Circle((9.55, sig_y), 0.55,
                    facecolor=DARK, edgecolor=CYAN2, lw=2, zorder=4))
ax.text(9.55, sig_y, 'y', color=CYAN2, fontsize=13, ha='center', va='center',
        fontweight='bold', zorder=5)
ax.text(9.55, sig_y - 1.1, '0 or 1', color=GRAY, fontsize=8.5, ha='center')
ax.text(9.55, sig_y - 1.55, 'Binary\noutput', color=GRAY, fontsize=8, ha='center')

ax.set_title('McCulloch–Pitts artificial neuron (1943)',
             color=WHITE, fontsize=13, fontweight='bold', pad=6)

plt.savefig('assets/mcculloch_pitts_neuron.png',
            dpi=150, bbox_inches='tight', facecolor=BG, edgecolor='none')
plt.close()
print("Saved.")
