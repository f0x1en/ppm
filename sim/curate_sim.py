"""How often does a quadratic fitted to 3 noisy dose-response points find the best dose?

True response: y(d) = 1 - ((d - D_STAR) / 15)^2, peak 1.0 at D_STAR.
Each trial: pick 3 distinct doses, add Gaussian noise, fit the exact quadratic
through the 3 points, take its best dose inside [LO, HI].
Success = chosen dose within TOL mg of D_STAR. Baseline = random dose in [LO, HI].
"""
import numpy as np

D_STAR, LO, HI, TOL = 15.0, 0.0, 30.0, 3.0
GRID = np.arange(5.0, 26.0, 1.0)  # doses that can be tested
N_TRIALS = 20000
rng = np.random.default_rng(0)


def truth(d):
    return 1 - ((d - D_STAR) / 15) ** 2


def best_dose(doses, y):
    a, b, _ = np.polyfit(doses, y, 2)
    if a < 0:  # concave: vertex, clipped to the allowed range
        return float(np.clip(-b / (2 * a), LO, HI))
    return LO if np.polyval([a, b, 0], LO) >= np.polyval([a, b, 0], HI) else HI


print(f"{'noise sd':>8} {'fit success':>12} {'random success':>15} {'mean regret':>12}")
for sd in (0.0, 0.05, 0.1, 0.2, 0.4):
    hits, regret = 0, 0.0
    for _ in range(N_TRIALS):
        doses = rng.choice(GRID, 3, replace=False)
        y = truth(doses) + rng.normal(0, sd, 3)
        d = best_dose(doses, y)
        hits += abs(d - D_STAR) <= TOL
        regret += 1 - truth(d)
    base = np.mean(np.abs(rng.uniform(LO, HI, N_TRIALS) - D_STAR) <= TOL)
    print(f"{sd:8.2f} {hits / N_TRIALS:12.1%} {base:15.1%} {regret / N_TRIALS:12.3f}")
