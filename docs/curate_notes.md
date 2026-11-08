# Notes: CURATE.AI per-patient dosing studies

All papers here are from the CURATE.AI group (National University of Singapore and collaborators). Quotes are from the open-access full texts.
Read with scepticism: every study below is small, single-centre, and judged by its own authors.

## 1. Tacrolimus after liver transplant, randomized (Khong et al., Nat Commun 2025, CC BY)

Full re-analysis with the per-patient source data: `dosing/khong2025_rct_check.ipynb`.

- Used CURATE.AI's **linear (proportional) variant**, "Function 2" (constant trough-to-dose ratio from one day to the next). The quadratic calibration the protocol planned ("Function 1") "could therefore not be applied to this study".
- Primary outcome 24.2% vs 38.4% of days far off target. Reported P = 0.029; with the two-sided Wilcoxon test the figure legend names, the published data give P = 0.059 (0.029 matches a Welch t-test).
- Benefit is mostly less under-dosing (mean trough 8.4 vs 7.6 ng/mL).

## 2. Hypertension and type 2 diabetes, single-arm feasibility (Sumner et al., JAMIA Open 2026, CC BY, PMC12794016)

- Used the quadratic: "three distinct datapoints that linked drug dose to clinical response".
- 18 recruited, 13 completed, **3 reached the active phase**, "primarily due to insufficient dose adjustments required during the calibration phase". Calibration also had to restart "if medications unrelated to the principal diagnosis changed".
- Recommendations depended on the data source: the paper fits separate quadratic curves for amlodipine from four data sources and for insulin from three.
- Per participant: ID01, physician matched CURATE.AI at all 4 visits (agreement, not shown benefit); ID02, no actionable recommendation; ID05, disagreed at 3 of 4 visits (CURATE.AI higher), and the HbA1c curve gave no recommendation.
- Conclusion claims "feasibility" based on actionable recommendations for 2 people. No outcome was compared with usual care.

## 3. Waldenström macroglobulinemia, one patient (Blasiak et al., npj Digit Med 2024, CC BY, PMC11350179)

- Closest disease to myeloma in the CURATE.AI work. One 80-year-old man, ibrutinib, target = serum IgM, two years.
- Quadratic dose-response profile, recalibrated when "systemic changes" occurred.
- Doses ranged 61.9-91.7% of standard; cumulative dose 22.3% below projected standard of care, 11.6% below the "MTD-adjusted" standard.
- "The patient's IgM demonstrated significant intracycle variability": exactly the measurement noise that makes 3-point quadratic fits unstable (see `sim/curate_sim.ipynb`).
- No comparator. Dose-limiting toxicity (grade 2 epistaxis) at cycle 12 narrowed the usable dose range. Reported outcomes are feasibility and adherence; "clinical efficacy" cannot be judged from one patient.

## 4. Chemotherapy, solid tumours, feasibility (Blasiak et al., NPJ Precis Oncol 2025, CC BY-NC-ND, doi 10.1038/s41698-025-00835-7)

- Quadratic profile on a tumour marker (CEA in 9 patients, CA125 in 1); CURATE.AI dosed capecitabine only, other drugs by physicians.
- **10 patients** (pre-specified), one hospital, no blinding. **3 reached the efficacy-driven dosing stage**; their profiles gave 11 recommendations, "which were all accepted".
- Recommendations were boxed in by a safety range of 50-100% of the standard dose plus patient-specific limits.
- 29 "systemic changes" in 10 patients, 19 absorbed into the model. Outcomes are feasibility and adherence; no comparison with standard dosing.

## 5. Warfarin, retrospective (Gan et al., Bioeng Transl Med 2025, PMC12079355)

- 127 patients' records, modelled retrospectively; no patient was dosed by CURATE.AI.
- The paper tried both a quadratic and a **linear** CURATE.AI. Five-fold cross-validation median absolute prediction error: quadratic 15.2-15.5%, **linear 14.3-14.6%**. The simpler model did slightly better.
- Comparison with other published warfarin models used each model's own reported metrics on other datasets; a statistical comparison "was not able to be performed" for lack of raw data.
- "Modeled potential time in therapeutic range with CURATE.AI was not significantly different from physician-guided dosing."
- The abstract still calls CURATE.AI "clinically validated in a range of indications".

## Pattern across the five studies

1. CURATE.AI comes in a **linear** and a **quadratic** variant. The quadratic has not been shown to beat the linear one: in warfarin the linear version predicted slightly better, and the only randomized trial used the linear variant.
2. **Calibration is the bottleneck**: 3 of 18 (hypertension/diabetes), 3 of 10 (chemotherapy) reached the dosing stage.
3. **No outcome benefit over usual care has been shown with the quadratic model.** Agreement with physicians and "feasibility" are the main reported results.
4. All studies are by the developers, small, mostly single-centre and unblinded.

## Not yet read

Tan et al. 2023 (paediatric tacrolimus, retrospective), Wang et al. 2026 (hypertension pilot RCT, conference abstract only).
