import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch
import numpy as np

BG    = '#0d1b2a'
CYAN  = '#22d3ee'
CYAN2 = '#67e8f9'
WHITE = '#e2e8f0'
GRAY  = '#94a3b8'
RED   = '#f87171'
DARK  = '#1e3a5f'

bio_img = mpimg.imread('assets/biological_neuron1.png')
H, W = bio_img.shape[:2]   # 720 × 1280

# ── Figure 1: annotated biological neuron ────────────────────────────────────
fig1, ax = plt.subplots(figsize=(10, 5.8), facecolor=BG)
ax.set_facecolor(BG)
ax.axis('off')
ax.imshow(bio_img, zorder=1, aspect='auto')

PAD_T = 125
PAD_B = 145
ax.set_xlim(-20, W + 20)
ax.set_ylim(H + PAD_B, -PAD_T)

def ann(ax_, label, lx, ly, px, py, rad=0.0):
    ax_.annotate(
        label,
        xy=(px, py), xytext=(lx, ly),
        color=WHITE, fontsize=10.5, ha='center', va='center',
        fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.28', facecolor=BG,
                  edgecolor=CYAN, alpha=0.93, lw=1.4),
        arrowprops=dict(arrowstyle='->', color=CYAN, lw=1.5,
                        mutation_scale=11,
                        connectionstyle=f'arc3,rad={rad}'),
        zorder=5
    )

# anatomy approx positions (1280×720, y=0 top):
#   dendrites/inputs  ~(160, 340)
#   soma (pink)       ~(470, 330)
#   axon midpoint     ~(820, 380)
#   terminals         ~(1150, 330)
#   synaptic weights  ~(300, 480)
ann(ax, 'Dendrites\n(inputs)',            160,  -68,  160,  340, rad= 0.0)
ann(ax, 'Cell body\n(soma)',              475,  -68,  475,  330, rad= 0.0)
ann(ax, 'Synaptic\nterminals\n(output)', 1150,  -80, 1150,  330, rad= 0.0)
ann(ax, 'Axon',                           820, H+82,  820,  390, rad= 0.0)
ann(ax, 'Synaptic\nweights  $w_i$',       320, H+82,  300,  480, rad=-0.15)

ax.text(W / 2, H + PAD_B - 16,
        r'fires when  $\sum w_i x_i \geq \theta$',
        color=CYAN, fontsize=11, ha='center', va='bottom', style='italic')

ax.set_title('Biological neuron', color=WHITE, fontsize=12,
             fontweight='bold', pad=4)

fig1.savefig('assets/bio_neuron_annotated.png',
             dpi=150, bbox_inches='tight', facecolor=BG, edgecolor='none')
plt.close(fig1)
print("Saved bio_neuron_annotated.png")

# ── Figure 2: McCulloch–Pitts artificial neuron ──────────────────────────────
fig2, ax = plt.subplots(figsize=(10, 4.2), facecolor=BG)
ax.set_facecolor(BG)
ax.axis('off')
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
             color=WHITE, fontsize=12, fontweight='bold', pad=6)

fig2.savefig('assets/mp_artificial_neuron.png',
             dpi=150, bbox_inches='tight', facecolor=BG, edgecolor='none')
plt.close(fig2)
print("Saved mp_artificial_neuron.png")
