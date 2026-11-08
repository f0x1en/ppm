# Personalized dosing from a few noisy measurements

A small, runnable study of the idea behind CURATE.AI (NUS): fit a low-order curve or surface to a handful of dose-response measurements, then pick the best dose. The question is how far that gets you, and when it breaks.

Everything is in `sim/curate_sim.ipynb`. The plots are interactive (rotate the 3D ones, use the noise sliders).

| Part | What it shows | Data |
|---|---|---|
| 1-3 | One drug, 3 noisy points, quadratic fit: success rate and regret vs noise | simulated |
| 4-5 | Two drugs, 6 points, 3D response surface | simulated |
| Case A | Prostate cancer, ZEN3694 + enzalutamide: predicted vs observed PSA | published numbers |
| Case B | Liver transplant tacrolimus: standard dosing vs feedback dosing | published rates + simulated patients |
| Case C | Multiple myeloma, two drugs with S-shaped kill curves | synthetic |

## Main finding

The quadratic works when the truth is a smooth bowl and fails when it is not. On the myeloma-like surface it picks the exact best pair 9% of the time with zero noise (random pair: 5%). Less noise does not fix a wrong model shape, so a model check against the next observed response is needed.

## Limits

- No myeloma CURATE.AI dosing data was found (PubMed and Europe PMC, 2026-11-08). Case C is synthetic and proves nothing clinical.
- Published CURATE.AI evidence is small, non-randomized studies, mostly from one group.
- Noise levels and surface shapes are chosen by hand.

## Run

```
uv venv && uv pip install -r requirements.txt
.venv/bin/python -m pytest -q tests
.venv/bin/jupyter lab sim/curate_sim.ipynb
```

`CURATE_AI.md`, `README_en.md` and `README_fa.md` are the earlier product proposal and feasibility study.
