"""Run the notebook's code cells in one namespace and check the claims it makes."""
import json
from pathlib import Path

import pytest

NB = Path(__file__).parent.parent / "sim" / "curate_sim.ipynb"


@pytest.fixture(scope="module")
def ns():
    space = {}
    for cell in json.loads(NB.read_text())["cells"]:
        if cell["cell_type"] == "code":
            exec("".join(cell["source"]), space)
    return space


def test_one_drug_beats_random_without_noise(ns):
    assert ns["success"][0] > 0.99
    assert ns["success"][0] > ns["random_success"]


def test_success_falls_with_noise(ns):
    assert ns["success"][-1] < ns["success"][0]


def test_two_drug_beats_random_without_noise(ns):
    assert ns["success2"][0] > 0.9 > ns["random_success2"]


def test_myeloma_optimum_is_interior(ns):
    assert 0 < ns["OPT_MM"][0] < 30 and 0 < ns["OPT_MM"][1] < 30


def test_quadratic_struggles_on_s_curve(ns):
    assert ns["success_mm"][0] < 0.5 < ns["success2"][0]


EV = Path(__file__).parent.parent / "qpop" / "qpop_evidence.ipynb"


@pytest.fixture(scope="module")
def ev():
    import os
    space, cwd = {}, os.getcwd()
    os.chdir(EV.parent)
    try:
        for cell in json.loads(EV.read_text())["cells"]:
            if cell["cell_type"] == "code":
                exec("".join(cell["source"]), space)
    finally:
        os.chdir(cwd)
    return space


def test_aml_counts_match_paper(ev):
    assert ev["N_AML"] == 29
    assert round((ev["TP"] + ev["TN"]) / ev["N_AML"], 3) == 0.862
    assert round(ev["TP"] / (ev["TP"] + ev["FN"]), 3) == 0.833
    assert round(ev["TN"] / (ev["TN"] + ev["FP"]), 3) == 0.909


def test_wilson_known_value(ev):
    lo, hi = ev["wilson"](5, 10)
    assert abs(lo - 0.2366) < 1e-3 and abs(hi - 0.7634) < 1e-3


def test_tuned_cutoff_is_optimistic(ev):
    assert (ev["REP"] > ev["TRUE"]).all()


MM = Path(__file__).parent.parent / "qpop" / "mm_invivo_refit.ipynb"


@pytest.fixture(scope="module")
def mm():
    space = {}
    for cell in json.loads(MM.read_text())["cells"]:
        if cell["cell_type"] == "code":
            exec("".join(cell["source"]), space)
    return space


def test_paper_model_reproduces_its_own_ranked_table(mm):
    # Table S17: (MitoC 0, Dec 0) -> 15 days, (1.5, 1.5) -> 33 days
    assert round(float(mm["X"](0.0, 0.0) @ mm["PAPER"])) == 15
    assert round(float(mm["X"](1.5, 1.5) @ mm["PAPER"])) == 33


def test_refit_differs_from_paper(mm):
    b, r2 = mm["fit"](mm["OUT"])
    assert abs(r2 - 0.680) > 0.1
    assert abs(b[2] - mm["PAPER"][2]) > 5  # Dec coefficient


def test_leave_one_out_worse_than_mean(mm):
    err = [p - o for _, _, _, p, o, _ in mm["loo"]]
    assert (sum(e * e for e in err) / 9) ** 0.5 > mm["OUT"].std(ddof=1)


def test_goh2022_pairs_and_fig_s2(ev):
    assert len(ev["PFS_PREV"]) == len(ev["PFS_QPOP"]) == 17
    assert ev["n_up"] == 10                       # paper: "10 of 17 patients (59%)"
    assert round(5 * 7 / (10 * 11), 2) == 0.32    # Fig S2 OR
    assert abs(ev["fisher_two_sided"](5, 10, 11, 7) - 0.166) < 0.005


def test_lee2025_pfs_table(ev):
    assert len(ev["L25"]) == 29
    assert int((ev["R25"] > 1.3).sum()) == 16      # 16/27 = 59.3% as reported
    assert ev["L25"]["3834-FB"] == (37, 49)


DATA = Path(__file__).parent.parent / "data"


def _csv(name):
    import csv
    with open(DATA / name) as f:
        return list(csv.DictReader(f))


def test_data_files_match_mouse_notebook(mm):
    rows = _csv("rashid2018_myeloma_mouse_tableS15_S16.csv")
    for key, col in [("MITO", "mitoc_mg_kg"), ("DEC", "dec_mg_kg"), ("SURV", "survival_days_mean"),
                     ("WT", "weight_change_g_mean"), ("OUT", "reported_output")]:
        assert [float(r[col]) for r in rows] == list(mm[key])
    model = [float(r["estimate"]) for r in _csv("rashid2018_myeloma_mouse_tableS18_model.csv")][:6]
    assert model == list(mm["PAPER"])


def test_data_files_match_evidence_notebook(ev):
    g22 = _csv("goh2022_lymphoma_tableS7_pfs.csv")
    assert [int(r["pfs_prev_days"]) for r in g22] == list(ev["PFS_PREV"])
    assert [int(r["pfs_qpop_days"]) for r in g22] == list(ev["PFS_QPOP"])
    assert {r["patient_id"]: (int(r["pfs_prev_days"]), int(r["pfs_qpop_days"]))
            for r in _csv("lee2025_lymphoma_tableS2_pfs.csv")} == ev["L25"]
    aml = {r["quantity"]: float(r["value"]) for r in _csv("sahib2024_aml_concordance.csv")}
    assert (aml["TP"], aml["FN"], aml["TN"], aml["FP"]) == (ev["TP"], ev["FN"], ev["TN"], ev["FP"])
    nhl = {r["quantity"]: float(r["value"]) for r in _csv("lee2025_lymphoma_concordance.csv")}
    assert {k: nhl[k] for k in ("TP", "FP", "TN", "FN")} == ev["NHL"]


ST = Path(__file__).parent.parent / "qpop" / "qpop_design_stress.ipynb"


@pytest.fixture(scope="module")
def st():
    import os
    space, cwd = {}, os.getcwd()
    os.chdir(ST.parent)
    try:
        for cell in json.loads(ST.read_text())["cells"]:
            if cell["cell_type"] == "code":
                exec("".join(cell["source"]), space)
    finally:
        os.chdir(cwd)
    return space


def test_design_matches_paper(st):
    assert st["DESIGN"].shape == (155, 12)
    assert len(st["DOUBLETS"]) == 66 * 4


def test_quadratic_beats_random_and_uses_interactions(st):
    res = st["RES"]
    assert (res[:, 0, 0, 1] > 0.7).all()                       # no noise: top-3 hit rate
    assert res[..., 2, 1].mean() < 0.03                        # random pick
    assert (res[-1, :, 0, 1] > res[-1, :, 1, 1]).all()         # strong synergy: quadratic beats no-interaction


def test_lab_concentrations_vs_cmax(ev):
    assert sorted(d for d, v in ev["aml_ratio"].items() if v > 0.10) == [
        "azacytidine", "bortezomib", "dasatinib", "gilteritinib", "midostaurin"]
    assert ev["mm_ratio"]["decitabine"] > 90 and ev["mm_ratio"]["bortezomib"] < 0.01


OA = Path(__file__).parent.parent / "qpop" / "open_aml_check.ipynb"
MALANI = Path(__file__).parent.parent / "ext" / "malani2022"


@pytest.mark.skipif(not MALANI.exists(), reason="run scripts/fetch_open_data.sh first")
def test_open_aml_cohort():
    import os
    space, cwd = {}, os.getcwd()
    os.chdir(OA.parent)
    try:
        for cell in json.loads(OA.read_text())["cells"]:
            if cell["cell_type"] == "code":
                exec("".join(cell["source"]), space)
    finally:
        os.chdir(cwd)
    assert len(space["Y"]) == 42 and space["Y"].sum() == 34
    assert space["AUC"]["Age at diagnosis"][0] > space["AUC"]["Cyt + Ida mean"][0]


RS = Path(__file__).parent.parent / "qpop" / "real_surfaces_check.ipynb"
DEC = Path(__file__).parent.parent / "ext" / "decrease"


@pytest.mark.skipif(not DEC.exists(), reason="run scripts/fetch_open_data.sh first")
def test_real_surfaces():
    import os
    space, cwd = {}, os.getcwd()
    os.chdir(RS.parent)
    try:
        for cell in json.loads(RS.read_text())["cells"]:
            if cell["cell_type"] == "code":
                exec("".join(cell["source"]), space)
    finally:
        os.chdir(cwd)
    res = space["RES"]
    assert len(res) == 192
    assert res.rmse_bliss.median() < res.rmse_quad9.median()
