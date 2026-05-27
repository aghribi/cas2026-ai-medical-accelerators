import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
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

bio_img = mpimg.imread('assets/biological_neuron1.png')
H, W = bio_img.shape[:2]   # 720 × 1280

fig = plt.figure(figsize=(16, 7.0), facecolor=BG)
ax_bio = fig.add_axes([0.01, 0.04, 0.47, 0.92])
ax_art = fig.add_axes([0.51, 0.04, 0.48, 0.92])

for ax in [ax_bio, ax_art]:
    ax.set_facecolor(BG)
    ax.axis('off')

# ── LEFT: annotated biological neuron photo ───────────────────────────────────
ax = ax_bio
ax.imshow(bio_img, zorder=1, aspect='auto')

# expand axis so labels can float above/below the image
PAD_T = 140   # pixels above
PAD_B = 150   # pixels below
ax.set_xlim(-20, W + 20)
ax.set_ylim(H + PAD_B, -PAD_T)   # y inverted: row 0 = top

def ann(label, lx, ly, ax_, ay_, rad=0.0, below=False):
    """lx,ly  = label centre (px, may be outside image bounds)
       ax_,ay_ = arrow target (px, inside image)"""
    ax.annotate(
        label,
        xy=(ax_, ay_), xytext=(lx, ly),
        color=WHITE, fontsize=8.5, ha='center', va='center',
        fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.28', facecolor=BG,
                  edgecolor=CYAN, alpha=0.92, lw=1.3),
        arrowprops=dict(
            arrowstyle='->', color=CYAN, lw=1.4, mutation_scale=10,
            connectionstyle=f'arc3,rad={rad}'
        ),
        zorder=5
    )

# Anatomy positions (1280×720 image, y=0 top):
#   Dendrites/inputs:  x≈160, y≈360
#   Soma (pink):       x≈470, y≈340
#   Axon midpoint:     x≈820, y≈370
#   Terminals:         x≈1150, y≈330
#   Synaptic weights:  between inputs and soma, x≈320, y≈480

# Labels ABOVE image (ly < 0)
ann('Dendrites\n(inputs)',         160,  -70,   160,  340, rad= 0.0)
ann('Cell body\n(soma)',           475,  -70,   475,  330, rad= 0.0)
ann('Synaptic\nterminals\n(output)', 1150, -80,  1150, 330, rad= 0.0)

# Labels BELOW image (ly > H)
ann('Axon',                        820,  H+80,  820,  390, rad= 0.0)
ann('Synaptic\nweights $w_i$',     320,  H+80,  300,  480, rad=-0.15)

# Firing rule caption below labels
ax.text(W / 2, H + PAD_B - 18,
        r'fires when  $\sum w_i x_i \geq \theta$',
        color=CYAN, fontsize=10, ha='center', va='bottom', style='italic')

ax.set_title('Biological neuron', color=WHITE, fontsize=13,
             fontweight='bold', pad=4)

# ── RIGHT: McCulloch–Pitts artificial neuron ──────────────────────────────────
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
