"""Calibrate the virtual-patient noise to the CURATE.AI trial's linear arm (Khong 2025, 27 patients).

Truth model: Bai et al. 2024 (as in scripts/sim_tacrolimus.R). Two knobs are calibrated:
  PROP  - proportional residual (measurement + unexplained) SD of the trough
  IOV   - SD of day-to-day random variation in log clearance (inter-occasion variability)
Fitted on 2 trial statistics (mean % days far off target, mean trough); checked on 4 others it never saw.
"""
import numpy as np
import pandas as pd

CL, V, KA = 37.6, 1710.0, 0.352
OM_CL, OM_V, OM_KA, COV = 0.666, 1.26, 2.36, 0.226
ADD = 0.355
TAU, TARGET, LO, HI, START = 12.0, 9.0, 8.0, 10.0, 4.0
FIT = ["far", "mean_ttl"]
CHECK = ["far_sd", "mean_ttl_sd", "add_below", "add_above"]


def trough(doses, cl_by_day, v, ka, day):
    """Trough before the morning dose of `day` (1-based); clearance of each dosing day used for that day's doses."""
    t = day * 24.0
    ta = np.arange(2 * len(doses)) * TAU
    amt = np.repeat(doses, 2) * 1000.0
    k = np.repeat(cl_by_day[: len(doses)], 2) / v
    dt = t - ta
    m = dt > 0
    return float(np.sum(amt[m] * ka / (v * (ka - k[m])) * (np.exp(-k[m] * dt[m]) - np.exp(-ka * dt[m]))))


def real_targets(path="../data/khong2025_tacrolimus_rct_source_data.csv"):
    p = pd.read_csv(path)
    p = p[p.Group == "PPM"]
    return dict(far=p["%Days >2"].mean(), mean_ttl=p["Mean TTL"].mean(), far_sd=p["%Days >2"].std(),
                mean_ttl_sd=p["Mean TTL"].std(), add_below=p.ADDBelow.mean(), add_above=p.ADDAbove.mean()), p


def simulate_linear(prop, iov, n, stays, seed=0):
    """Linear (proportional) rule from day 4, as in the trial. Returns per-patient summaries."""
    rng = np.random.default_rng(seed)
    eta = rng.multivariate_normal([0, 0], [[OM_CL**2, COV], [COV, OM_V**2]], n)
    out = []
    for i in range(n):
        days = int(rng.choice(stays))
        cl = CL * np.exp(eta[i, 0] + rng.normal(0, iov, days))
        v, ka = V * np.exp(eta[i, 1]), KA * np.exp(rng.normal(0, OM_KA))
        D, O = [], []
        for d in range(1, days + 1):
            dose = START if d <= 3 else D[-1] * TARGET / O[-1]
            D.append(min(max(round(dose * 2) / 2, 0.5), 10.0))
            tr = trough(np.array(D), cl, v, ka, d)
            O.append(max(tr * (1 + prop * rng.normal()) + ADD * rng.normal(), 0.1))
        o = np.array(O[3:]) if days > 3 else np.array(O)
        dev = np.maximum(LO - o, o - HI)
        out.append(dict(far=np.mean(dev > 2), mean_ttl=o.mean(),
                        add_below=np.mean(np.clip(LO - o, 0, None)), add_above=np.mean(np.clip(o - HI, 0, None))))
    s = pd.DataFrame(out)
    return dict(far=s.far.mean(), mean_ttl=s.mean_ttl.mean(), far_sd=s.far.std(), mean_ttl_sd=s.mean_ttl.std(),
                add_below=s.add_below.mean(), add_above=s.add_above.mean())
