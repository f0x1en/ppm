# Data

Numbers copied from the papers' published tables and supplements, one file per source table. Nothing here is simulated.
File names: `<first author><year>_<disease>_<what>_<source table>.csv`.

| File | Paper | Source |
|---|---|---|
| `rashid2018_myeloma_mouse_tableS15_S16.csv` | Rashid et al., Sci Transl Med 2018, doi 10.1126/scitranslmed.aan0941 | Supplement Tables S15 (doses), S16 (outputs, ± SD) |
| `rashid2018_myeloma_mouse_tableS18_model.csv` | same | Supplement Table S18 (published quadratic coefficients) |
| `rashid2018_myeloma_mouse_tableS19_fig5b_death_days.csv` | same | Table S19 (Excel), sheet "Figure 5", panel 5B; one row per recorded death. Group numbers follow Table S15 |
| `rashid2018_myeloma_exvivo_tableS12_concentrations_uM.csv` | same | Supplement Table S12 |
| `rashid2018_myeloma_exvivo_tables2to5_ranks.csv` | same | Main text Tables 2-5 (best Dec + MitoC row and the two clinical regimens per patient) |
| `sahib2024_aml_concordance.csv` | Sahib et al., Cancer Med 2024, doi 10.1002/cam4.70401 (open access) | Results text: sample funnel and 2x2 table |
| `sahib2024_aml_tableS3_concentrations_uM.csv` | same | Supplement Tables S2-S3 (Cmax from Liston & Davis 2017; median blast IC50; QPOP high and low concentrations) |
| `lee2025_lymphoma_concordance.csv` | Lee et al., JCO Precis Oncol 2025, doi 10.1200/PO-24-00780 (CC BY 4.0) | Results text; 2x2 derived from reported TP, TN, PPV 69.2%, NPV 81.0% |
| `lee2025_lymphoma_tableS2_pfs.csv` | same | Data Supplement Table S2 |
| `goh2022_lymphoma_tableS7_pfs.csv` | Goh et al., Sci Transl Med 2022, doi 10.1126/scitranslmed.abn7824 | Supplement Table S7 |
| `goh2022_lymphoma_figS2_pd_6mo.csv` | same | Supplement Fig S2 (progressive disease at 6 months, ≥2 prior lines) |
| `khong2025_tacrolimus_rct_source_data.csv` | Khong et al., Nat Commun 2025, doi 10.1038/s41467-025-59739-6 (CC BY) | Supplementary Data sheets Figure 2-6 and Participants Data (group, target-range flag); rows joined by position (Group order identical across sheets) |
| `chan2025_sarcoma_concordance.csv` | Chan et al., NPJ Precis Oncol 2025, doi 10.1038/s41698-025-00851-7 (CC BY) | Results text and Fig. 1 legend; TP/FP/FN/TN derived from the reported totals (unique solution, reproduces OR 13.5) |
| `kropivsek2023_myeloma_tableS8_fig8b.csv` | Kropivsek et al., Nat Cancer 2023, doi 10.1038/s43018-023-00544-9 (CC BY) | Supplementary Table 8 (S8-Survival) joined with Source Data Fig. 8b (iPCY); columns renamed, values unchanged |
| `tacrolimus_sim_60x3.csv` | Simulation, `scripts/sim_tacrolimus.R` | Daily dose and trough for 60 virtual patients x 3 scenarios x 4 rules; computed here, model from Bai et al. 2024 |
| `decrease_predictions_60_matrices.csv` | DECREASE (Ianevski 2019) run by `scripts/run_decrease.R` | Predictions of the published example model for 60 of the 192 matrices (seed 2026); computed here, not copied from a paper |
| `goh2022_lymphoma_tableS8_oacd_design.csv` | same | Supplement Table S8 (155-run, 12-drug, 3-level design; 0 none, 1 low, 2 high) |

`tests/test_sim.py` checks that the notebooks use exactly these numbers.
