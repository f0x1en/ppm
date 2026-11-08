# Sources

QPOP = quadratic phenotypic optimization platform (Chow / Ho groups, National University of Singapore).
A patient's tumour cells are exposed ex vivo to ~155 drug combinations from a 12-drug panel; a quadratic model
ranks all 3^12 = 531,441 combinations by predicted cell kill.

"Read" = what was actually read for this repo. Abstract-only papers are paywalled.

| Disease | Paper | Read | Usable numbers |
|---|---|---|---|
| Multiple myeloma | Rashid et al., Sci Transl Med 2018, PMID 30089632 | full text + supplements (see `docs/mm2018_notes.md`) | 114-drug pool; cell lines, mouse model, ex vivo patient samples. **No clinical outcome data.** |
| NHL (lymphoma) | Goh et al., Sci Transl Med 2022, PMID 36260690 | full text + supplement | 71 patients; reports for 67/75 samples; 17 off-label QPOP-guided: CR 5, PR 3, SD/PD 9; paired PFS per patient (Table S7); Fig S2 2x2 (>=2 lines): PD 5/15 vs 11/18, p 0.166; Table S8 = full 155-run 12-drug design |
| NHL (lymphoma) | Lee et al., JCO Precis Oncol 2025, PMID 40700670 | full text + data supplement | 126 cases, 105 evaluable; accuracy 74.5% on 47 cases (TP 18, FP 8, TN 17, FN 4); AUROC 0.69; ORR 16/27 on QPOP-guided therapy; allocation nonrandomized; per-patient PFS for 29 (Table S2) |
| AML | Sahib et al., Cancer Med 2024, PMID 39560206, PMC11574777 | full text (methods, results, discussion) | 63 samples → 59 runs → 55 evaluable → 38 → 29 used; TP 15, FN 3, TN 10, FP 1; cutoff 0.65 NCV chosen by ROC; AUC 0.808 |
| Soft tissue sarcoma | Chan et al., NPJ Precis Oncol 2025, PMID 40121334, PMC11929909 | abstract | 45 samples; "improved or concordant outcomes" (counts not yet read) |
| HCC | Lim et al., J Exp Clin Cancer Res 2022, PMID 35971164, PMC9377092 | title only | bortezomib + CDK inhibitor, patient-derived models |
| HCC (MYC) | Thng et al., Bioeng Transl Med 2023, PMID 36684069, PMC9842033 | title only | preclinical |
| Colorectal | Thng et al., NPJ Precis Oncol 2024, PMID 38413740, PMC10899621 | title only | organoids |
| Head and neck | Chan et al., Exp Hematol Oncol 2025, PMID 39800760, PMC11727331 | title only | preclinical |
| Glioma | Toh et al., PLoS One 2024, PMID 39058662 | title only | trial protocol, no results |
| Critique | Pang, JCO Precis Oncol 2025, PMID 41411607; reply PMID 41411613 | title only | letter on QPOP clinical decision thresholds |
| Myeloma, other methods | Oliver et al., Cancers 2026, PMID 41681883, PMC12896484 | title only | review of ex vivo response prediction in myeloma |

Search: PubMed + Europe PMC via pubmed-search MCP, 2026-11-08.
Every QPOP paper above comes from the same research group; no independent replication was found.
