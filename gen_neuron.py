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
fig2, ax = plt.subplots(figsize=(11, 4.6), facecolor=BG)
ax.set_facecolor(BG)
ax.axis('off')
ax.set_xlim(0, 11)
ax.set_ylim(0, 10)

sig_x, sig_y = 4.8, 5.0

# Input nodes + weighted arrows
for (lbl, ix, iy), wl in zip(
        [('x₃', 1.0, 7.8), ('x₂', 1.0, 5.0), ('x₁', 1.0, 2.2)],
        ['w₃', 'w₂', 'w₁']):
    ax.add_patch(Ellipse((ix, iy), 1.3, 1.1,
                         facecolor=DARK, edgecolor=CYAN2, lw=2, zorder=4))
    ax.text(ix, iy, lbl, color=WHITE, fontsize=12, ha='center', va='center',
            fontweight='bold', zorder=5)
    ax.annotate('', xy=(sig_x - 0.90, sig_y + (iy - sig_y) * 0.13),
                xytext=(ix + 0.65, iy),
                arrowprops=dict(arrowstyle='->', color=CYAN, lw=1.8,
                                mutation_scale=12), zorder=3)
    # weight label — brighter and larger
    mx = (ix + 0.65 + sig_x - 0.90) / 2 - 0.1
    my = (iy + sig_y + (iy - sig_y) * 0.13) / 2 + 0.12
    ax.text(mx, my, wl, color=CYAN2, fontsize=10.5, ha='center', va='center',
            fontweight='bold')

ax.text(1.0, 0.85, 'Binary inputs', color=GRAY, fontsize=9, ha='center')

# Sigma node
ax.add_patch(Ellipse((sig_x, sig_y), 1.9, 1.7,
                     facecolor=DARK, edgecolor=CYAN, lw=2.5, zorder=4))
ax.text(sig_x, sig_y + 0.08, 'Σ', color=CYAN, fontsize=22, ha='center', va='center',
        fontweight='bold', zorder=5)
ax.text(sig_x, sig_y - 1.45, r'$\Sigma\,w_i x_i$', color=GRAY,
        fontsize=9.5, ha='center')

# Arrow sigma → threshold
ax.annotate('', xy=(6.85, sig_y), xytext=(sig_x + 0.95, sig_y),
            arrowprops=dict(arrowstyle='->', color=CYAN, lw=1.8,
                            mutation_scale=12), zorder=3)

# Threshold box — draw a Heaviside step function inside instead of text
bx0, bx1 = 6.85, 9.05
by0, by1 = sig_y - 0.85, sig_y + 0.85
ax.add_patch(FancyBboxPatch((bx0, by0), bx1 - bx0, by1 - by0,
                            boxstyle='round,pad=0.08',
                            facecolor='#2d1515', edgecolor=RED, lw=2.5, zorder=4))

# Heaviside step function drawn inside the box
mid_x = (bx0 + bx1) / 2        # ≈ 7.95
step_lo_y = sig_y - 0.50
step_hi_y = sig_y + 0.52
margin_x = 0.52
# horizontal baseline → step → plateau
sx = [bx0 + margin_x, mid_x, mid_x, bx1 - margin_x]
sy_ = [step_lo_y,     step_lo_y, step_hi_y, step_hi_y]
ax.plot(sx, sy_, color=RED, lw=2.2, solid_joinstyle='miter', zorder=6)
# dashed vertical at θ
ax.plot([mid_x, mid_x], [step_lo_y - 0.08, step_hi_y + 0.08],
        color=RED, lw=1.1, linestyle='--', alpha=0.55, zorder=6)
# θ label below the step
ax.text(mid_x, by0 + 0.08, 'θ', color=RED, fontsize=10.5,
        ha='center', va='bottom', fontstyle='italic', zorder=7)
# "0" and "1" level markers
ax.text(bx0 + 0.12, step_lo_y, '0', color=RED, fontsize=8, ha='left',
        va='center', alpha=0.75, zorder=7)
ax.text(bx0 + 0.12, step_hi_y, '1', color=RED, fontsize=8, ha='left',
        va='center', alpha=0.75, zorder=7)

ax.text((bx0 + bx1) / 2, by0 - 0.30, 'Binary threshold',
        color=RED, fontsize=9, ha='center')

# Arrow threshold → output
ax.annotate('', xy=(9.60, sig_y), xytext=(bx1, sig_y),
            arrowprops=dict(arrowstyle='->', color=CYAN, lw=1.8,
                            mutation_scale=12), zorder=3)

# Output node
ax.add_patch(Circle((10.05, sig_y), 0.60,
                    facecolor=DARK, edgecolor=CYAN2, lw=2, zorder=4))
ax.text(10.05, sig_y, 'y', color=CYAN2, fontsize=14, ha='center', va='center',
        fontweight='bold', zorder=5)
ax.text(10.05, sig_y - 1.20, 'Binary output\n(0 or 1)',
        color=GRAY, fontsize=9, ha='center', linespacing=1.35)

ax.set_title('McCulloch–Pitts artificial neuron (1943)',
             color=WHITE, fontsize=12, fontweight='bold', pad=6)

fig2.savefig('assets/mp_artificial_neuron.png',
             dpi=150, bbox_inches='tight', facecolor=BG, edgecolor='none')
plt.close(fig2)
print("Saved mp_artificial_neuron.png")
