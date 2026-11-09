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
| Soft tissue sarcoma | Chan et al., NPJ Precis Oncol 2025, PMID 40121334, PMC11929909 | results (publisher HTML, CC BY) | reports 45/51; 27 outcomes from 14 patients; PR 7, SD 9, PD 11; cutoff 0.8305 by ROC, AUC 0.769; rebuilt 2x2 TP 12, FP 2, FN 4, TN 9 (OR 13.5) |
| HCC | Lim et al., J Exp Clin Cancer Res 2022, PMID 35971164, PMC9377092 | title only | bortezomib + CDK inhibitor, patient-derived models |
| HCC (MYC) | Thng et al., Bioeng Transl Med 2023, PMID 36684069, PMC9842033 | title only | preclinical |
| Colorectal | Thng et al., NPJ Precis Oncol 2024, PMID 38413740, PMC10899621 | title only | organoids |
| Head and neck | Chan et al., Exp Hematol Oncol 2025, PMID 39800760, PMC11727331 | title only | preclinical |
| Glioma | Toh et al., PLoS One 2024, PMID 39058662 | title only | trial protocol, no results |
| Critique | Pang, JCO Precis Oncol 2025, PMID 41411607; reply PMID 41411613 | title only | letter on QPOP clinical decision thresholds |
| Myeloma, other methods | Oliver et al., Cancers 2026, PMID 41681883, PMC12896484 | title only | review of ex vivo response prediction in myeloma |

Search: PubMed + Europe PMC via pubmed-search MCP, 2026-11-08.
Every QPOP paper above comes from the same research group; no independent replication was found.

## CURATE.AI (per-patient dosing), the main thread

| Indication | Paper | Read | Usable numbers |
|---|---|---|---|
| Tacrolimus, liver transplant, RCT | Khong et al., Nat Commun 2025, doi 10.1038/s41467-025-59739-6 (CC BY), NCT03527238 | full text + Supplementary Information (protocol) + source data | per-patient outcomes for 56 patients (`data/khong2025_tacrolimus_rct_source_data.csv`) |
| Tacrolimus, paediatric liver transplant, retrospective | Tan et al., Adv Ther 2023, doi 10.1002/adtp.202300236 | not yet | - |
| Warfarin, retrospective | Gan et al., Bioeng Transl Med 2025, doi 10.1002/btm2.10757, PMC12079355 | full text | see `docs/curate_notes.md` |
| Solid-tumour chemotherapy (PRECISE) | Blasiak et al., NPJ Precis Oncol 2025, doi 10.1038/s41698-025-00835-7, PMC11845749 | full text | see `docs/curate_notes.md` |
| Waldenström macroglobulinemia (PRECISE) | Blasiak et al., npj Digit Med 2024, doi 10.1038/s41746-024-01195-5, PMC11350179 | full text | see `docs/curate_notes.md` |
| Hypertension and type 2 diabetes, feasibility | Sumner et al., JAMIA Open 2026, doi 10.1093/jamiaopen/ooaf153, PMC12794016; protocol Mukhopadhyay 2022, PMC9332044 | full text | see `docs/curate_notes.md` |
| Hypertension, pilot RCT | Wang et al., Eur Heart J 2026 suppl (abstract), doi 10.1093/eurheartj/ehag785.3053; protocol Truong 2024, PMC10802822 | not yet | - |
| Prostate cancer, single patient | Pantuck et al., Adv Ther 2018 | numbers used in `sim/curate_sim.ipynb` | - |

Mainstream comparison method: Bayesian model-informed precision dosing; open tool `posologyr` (CRAN, AGPL-3).

## Independent work used for comparison

| Topic | Paper | Read | Usable numbers |
|---|---|---|---|
| AML, open data | Malani et al., Cancer Discov 2022, doi 10.1158/2159-8290.CD-21-0410; data Zenodo 10.5281/zenodo.7370747 (CC BY 4.0) | data files | 515-drug sDSS for 164 samples; clinical summary for 186 patients (`qpop/open_aml_check.ipynb`) |
| Combination surfaces | Ianevski et al., Nat Mach Intell 2019 (DECREASE), doi 10.1038/s42256-019-0122-4; GitHub IanevskiAleksandr/DECREASE (GPL-3) | code + data | 192 measured 8x8 matrices (`qpop/real_surfaces_check.ipynb`) |
| Myeloma, ex vivo vs clinic | Kropivsek et al., Nat Cancer 2023, doi 10.1038/s43018-023-00544-9, PMC10212768 (CC BY) | results + methods text | 34 patients tested before their next line: ex vivo "sensitive" (above subcohort mean iPCY) had longer time to next treatment, HR 4.57 (95% CI 1.77-11.8), log-rank P = 0.0076; immunotherapy subcohort n = 15, HR 7.01 (1.59-31); non-immunotherapy n = 19, HR 3.49 (1.01-12.1), P = 0.0898. Patient-level data: Supplementary Table 8 + Fig 8b source data, re-analysed in `qpop/myeloma_independent_check.ipynb` |

Replication search, 2026-11-09 (PubMed, Europe PMC, OpenAlex; query `"Optim.AI" OR "KYAN Technologies" OR "quadratic phenotypic optimization"`):
the platform is now sold as Optim.AI by KYAN Technologies (Rashid, a QPOP author, is listed with a KYAN affiliation in Sahib 2024).
All further hits are from the same authors (Rashid, Lim, Chan, Chow), and most are conference abstracts, for example
Cancer Res 2025 abstract 7214 ("real-world concordance", doi 10.1158/1538-7445.am2025-7214) and Cancer Res 2026 abstract 2517 (doi 10.1158/1538-7445.am2026-2517).
Conference abstracts are not peer-reviewed full papers and give too little detail to check.
