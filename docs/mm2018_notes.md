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
9. **Doses to check.** Ex vivo Dec levels 30 and 60 (units in table S12, not yet read). Dec single-drug IC50 in patient 2 is 7530 µM (Table 1). Whether these concentrations are reachable in patients is not checked yet.

## Follow-up

PubMed + Europe PMC + ClinicalTrials.gov (2026-11-09): no clinical study of decitabine + mitomycin C in myeloma found.

## Needed from supplements

Table S12 (ex vivo drugs and concentrations), S6-S8 (155-combination design and coefficients), S15-S18 (in vivo design, output, ranks, coefficients), S19 (primary data, Excel), data file S1 (MATLAB code).
