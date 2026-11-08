# Gaps: what we cannot check yet

Each row: what is missing, why it matters, and how to get it.

| # | Paper | Missing | Why it matters | Route |
|---|---|---|---|---|
| 1 | Rashid 2018 (myeloma) | How Table S18 was fitted: per-mouse or group means, censoring, units, any weighting | Published coefficients cannot be rebuilt from Table S16 | email authors (draft: `papers/emails/chow_mm2018.md`) |
| 2 | Rashid 2018 | Per-mouse survival, including censored mice | Table S19 Fig 5B records fewer than 4 deaths per group; means differ from S16 | same email |
| 3 | Rashid 2018 | Full input data for the 128-, 155- and ex vivo fits | Data file S1 holds only 10 of 128 rows; no fit can be reproduced | same email |
| 4 | Rashid 2018 | Ex vivo raw viability per patient (6 drugs x 3 levels) | Tables 2-5 give ranks only; cannot test robustness of the patient rankings | same email |
| 5 | Lee 2025 (lymphoma) | RESOLVED: accuracy is on 47 cases, 2x2 = TP 18, FP 8, TN 17, FN 4 | - | - |
| 6 | Pang 2025 letter + reply | Full text | The only published outside critique of QPOP | paywalled; ask authors or a library |
| 7 | Sahib 2024 (AML) | Which of the first 22 samples (used to tune doses) are among the 29 scored; full 2x2 for all 38 runs (Fig S3 gives AUC 0.719 only) | Overlap would mean the doses were tuned on test patients | email Chow (AML co-corresponding author); Tables S2-S3 now read |
| 8 | Goh 2022 / Lee 2025 (lymphoma) | Why patient 3834-FB previous PFS changed 284 to 37 days; which 2 of 29 were excluded; how 105 cases became 47 | Changes the "improved" count; tests cutoff tuning | email (draft: `papers/emails/jeyasekharan_nhl.md`) |
| 9 | All | Independent replication | Every QPOP paper and abstract comes from one group (see `docs/sources.md`) | none found 2026-11-09; search again later |
| 10 | Chan 2025 (sarcoma) | RESOLVED: counts from the publisher's open HTML; 2x2 rebuilt | - | `qpop/qpop_evidence.ipynb` section 8 |
| 11 | Kropivsek 2023 (myeloma, independent group) | RESOLVED: Supplementary Table 8 + Fig 8b source data downloaded from the publisher's supplement server (CC BY) | - | `qpop/myeloma_independent_check.ipynb` |
