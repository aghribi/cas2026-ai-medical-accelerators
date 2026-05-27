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
# Extra right margin for the "Synaptic terminals" label placed to the right
R_PAD = 230
PAD_T = 125
PAD_B = 80   # reduced — no "fires when" text any more

fig1, ax = plt.subplots(figsize=(11.5, 5.4), facecolor=BG)
ax.set_facecolor(BG)
ax.axis('off')
ax.imshow(bio_img, zorder=1, aspect='auto')

ax.set_xlim(-20, W + R_PAD)
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

# Dendrites and soma: labels above the image (ly < 0)
ann(ax, 'Dendrites\n(inputs)',     160,  -68,  160, 340, rad= 0.0)
ann(ax, 'Cell body\n(soma)',       475,  -68,  475, 330, rad= 0.0)

# Synaptic terminals: label to the RIGHT of the image (lx > W)
ann(ax, 'Synaptic\nterminals\n(output)', W + 115, H // 2, 1150, 330, rad=-0.20)

# Axon and weights: labels below the image (ly > H)
ann(ax, 'Axon',                    820, H + 50,  820, 390, rad= 0.0)
ann(ax, 'Synaptic\nweights $w_i$', 320, H + 50,  300, 480, rad=-0.15)

ax.set_title('Biological neuron', color=WHITE, fontsize=12,
             fontweight='bold', pad=4)

fig1.savefig('assets/bio_neuron_annotated.png',
             dpi=150, bbox_inches='tight', facecolor=BG, edgecolor='none')
plt.close(fig1)
print("Saved bio_neuron_annotated.png")

# ── Figure 2: McCulloch–Pitts artificial neuron ──────────────────────────────
# Designed for display at ~540px wide / ~280px tall in a reveal.js column.
# Use 100 dpi so fonts appear larger at final display size.
fig2, ax = plt.subplots(figsize=(9.5, 5.0), facecolor=BG)
ax.set_facecolor(BG)
ax.axis('off')
ax.set_xlim(0, 11.2)
ax.set_ylim(-1.5, 10)   # extra room below for labels

sig_x, sig_y = 4.2, 5.2

# Input nodes + weighted arrows
for (lbl, ix, iy), wl in zip(
        [('x₃', 0.85, 8.0), ('x₂', 0.85, 5.2), ('x₁', 0.85, 2.4)],
        ['w₃', 'w₂', 'w₁']):
    ax.add_patch(Ellipse((ix, iy), 1.25, 1.05,
                         facecolor=DARK, edgecolor=CYAN2, lw=2, zorder=4))
    ax.text(ix, iy, lbl, color=WHITE, fontsize=16, ha='center', va='center',
            fontweight='bold', zorder=5)
    ax.annotate('', xy=(sig_x - 0.88, sig_y + (iy - sig_y) * 0.14),
                xytext=(ix + 0.63, iy),
                arrowprops=dict(arrowstyle='->', color=CYAN, lw=2.0,
                                mutation_scale=13), zorder=3)
    mx = (ix + 0.63 + sig_x - 0.88) / 2
    my = (iy + sig_y + (iy - sig_y) * 0.14) / 2 + 0.15
    ax.text(mx, my, wl, color=CYAN2, fontsize=13, ha='center', va='center',
            fontweight='bold')

ax.text(0.85, 1.2, 'Binary inputs', color=GRAY, fontsize=12, ha='center')

# Sigma node
ax.add_patch(Ellipse((sig_x, sig_y), 1.85, 1.65,
                     facecolor=DARK, edgecolor=CYAN, lw=2.5, zorder=4))
ax.text(sig_x, sig_y + 0.08, 'Σ', color=CYAN, fontsize=26, ha='center',
        va='center', fontweight='bold', zorder=5)
ax.text(sig_x, sig_y - 1.45, r'$\Sigma\,w_i x_i$', color=GRAY,
        fontsize=13, ha='center')

# Arrow sigma → threshold
bx0, bx1 = 5.65, 8.10
by0, by1 = sig_y - 0.88, sig_y + 0.88
ax.annotate('', xy=(bx0, sig_y), xytext=(sig_x + 0.93, sig_y),
            arrowprops=dict(arrowstyle='->', color=CYAN, lw=2.0,
                            mutation_scale=13), zorder=3)

# Threshold box
ax.add_patch(FancyBboxPatch((bx0, by0), bx1 - bx0, by1 - by0,
                            boxstyle='round,pad=0.08',
                            facecolor='#2d1515', edgecolor=RED, lw=2.5, zorder=4))

# Heaviside step function drawn inside the box
mid_x   = (bx0 + bx1) / 2        # x position of the threshold
margin  = 0.48
step_lo = sig_y - 0.55
step_hi = sig_y + 0.55
sx = [bx0 + margin, mid_x,  mid_x,  bx1 - margin]
sy = [step_lo,      step_lo, step_hi, step_hi]
ax.plot(sx, sy, color=RED, lw=2.5, solid_joinstyle='miter', zorder=6)
ax.plot([mid_x, mid_x], [step_lo - 0.05, step_hi + 0.05],
        color=RED, lw=1.1, linestyle='--', alpha=0.5, zorder=6)

# θ label at the step transition, centred vertically between 0 and 1
ax.text(mid_x, (step_lo + step_hi) / 2, 'θ', color=RED, fontsize=14,
        ha='left', va='center', fontstyle='italic', zorder=7,
        bbox=dict(boxstyle='square,pad=0.05', facecolor='none',
                  edgecolor='none', alpha=0.0))
# output level markers on the left edge of the step
ax.text(bx0 + 0.12, step_lo, '0', color=RED, fontsize=10.5, ha='left',
        va='center', alpha=0.75, zorder=7)
ax.text(bx0 + 0.12, step_hi, '1', color=RED, fontsize=10.5, ha='left',
        va='center', alpha=0.75, zorder=7)

# "Binary threshold" label BELOW the box — clear of step function
ax.text((bx0 + bx1) / 2, by0 - 0.35, 'Binary threshold',
        color=RED, fontsize=12, ha='center', va='top',
        fontweight='bold', zorder=7)

# Arrow threshold → output
ax.annotate('', xy=(8.65, sig_y), xytext=(bx1, sig_y),
            arrowprops=dict(arrowstyle='->', color=CYAN, lw=2.0,
                            mutation_scale=13), zorder=3)

# Output node
ax.add_patch(Circle((9.15, sig_y), 0.62,
                    facecolor=DARK, edgecolor=CYAN2, lw=2, zorder=4))
ax.text(9.15, sig_y, 'y', color=CYAN2, fontsize=18, ha='center', va='center',
        fontweight='bold', zorder=5)
ax.text(9.15, sig_y - 1.45, 'Binary output\n(0 or 1)',
        color=GRAY, fontsize=12, ha='center', linespacing=1.35)

ax.set_title('McCulloch–Pitts artificial neuron (1943)',
             color=WHITE, fontsize=14, fontweight='bold', pad=8)

fig2.savefig('assets/mp_artificial_neuron.png',
             dpi=100, bbox_inches='tight', facecolor=BG, edgecolor='none')
plt.close(fig2)
print("Saved mp_artificial_neuron.png")
