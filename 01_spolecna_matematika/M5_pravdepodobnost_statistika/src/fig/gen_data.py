"""Generátor simulačních dat pro pgfplots v M5/src/main.tex.

Spuštění (z adresáře M5/src/fig):
    python3 gen_data.py

Vygeneruje .dat soubory:
  - bin_pmf.dat, bin_cdf.dat        (PMF + CDF Bin(10, 0.4))
  - clv_hist_n{1,2,10,100}.dat      (CLV histogramy, Exp(1))
  - zvc_traj{1,2,3}.dat             (ZVČ trajektorie, fair coin)
  - ci_intervals_{in,out}.dat       (20 konfidenčních intervalů, rozdělené podle pokrytí μ)
  - phi_cdf.dat                     (Φ(x) tabulka pro pgfplots, x ∈ [-3.5, 3.5])

Použité seedy jsou fixní → reprodukovatelné.
"""

import numpy as np
from math import comb

from scipy.stats import norm

rng = np.random.default_rng(42)

# ============================================================
# Obr. 3 — CDF standardního normálního Φ(x) jako tabulka
# ============================================================
xs = np.linspace(-3.5, 3.5, 71)
with open("phi_cdf.dat", "w") as f:
    f.write("x phi\n")
    for x in xs:
        f.write(f"{x:.3f} {norm.cdf(x):.6f}\n")

# ============================================================
# Obr. 2 — PMF + CDF Bin(10, 0.4)
# ============================================================
n, p = 10, 0.4
pmf = np.array([comb(n, k) * p**k * (1 - p)**(n - k) for k in range(n + 1)])
cdf = np.cumsum(pmf)

with open("bin_pmf.dat", "w") as f:
    f.write("k pmf\n")
    for k, v in enumerate(pmf):
        f.write(f"{k} {v:.6f}\n")

with open("bin_cdf.dat", "w") as f:
    f.write("k cdf\n")
    for k, v in enumerate(cdf):
        f.write(f"{k} {v:.6f}\n")

print(f"Bin(10, 0.4): PMF součet = {pmf.sum():.6f} (mělo by být 1.0)")
print(f"Bin(10, 0.4): E[X] = {(np.arange(n+1) * pmf).sum():.4f} (= np = 4.0)")

# ============================================================
# Obr. 4 — CLV histogramy: průměr n nezávislých Exp(1)
# Standardizace: Z_n = (X̄_n − 1) · √n  (μ=1, σ=1 pro Exp(1))
# ============================================================
N_SAMPLES = 50000
for n_clv in [1, 2, 10, 100]:
    samples = rng.exponential(1.0, size=(N_SAMPLES, n_clv))
    means = samples.mean(axis=1)
    standardized = (means - 1.0) * np.sqrt(n_clv)
    # Histogram s pevnými biny od -3.5 do 3.5
    bins = np.linspace(-3.5, 3.5, 36)  # 35 binů (krok ~0.2)
    hist, edges = np.histogram(standardized, bins=bins, density=True)
    centers = 0.5 * (edges[:-1] + edges[1:])
    with open(f"clv_hist_n{n_clv}.dat", "w") as f:
        f.write("x density\n")
        for c, h in zip(centers, hist):
            f.write(f"{c:.4f} {h:.6f}\n")
    print(f"CLV n={n_clv}: prům.={means.mean():.3f}, sm.odch.={means.std():.4f} "
          f"(očekáv. 1/√n = {1/np.sqrt(n_clv):.4f})")

# ============================================================
# Obr. 5 — ZVČ trajektorie: hod férovou mincí, X̄_n při n=1..2000
# ============================================================
N_MAX = 2000
N_POINTS = 80  # vzorkujeme logaritmicky pro pgfplots
ns_log = np.unique(np.round(np.logspace(0, np.log10(N_MAX), N_POINTS)).astype(int))

for traj_idx in [1, 2, 3]:
    rng_traj = np.random.default_rng(100 + traj_idx)
    flips = rng_traj.binomial(1, 0.5, size=N_MAX)
    cum = np.cumsum(flips)
    means = cum / np.arange(1, N_MAX + 1)
    with open(f"zvc_traj{traj_idx}.dat", "w") as f:
        f.write("n xbar\n")
        for n_idx in ns_log:
            f.write(f"{n_idx} {means[n_idx-1]:.5f}\n")
    print(f"ZVČ traj{traj_idx}: X̄_2000 = {means[-1]:.4f}")

# ============================================================
# Obr. 7 — Konfidenční intervaly: 20 vzorků z N(μ=10, σ=2), n=25
# CI = X̄_n ± 1.96 · σ / √n  (95%, σ známé)
# ============================================================
mu_true, sigma = 10.0, 2.0
n_sample = 25
z = 1.96
hw = z * sigma / np.sqrt(n_sample)  # poloviční šířka

rng_ci = np.random.default_rng(13)
n_intervals = 20
xbars = rng_ci.normal(mu_true, sigma / np.sqrt(n_sample), size=n_intervals)

f_in = open("ci_intervals_in.dat", "w")
f_out = open("ci_intervals_out.dat", "w")
for fh in (f_in, f_out):
    fh.write("idx xbar lower upper\n")
n_contains = 0
for i, xb in enumerate(xbars, start=1):
    lo, up = xb - hw, xb + hw
    contains = lo <= mu_true <= up
    target = f_in if contains else f_out
    target.write(f"{i} {xb:.4f} {lo:.4f} {up:.4f}\n")
    if contains:
        n_contains += 1
f_in.close()
f_out.close()
print(f"CI: {n_contains}/{n_intervals} intervalů obsahuje μ=10 "
      f"(očekáváme cca 19/20)")
print(f"CI: poloviční šířka = ±{hw:.4f}")
