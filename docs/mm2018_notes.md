# Notes: Rashid et al. 2018, QPOP in multiple myeloma

Source: main article PDF, 18 pages (doi 10.1126/scitranslmed.aan0941). Supplements not yet read.
Page numbers refer to the article's own "N of 17" footer.

## What was done

| Stage | System | Design | n | Fit |
|---|---|---|---|---|
| Screen | RPMI 8226 and Bort-resistant P100v cell lines | 114 FDA oncology drugs at 1 and 5 µM; cutoff < 0.6 normalized viability | 1 line pair | none; 4 hits: Dac, Dec, Mech, MitoC (p. 2) |
| QPOP 1 | P100v vs normal THLE-2 cells | 14 drugs x 2 levels, 128 combinations | cell lines | tables S3-S5 |
| QPOP 2 | same | 9 drugs x 3 levels, 155 combinations | cell lines | R² = 0.803 (p. 2) |
| Ex vivo | bone marrow of 4 newly diagnosed patients | 6 drugs (Dec, Bort, MitoC, Pano, Dex, Melph) x 3 levels | 4 | R² > 0.9 (p. 5) |
| In vivo | P100v xenograft mice | Dec + MitoC, 5 levels, 9 test combinations | 4 mice per group | R² = 0.680 (p. 8) |

Model: full second-order polynomial (Eq. 1, p. 14), reduced by stepwise regression that removes terms by F-test p-value.
Output: viability(THLE-2) minus viability(P100v) in vitro; mean survival time minus mean body-weight loss in vivo.

## Ex vivo ranks (Tables 2-5, pp. 6-8). Overall rank out of 3^6 = 729 combinations; lower is better

| Patient | best Dec + MitoC | Bort + Pano + Dex | Bort + Melph + Dex |
|---|---|---|---|
| 1 | 208 (output −2.17) | 562 (−1.36) | 654 (−1.01) |
| 2 | 391 (0.490) | 461 (0.545) | 707 (0.979) |
| 3 | 568 (0.501) | 427 (0.274) | 662 (0.612) |
| 4 | 530 (0.226) | 347 (0.0654) | 98 (−0.109) |

## Problems found (main text only)

1. **Text contradicts its own table.** p. 5 says both clinical combinations ranked higher than Dec/MitoC for patients 3 and 4. Table 4: for patient 3, Bort/Melph/Dex is rank 662, below Dec/MitoC at 568.
2. **No ground truth.** p. 13: testing all combinations to confirm the global optimum "was not done in this study". The claim of global optimality is untested.
3. **In-sample fit only.** R² is reported on the same data used for stepwise term selection. No held-out or cross-validated error is reported.
4. **In vivo objective adds unlike units.** "Mean survival time minus mean loss in body weight" (p. 8). Changing units (days vs weeks, grams vs %) changes the optimum.
5. **Tiny in vivo design.** 9 test combinations, 4 mice each, 2 drugs at 5 levels. R² = 0.680. Interaction p = 0.0489, just under 0.05.
6. **Comparison stacked.** Dec/MitoC beat Bort/Dex/Melph and Bort/Dex/Lena in a model built to be bortezomib-resistant (P100v). Both comparators contain bortezomib.
7. **Negative result.** In a Bort-resistant ALL mouse model, Dec/MitoC did not beat vehicle, single drugs, or clinical combinations (fig. S7, p. 13).
8. **Ex vivo n = 4**, all newly diagnosed. Rankings differ per patient. No patient outcomes.
9. **Ex vivo doses are not reachable in patients, and lopsided.** Table S12 (µM): Dec 30/60, Bort 0.001/0.002, Pano 0.0014/0.0028. With Cmax from Sahib 2024 Table S2 (Liston & Davis 2017): Dec 0.323, Bort 0.312, Pano 0.082 µM. So Dec ran at 93-186x Cmax; Bort at 0.3-0.6% and Pano at 2-3% of Cmax. Dec single-drug IC50 in patient 2 was 7530 µM (Table 1).

## Follow-up

PubMed + Europe PMC + ClinicalTrials.gov (2026-11-09): no clinical study of decitabine + mitomycin C in myeloma found.

## Supplements (read 2026-11-09)

Files (local `papers/`, not in repo): `rashid2018_myeloma_stm_supplement.pdf`, Table S19 (xlsx, 6 sheets = raw data for Figs 1-6), data file S1 (docx with MATLAB code).

Ex vivo concentrations (Table S12, µM, levels −1/0/1): Dec 0/30/60, Bort 0/0.001/0.002, MitoC 0/1/2, Pano 0/0.0014/0.0028, Melph 0/0.4/0.8, Dex 0/0.008/0.016.

### In vivo QPOP re-analysis (Tables S15, S16, S18; computed in this repo)

Design (S15): 9 combinations of MitoC (0-2 mg/kg) and Dec (0-1.5 mg/kg). Output (S16) = survival (days) + body-weight change (g).

1. **Output column arithmetic is wrong in 5 of 9 rows (4 by more than 0.5).** Survival + weight change vs reported output:
   combo 2: 18.94 vs 18.4; combo 4: 26.43 vs 27.3; combo 7: 27.42 vs 26.7; combo 8: 26.65 vs 26.5; combo 9 (centre point, the best one): 35.67 vs 38.4.
2. **The published model (S18) is not reproducible from the published outputs.**
   Least-squares fit of the full quadratic to S16 outputs: coefficients [16.54, 20.47, 0.22, 0.67, −9.08, 0.93], R² 0.537.
   Paper: [14.9, 15.2, 10.0, 2.00, −6.41, −4.29], R² 0.680. Survival-only fit: [14.95, 16.61, 6.31, 1.53, −7.09, −2.29], R² 0.720, closer but not equal.
   The paper's model evaluated at its own 9 points: combo 6 predicts 30.6 vs 21.1 reported; combo 9 predicts 30.3 vs 38.4.
3. **The fit has no predictive value.** 6 coefficients on 9 points leaves 3 degrees of freedom. Leave-one-out:
   the optimum moves from (MitoC 0.53, Dec 0) to (MitoC 2.0, Dec 0.8) depending on which group is dropped;
   held-out predictions miss by up to 30 days (drop combo 4: predicted −2.7, observed 27.3). Leave-one-out RMSE 15.7 days vs output SD 6.6 days: worse than predicting the mean.
4. **The optimum is on the edge.** Every fit puts Dec at or near 1.5 mg/kg, the highest dose tested, so the true optimum may lie outside the tested range.
5. **Table errors.** S18 title says "four drugs at five levels"; the model has two drugs. S17 has a rank written "x14".
6. **Raw survival data (S19, Fig 5B) do not match S16 survival means.** S19 records fewer than 4 deaths per group (DMSO: 1 death, day 15), and means of recorded death days differ from S16 (centre point: 29.75 vs 35.3).
   Unknown: whether the missing mice are censored (alive at end or euthanized at 15 mm tumour) and how S16 treated them. Not explained in the main text.
