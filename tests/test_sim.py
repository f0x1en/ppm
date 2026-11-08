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
    space = {}
    for cell in json.loads(EV.read_text())["cells"]:
        if cell["cell_type"] == "code":
            exec("".join(cell["source"]), space)
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
