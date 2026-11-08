# Articles: where to read every source

Checked with OpenAlex on 2026-11-09. "Free" means a legal open copy exists.

| Paper | Used for | Free? | Read it |
|---|---|---|---|
| Lee et al., JCO Precis Oncol 2025, doi 10.1200/PO-24-00780 | lymphoma accuracy, PFS | yes, CC BY 4.0 | copy in this folder: `lee2025_lymphoma_jcopo_CC-BY-4.0.pdf`; also https://doi.org/10.1200/PO-24-00780 |
| Sahib et al., Cancer Med 2024, doi 10.1002/cam4.70401 | AML accuracy | yes, CC BY | https://pmc.ncbi.nlm.nih.gov/articles/PMC11574777/ |
| Malani et al., Cancer Discov 2022, doi 10.1158/2159-8290.CD-21-0410 | independent open AML data | data: yes, CC BY 4.0 (Zenodo 10.5281/zenodo.7370747); paper: not checked | `scripts/fetch_open_data.sh` downloads the data |
| Ianevski et al., Nat Mach Intell 2019, doi 10.1038/s42256-019-0122-4 (DECREASE) | 192 measured 8x8 combination matrices | data and code open on GitHub (code GPL-3), pinned commit in `scripts/fetch_open_data.sh` | https://github.com/IanevskiAleksandr/DECREASE |
| Chan et al., NPJ Precis Oncol 2025, doi 10.1038/s41698-025-00851-7 | sarcoma (listed, not yet analysed) | yes, CC BY | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11929909/ |
| Rashid et al., Sci Transl Med 2018, doi 10.1126/scitranslmed.aan0941 | myeloma mouse and ex vivo data | no (AAAS) | https://doi.org/10.1126/scitranslmed.aan0941 (library or authors). Supplementary tables: "Supplementary Materials" on the same page |
| Goh et al., Sci Transl Med 2022, doi 10.1126/scitranslmed.abn7824 | lymphoma PFS, Fig S2, design Table S8 | no (AAAS) | https://doi.org/10.1126/scitranslmed.abn7824 (library or authors) |

Every number taken from these papers is in `../data/`, with the table it came from, so the analysis can be checked without the PDFs.

Licence of the included copy: Lee 2025 states "Licensed under the Creative Commons Attribution 4.0 License" on page 1. Unmodified.
Lee RX, Rashid MBMA, Sahib NRBM, et al. Prospective Clinical Validation of a Combinatorial Functional Precision Medicine Platform in Relapsed/Refractory Non-Hodgkin's Lymphoma. JCO Precis Oncol 2025; 9: e2400780.
