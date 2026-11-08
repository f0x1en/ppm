# Checking the evidence for QPOP

QPOP (quadratic phenotypic optimization platform, National University of Singapore) tests drug combinations on a patient's tumour cells in the lab, fits a quadratic surface, and ranks every possible combination. Its papers report high accuracy in blood cancers and an optimized drug pair for multiple myeloma.

This repo re-checks those claims using only what the papers themselves publish: main text, supplementary tables and raw data. Where data is missing, simulations fill the gap and are labelled as simulated.

## Verdict

QPOP's design is sensible and its lab signal is real but modest; noise limits it, and the published numbers overstate it. Independent open data give mixed support for the shared premise (lab response predicts clinical response): positive but small in myeloma (34 patients), not shown for single induction drugs in AML (42 patients). The clinical benefit claims and the myeloma dose optimization are not supported by the papers' own data.

## Dose optimization (main thread): CURATE.AI-style per-patient dosing

| Study | Claim | What the published data show | Notebook |
|---|---|---|---|
| Khong 2025, tacrolimus after liver transplant, randomized (n = 56) | CURATE.AI-group dosing ("PPM") cuts days far off target: 24.2% vs 38.4%, P = 0.029 | The trial did not use the per-patient quadratic: its calibration "could therefore not be applied", so a proportional day-to-day rule was used. The gain is mostly less under-dosing. With the two-sided Wilcoxon test the legend names, P = 0.059; 0.029 matches a Welch t-test. One listed secondary outcome has no reported result | `dosing/khong2025_rct_check.ipynb` |

Other CURATE.AI studies (hypertension/diabetes, chemotherapy, Waldenström, warfarin, paediatric tacrolimus) are being checked next; see `docs/sources.md`.

## Drug selection (supporting section): QPOP


| Paper | Claim | What the published data show | Notebook |
|---|---|---|---|
| Rashid 2018, myeloma (mice) | QPOP found the optimal Dec + MitoC dose | Output column wrong in 5 of 9 rows; published model cannot be rebuilt from published data; leave-one-out error (15.7 days) is over twice the spread of the data (6.6 days); optimum sits at the highest tested dose | `qpop/mm_invivo_refit.ipynb` |
| Rashid 2018, myeloma (patients) | Dec + MitoC beats clinical regimens ex vivo | 4 patient samples, no outcomes; decitabine tested at 93-186x patient Cmax while bortezomib and panobinostat were at under 4% of theirs; text contradicts its own Table 4; no clinical study since | `docs/mm2018_notes.md` |
| Sahib 2024, AML | 86.2% accuracy | Real signal (kappa 0.72), but on 29 of 63 samples, against a 62% do-nothing baseline, with the cutoff tuned on the same patients (simulated optimism: 7-11 points); on all 38 evaluated runs AUC is 0.72, not 0.81; five drugs at ~20% of Cmax despite a stated 10% limit | `qpop/qpop_evidence.ipynb` |
| Lee 2025, lymphoma | 74.5% accuracy, 105 evaluable | Accuracy uses 47 of 126 cases; kappa 0.49, AUROC 0.69, 53% do-nothing baseline | `qpop/qpop_evidence.ipynb` |
| Chan 2025, sarcoma | Concordance 77.8% (OR 13.5) | 27 outcomes from only 14 patients counted as independent; stable disease counted as response; cutoff tuned on the same outcomes; 59% do-nothing baseline; rebuilt 2x2 TP 12, FP 2, FN 4, TN 9 matches the reported OR and Fisher p | `qpop/qpop_evidence.ipynb` |
| Goh 2022 + Lee 2025, lymphoma | QPOP-guided therapy improves PFS | Paired per-patient PFS: median 81 vs 97 days (2022) and 105 vs 109 days (2025), sign tests p = 0.63 and 0.14; the PFS ratio tracks regression to the mean; one patient's prior PFS changed between papers (284 to 37 days) | `qpop/qpop_evidence.ipynb` |
| All | - | One research group, no independent replication found, no randomized comparison | `docs/sources.md` |
| QPOP's foundation, on 192 measured surfaces (DECREASE open data) | Drug-combination response is a smooth quadratic surface | Median R² 0.90 even with all 64 points; from QPOP-style 3x3 points the quadratic predicts unmeasured combinations worse than the plain Bliss baseline (median RMSE 0.106 vs 0.074), and depends strongly on the dose levels chosen | `qpop/real_surfaces_check.ipynb` |
| Shared premise, myeloma, independent group (Kropivsek 2023, Zurich, CC BY) | Lab sensitivity predicts time to next treatment | **Supported, small.** Published log-rank P = 0.00763 reproduces exactly; robust to cutoff, single patients, permutation (P = 0.009) and transplant stratification (HR 0.20, 0.06-0.74); 34 patients, 17 events, C-index of the raw score 0.64 | `qpop/myeloma_independent_check.ipynb` |
| Shared premise, on independent open data (Malani 2022, FIMM, CC BY) | Lab sensitivity of a patient's cells predicts clinical response | 42 AML patients on intensive induction: lab sensitivity to their induction drugs gives AUC 0.44-0.67 (intervals include 0.5); age alone gives 0.74, genetic risk class 0.70 | `qpop/open_aml_check.ipynb` |
| Method itself (simulation on the real 155-run design) | Quadratic over 155 runs finds the best combination | Fair in principle: with low noise the true best doublet is in the top 3 most of the time, and drug-drug terms clearly help when synergy exists. At plausible assay noise the top-3 hit rate falls to about 40-75%. Truth model is made up | `qpop/qpop_design_stress.ipynb` |

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
sh scripts/fetch_open_data.sh        # open datasets into ext/ (needed for open_aml_check, real_surfaces_check)
.venv/bin/python -m pytest -q tests
.venv/bin/jupyter lab
```
