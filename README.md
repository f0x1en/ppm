# Checking the evidence for QPOP

QPOP (quadratic phenotypic optimization platform, National University of Singapore) tests drug combinations on a patient's tumour cells in the lab, fits a quadratic surface, and ranks every possible combination. Its papers report high accuracy in blood cancers and an optimized drug pair for multiple myeloma.

This repo re-checks those claims using only what the papers themselves publish: main text, supplementary tables and raw data. Where data is missing, simulations fill the gap and are labelled as simulated.

## Verdict

QPOP's lab signal is real but modest, and the published numbers overstate it. The clinical benefit claims and the myeloma dose optimization are not supported by the papers' own data.

## Findings

| Paper | Claim | What the published data show | Notebook |
|---|---|---|---|
| Rashid 2018, myeloma (mice) | QPOP found the optimal Dec + MitoC dose | Output column wrong in 5 of 9 rows; published model cannot be rebuilt from published data; leave-one-out error (15.7 days) is over twice the spread of the data (6.6 days); optimum sits at the highest tested dose | `qpop/mm_invivo_refit.ipynb` |
| Rashid 2018, myeloma (patients) | Dec + MitoC beats clinical regimens ex vivo | 4 patient samples, no outcomes; text contradicts its own Table 4; no clinical study since | `docs/mm2018_notes.md` |
| Sahib 2024, AML | 86.2% accuracy | Real signal (kappa 0.72), but on 29 of 63 samples, against a 62% do-nothing baseline, with the cutoff tuned on the same patients (simulated optimism: 7-11 points) | `qpop/qpop_evidence.ipynb` |
| Lee 2025, lymphoma | 74.5% accuracy, 105 evaluable | Accuracy uses 47 of 126 cases; kappa 0.49, AUROC 0.69, 53% do-nothing baseline | `qpop/qpop_evidence.ipynb` |
| Goh 2022 + Lee 2025, lymphoma | QPOP-guided therapy improves PFS | Paired per-patient PFS: median 81 vs 97 days (2022) and 105 vs 109 days (2025), sign tests p = 0.63 and 0.14; the PFS ratio tracks regression to the mean; one patient's prior PFS changed between papers (284 to 37 days) | `qpop/qpop_evidence.ipynb` |
| All | - | One research group, no independent replication found, no randomized comparison | `docs/sources.md` |

Open questions and the data still missing are in `docs/gaps.md`.

## Files

- `qpop/` re-analysis notebooks with interactive plots (3D surfaces rotate; sliders switch views).
- `docs/sources.md` every paper used, and how much of it was read.
- `docs/mm2018_notes.md` page-referenced notes on the myeloma paper.
- `docs/gaps.md` what cannot be checked yet, and how to get it.
- `sim/curate_sim.ipynb` earlier background work: single-patient dose finding with a quadratic (CURATE.AI-style), simulated.
- `data/` every published number used, one CSV per source table, with sources in `data/README.md`.
- `articles/` papers whose license allows redistribution (currently Lee 2025, CC BY 4.0).
- `tests/` checks that the notebooks still reproduce the published numbers and match `data/`.

The Science Translational Medicine papers are not included because the publisher holds the rights. Get them through the DOIs in `docs/sources.md`.

## Run

```
uv venv && uv pip install -r requirements.txt
.venv/bin/python -m pytest -q tests
.venv/bin/jupyter lab
```
