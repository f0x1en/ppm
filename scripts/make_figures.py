"""Static PNG figures for the README (GitHub does not render the notebooks' plotly charts).

Run from the repo root: .venv/bin/python scripts/make_figures.py
Same computations as the notebooks; numbers come from data/ (and ext/decrease for the DECREASE figure).
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA, OUT = ROOT / "data", ROOT / "figures"
OUT.mkdir(exist_ok=True)
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]          # categorical slots 1-4, fixed order
INK, MUTED, SURF = "#0b0b0b", "#52514e", "#fcfcfb"
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
                     "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "axes.axisbelow": True,
                     "grid.color": "#e4e3df", "grid.linewidth": 0.8, "font.size": 10, "axes.titlesize": 11})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=150)
    plt.close(fig)
    print("wrote", OUT / name)


def tacrolimus_rules():
    S = pd.read_csv(DATA / "tacrolimus_sim.csv")
    S["far"] = np.maximum(8 - S.trough, S.trough - 10) > 2
    W = S[S.day >= 4]
    far = W.groupby(["scenario", "rule", "id"]).far.mean().groupby(["scenario", "rule"]).mean().unstack("rule")
    order = ["fixed", "linear", "quadratic", "bayes"]
    sc = list(far.index)
    fig, ax = plt.subplots(figsize=(9, 4.6))
    w = 0.2
    for i, r in enumerate(order):
        x = np.arange(len(sc)) + (i - 1.5) * w
        ax.bar(x, 100 * far[r].to_numpy(), w * 0.92, color=C[i], label=r)
        if "calibrated" in sc:
            k = sc.index("calibrated")
            ax.text(x[k], 100 * far[r].iloc[k] + 0.8, f"{100 * far[r].iloc[k]:.1f}", ha="center", fontsize=8, color=INK)
    ax.axhline(38.4, color=MUTED, ls=":", lw=1.2)
    ax.axhline(24.2, color=MUTED, ls="--", lw=1.2)
    tr = ax.get_yaxis_transform()
    ax.text(1.01, 38.4, "trial,\nstandard care\n38.4%", transform=tr, va="center", fontsize=8, color=MUTED)
    ax.text(1.01, 24.2, "trial,\nCURATE.AI linear\n24.2%", transform=tr, va="center", fontsize=8, color=MUTED)
    ax.set_xticks(range(len(sc)), sc)
    ax.set_ylabel("% days far (>2 ng/mL) off target, days 4-14")
    ax.set_title("Virtual tacrolimus patients: days far off target, by dosing rule")
    ax.legend(title="rule", frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.08))
    save(fig, "tacrolimus_rules.png")


def calibration():
    sys.path.insert(0, str(ROOT / "dosing"))
    import calib
    p = pd.read_csv(DATA / "khong2025_tacrolimus_rct_source_data.csv")
    p = p[(p.Group == "PPM") & (p["Tac Range 8-10"] == "Y")]
    real = dict(far=p["%Days >2"].mean(), mean_ttl=p["Mean TTL"].mean(), add_below=p.ADDBelow.mean(),
                add_above=p.ADDAbove.mean(), far_sd=p["%Days >2"].std(), mean_ttl_sd=p["Mean TTL"].std())
    cv2sd = lambda cv: float(np.sqrt(np.log(1 + cv**2)))
    calib.OM_CL, calib.OM_V, calib.OM_KA = cv2sd(0.666), cv2sd(1.26), cv2sd(2.36)
    calib.START = 2                                       # chosen setting in dosing/calibration.ipynb
    sim = calib.simulate_linear(0.10, 0.0, 2000, p.LOHosp.clip(upper=30).to_numpy(), seed=7)
    keys = ["far", "mean_ttl", "add_below", "add_above", "far_sd", "mean_ttl_sd"]
    labels = ["% days far off (mean)", "trough (mean)", "deviation below (mean)",
              "deviation above (mean)", "% days far off (SD)", "trough (SD)"]
    ratio = [sim[k] / real[k] for k in keys]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    y = np.arange(len(keys))[::-1]
    for yi, r, k in zip(y, ratio, keys):
        held = k not in ("far", "mean_ttl", "add_below")
        ax.plot([1, r], [yi, yi], color="#c9c8c2", lw=2, zorder=1)
        ax.scatter(r, yi, s=60, color=C[1] if held else C[0], zorder=2, edgecolor=SURF, linewidth=2)
        ax.text(r + 0.04, yi, f"{r:.2f}", va="center", fontsize=8, color=INK)
    ax.axvline(1, color=MUTED, lw=1)
    ax.set_yticks(y, labels)
    ax.set_xlabel("synthetic / real (1 = exact match)")
    ax.scatter([], [], color=C[0], label="used for fitting")
    ax.scatter([], [], color=C[1], label="held out")
    ax.legend(frameon=False, loc="lower right")
    ax.set_title("Calibrated virtual patients vs the trial's linear arm (n = %d)" % len(p))
    save(fig, "calibration.png")


def khong_deviation():
    d = pd.read_csv(DATA / "khong2025_tacrolimus_rct_source_data.csv")
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    rng = np.random.default_rng(0)
    pos = 0
    ticks = []
    for col, side in (("ADDBelow", "below range"), ("ADDAbove", "above range")):
        for g, name, c in (("PPM", "CURATE.AI", C[0]), ("Ctrl", "standard care", C[1])):
            v = d.loc[d.Group == g, col].dropna().to_numpy()
            ax.boxplot(v, positions=[pos], widths=0.5, showfliers=False,
                       medianprops=dict(color=INK), boxprops=dict(color=MUTED), whiskerprops=dict(color=MUTED),
                       capprops=dict(color=MUTED))
            ax.scatter(pos + rng.uniform(-0.15, 0.15, len(v)), v, s=16, color=c, alpha=0.8, zorder=3)
            ticks.append((pos, f"{name}\n{side}"))
            pos += 1
        pos += 0.5
    ax.set_xticks([t[0] for t in ticks], [t[1] for t in ticks], fontsize=8)
    ax.set_ylabel("average daily deviation (ng/mL)")
    ax.set_title("Khong 2025 trial: less time below range, more time above")
    save(fig, "khong_deviation.png")


def decrease_vs_quadratic():
    xl = ROOT / "ext/decrease/210_Novel_Anticancer_combinations/192_Combinations_.xlsx"
    if not xl.exists():
        print("skip decrease_vs_quadratic.png: run scripts/fetch_open_data.sh first")
        return
    raw = pd.read_excel(xl)
    dec = pd.read_csv(DATA / "decrease_predictions_60_matrices.csv")
    I, J = np.meshgrid(np.arange(8), np.arange(8), indexing="ij")
    F = lambda i, j: np.stack([np.ones_like(i, float), i, j, i * j, i * i, j * j], -1).astype(float)
    MEAS = (I == 0) | (J == 0) | (I == J)
    TEST = ~MEAS
    R = {"quadratic": [], "DECREASE": [], "Bliss": []}
    for k, g in raw.groupby("PairIndex"):
        d = dec[dec.PairIndex == k]
        if d.empty:
            continue
        c1, c2 = np.sort(g.Conc1.unique()), np.sort(g.Conc2.unique())
        V = g.pivot_table(index="Conc1", columns="Conc2", values="Response").loc[c1, c2].to_numpy()
        P_dec = d.pivot_table(index="Conc1", columns="Conc2", values="pred").loc[c1, c2].to_numpy()
        b = np.linalg.lstsq(F(I[MEAS], J[MEAS]), V[MEAS], rcond=None)[0]
        P_quad = (F(I.ravel(), J.ravel()) @ b).reshape(8, 8)
        P_bliss = V[0, 0] * np.outer(V[:, 0] / V[0, 0], V[0, :] / V[0, 0])
        for name, P in (("quadratic", P_quad), ("DECREASE", P_dec), ("Bliss", P_bliss)):
            R[name].append(float(np.sqrt(((P - V)[TEST] ** 2).mean())))
    fig, ax = plt.subplots(figsize=(6, 3.8))
    rng = np.random.default_rng(0)
    for i, (name, v) in enumerate(R.items()):
        ax.boxplot(v, positions=[i], widths=0.5, showfliers=False, medianprops=dict(color=INK),
                   boxprops=dict(color=MUTED), whiskerprops=dict(color=MUTED), capprops=dict(color=MUTED))
        ax.scatter(i + rng.uniform(-0.15, 0.15, len(v)), v, s=14, color=C[i], alpha=0.7, zorder=3)
        ax.text(i + 0.3, np.median(v), f"median {np.median(v):.1f}", va="center", fontsize=8, color=INK)
    ax.set_xticks(range(3), list(R))
    ax.set_ylabel("RMSE on 42 unmeasured combinations\n(viability %)")
    ax.set_title(f"Same 22 measurements, three ways to predict the rest ({len(R['quadratic'])} matrices)")
    save(fig, "decrease_vs_quadratic.png")


def aml_funnel():
    a = pd.read_csv(DATA / "sahib2024_aml_concordance.csv").set_index("quantity").value
    steps = ["samples_collected", "qpop_runs", "passed_quality_check", "evaluated_vs_outcome", "headline_set"]
    names = ["samples collected", "QPOP runs", "passed quality check", "compared with outcome", "headline set"]
    n = [int(a[s]) for s in steps]
    tp, fn, tn, fp = (int(a[k]) for k in ("TP", "FN", "TN", "FP"))
    total = tp + fn + tn + fp
    acc, base = (tp + tn) / total, max(tp + fn, tn + fp) / total
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.4), gridspec_kw=dict(width_ratios=[1.6, 1]))
    y = np.arange(len(n))[::-1]
    ax1.barh(y, n, color=C[0], height=0.6)
    for yi, v in zip(y, n):
        ax1.text(v + 1, yi, str(v), va="center", fontsize=8, color=INK)
    ax1.set_yticks(y, names)
    ax1.set_xlabel("patients / samples")
    ax1.set_title("Sahib 2024 AML: sample funnel")
    ax1.grid(axis="y", visible=False)
    ax2.bar([0, 1], [100 * acc, 100 * base], color=[C[0], "#a3a29d"], width=0.6)
    for x, v in ((0, acc), (1, base)):
        ax2.text(x, 100 * v + 1.5, f"{100 * v:.0f}%", ha="center", fontsize=9, color=INK)
    ax2.set_xticks([0, 1], ["QPOP", "always predict\nmajority class"])
    ax2.set_ylim(0, 100)
    ax2.set_ylabel("accuracy (%)")
    ax2.set_title(f"Accuracy, {total} headline cases")
    ax2.grid(axis="x", visible=False)
    save(fig, "aml_funnel.png")


if __name__ == "__main__":
    for f in (tacrolimus_rules, calibration, khong_deviation, decrease_vs_quadratic, aml_funnel):
        f()
