# Personalized dosing: what the published evidence actually supports

Two ideas from the National University of Singapore are often presented together as "AI-driven personalized medicine":

- **How much: CURATE.AI.** Fit a small curve (linear or quadratic) to *one* patient's own dose and response data, recommend that patient's next dose, refit as new data arrive.
- **Which drugs: QPOP.** Test drug combinations on the patient's tumour cells in the lab, fit a quadratic surface, rank the combinations.

This repo re-checks both with the papers' own published numbers, open datasets from independent groups, and clearly labelled simulations. Nothing here is the author's own clinical research; it is a critical reading of other people's work, built to be reproducible.

## Verdict

- **Per-patient feedback dosing is sound, but the evidence is for the simple version.** The one randomized trial supports CURATE.AI's linear (proportional) variant for tacrolimus, mainly by avoiding under-dosing, and even that result is weaker than reported (P = 0.059 with the test the paper names). The quadratic variant has never been shown to beat simpler rules or usual care, and most patients never collect enough data to calibrate it.
- **Lab testing of a patient's cells has real but modest predictive value** in independent work (myeloma, 34 patients). QPOP's own papers overstate it every time: tuned cutoffs, selected samples, weak baselines, and a myeloma dose "optimization" that its own data do not support.

## Dose optimization (main thread): CURATE.AI

| Study | Claim | What the published data show | Where |
|---|---|---|---|
| Khong 2025, tacrolimus after liver transplant, randomized (n = 56) | Days far off target 24.2% vs 38.4%, P = 0.029 | Used CURATE.AI's linear (proportional) variant, not the quadratic the protocol planned. Gain is mostly less under-dosing. With the two-sided Wilcoxon test the legend names, P = 0.059; 0.029 matches a Welch t-test. One listed secondary outcome has no reported result | `dosing/khong2025_rct_check.ipynb` |
| Sumner 2026, hypertension and type 2 diabetes (n = 18) | Feasible in outpatient care | Only 3 of 18 reached the dosing phase; usable recommendations for 2 people; recommendations changed with the data source; no outcome comparison | `docs/curate_notes.md` |
| Blasiak 2025, chemotherapy, solid tumours (n = 10) | Feasible | 3 of 10 reached the dosing phase; doses boxed into 50-100% of standard; no outcome comparison | `docs/curate_notes.md` |
| Blasiak 2024, Waldenström macroglobulinemia (n = 1) | "Potential" for engagement and clinical efficacy | One patient, no comparator; IgM noisy within cycles | `docs/curate_notes.md` |
| Gan 2025, warfarin, retrospective (n = 127) | Better prediction than other models | CURATE.AI's linear variant predicted slightly better than its quadratic; no head-to-head on the same data; modelled time in range not different from physicians | `docs/curate_notes.md` |
| Single-patient simulation | A 3-point quadratic finds the best dose | Works with low noise and a bowl-shaped truth; fails when the true curve is not a bowl | `sim/curate_sim.ipynb` |

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

- `dosing/` re-analysis of the CURATE.AI randomized trial (per-patient source data).
- `qpop/` QPOP re-analysis notebooks with interactive plots (3D surfaces rotate; sliders switch views).
- `docs/curate_notes.md` notes on the five CURATE.AI dosing studies.
- `docs/sources.md` every paper used, and how much of it was read.
- `docs/mm2018_notes.md` page-referenced notes on the myeloma paper.
- `docs/gaps.md` what cannot be checked yet, and how to get it.
- `sim/curate_sim.ipynb` simulation of single-patient quadratic dose finding, plus early case notes.
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
