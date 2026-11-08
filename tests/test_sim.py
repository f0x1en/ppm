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
