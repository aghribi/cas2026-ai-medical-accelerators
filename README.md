# AI Applications for Medical Accelerators — Accelerator Side

**CAS Topical Course on Medical Accelerators · Jurmala, Latvia · June 2026**  
Dr. Adnan Ghribi — GANIL / CNRS-IN2P3

---

## Quick links

| | |
|---|---|
| **Live slides** | https://aghribi.github.io/cas2026-ai-medical-accelerators/ |
| **Notebook 01** — RF fault detection | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aghribi/cas2026-ai-medical-accelerators/blob/main/notebooks/01_fault_detection/notebook.ipynb) |
| **Notebook 02** — Beam tuning with Cheetah + BO | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aghribi/cas2026-ai-medical-accelerators/blob/main/notebooks/02_beam_tuning/notebook.ipynb) |
| **Notebook 03** — Neural network surrogate | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aghribi/cas2026-ai-medical-accelerators/blob/main/notebooks/03_surrogate_model/notebook.ipynb) |

---

## Lecture structure (50 min + 10 min Q&A)

| Time | Topic |
|------|-------|
| 0–5 min | Medical vs. research accelerators — what changes for AI |
| 5–17 min | **Use case 1**: RF fault detection — autoencoders on IQ waveforms |
| 17–29 min | **Use case 2**: Beam tuning — Bayesian optimisation with Cheetah |
| 29–41 min | **Use case 3**: Surrogate models — replacing tracking codes |
| 41–47 min | Digital twins and open problems |
| 47–50 min | Wrap-up |

---

## Run locally

```bash
# Clone
git clone https://github.com/aghribi/cas2026-ai-medical-accelerators.git
cd cas2026-ai-medical-accelerators

# Create environment (conda)
conda env create -f environment.yml
conda activate cas2026

# Render slides
quarto render index.qmd

# Launch notebooks
jupyter lab
```

## Repository structure

```
├── index.qmd                            ← Quarto reveal.js lecture slides
├── custom.scss                          ← Visual theme (ARTIFACT palette)
├── _quarto.yml                          ← Quarto project config
├── environment.yml                      ← Conda environment
├── requirements.txt                     ← pip requirements (for Colab)
│
├── notebooks/
│   ├── 01_fault_detection/
│   │   ├── notebook.ipynb              ← Autoencoder on synthetic RF waveforms
│   │   └── generate_data.py            ← Synthetic IQ waveform generator
│   ├── 02_beam_tuning/
│   │   └── notebook.ipynb              ← BO with Cheetah (proton lattice)
│   └── 03_surrogate_model/
│       └── notebook.ipynb              ← MLP surrogate + ensemble UQ
│
└── data/                                ← Pre-generated datasets (gitignored if large)
```

## Key tools

| Tool | Role |
|------|------|
| [Cheetah](https://github.com/desy-ml/cheetah) | PyTorch-based differentiable beam dynamics — simulation backbone for notebooks 02 & 03 |
| [xsuite](https://github.com/xsuite/xsuite) | CERN tracking framework for complex lattices (production alternative) |
| [scikit-optimize](https://scikit-optimize.github.io/) | Gaussian Process Bayesian optimisation |
| [Quarto](https://quarto.org/) | Reproducible reveal.js slides from Markdown + Python |

## Key references

- Kaiser et al., *Phys. Rev. Accel. Beams* **27**, 054601 (2024) — Cheetah simulator
- Tennant et al., *PRAB* **23**, 114601 (2020) — SRF fault classification at JLab
- Duris et al., *PRL* **124**, 124801 (2020) — Bayesian optimisation at LCLS
- Ghribi et al., *Europhysics News* **56**(1), 15–19 (2025) — ARTIFACT / KARA −30% result
- AccML living review: https://aghribi.github.io/acc-ml-living-review

## Cite

If you use material from this lecture, please cite:

```bibtex
@misc{ghribi2026cas,
  author    = {Ghribi, Adnan},
  title     = {{AI Applications for Medical Accelerators — Accelerator Side}},
  year      = {2026},
  note      = {CAS Topical Course on Medical Accelerators, Jurmala},
  url       = {https://github.com/aghribi/cas2026-ai-medical-accelerators}
}
```

## License

Code: MIT · Slides content: CC BY 4.0
