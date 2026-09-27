#!/usr/bin/env python3
"""Generuje hustoty testovych rozdeleni pro pgfplots (sekce S9 -- statisticke testy).
Math engine pgfplots nema gamma/erf, takze hustoty chi^2 a t pocita scipy a uklada
je do .dat (sloupce x  pdf). LaTeX je nacita pres \\addplot table a fillbetween
vysrafuje kriticky obor (zamitaci oblast) v ocasu.

Vystupy:
  s9_chi2_df4.dat  -- hustota chi^2_4, x in [0, 20]
  s9_t_df99.dat    -- hustota t_99,    x in [-5, 5]
"""
import os
from scipy import stats

here = os.path.dirname(__file__)


def dump(path, xs, pdf):
    with open(path, "w") as f:
        f.write("x p\n")
        for x in xs:
            f.write(f"{x:.5f} {pdf(x):.7f}\n")
    print(f"napsano: {path}  ({len(xs)} bodu)")


# --- chi^2 s df=4 (test dobre shody, K=5 kategorii -> df=K-1=4) ---
df_chi = 4
xs_chi = [i * 20.0 / 400 for i in range(0, 401)]  # 0 .. 20
dump(os.path.join(here, "s9_chi2_df4.dat"), xs_chi, lambda x: stats.chi2.pdf(x, df_chi))
crit_chi = stats.chi2.ppf(0.95, df_chi)
print(f"  chi^2_4 kriticka hodnota (alpha=0.05) = {crit_chi:.4f}  (napoveda 9.5)")
print(f"  pdf(crit) = {stats.chi2.pdf(crit_chi, df_chi):.5f}")

# --- t s df=99 (jednovyberovy t-test, n=100 -> df=n-1=99) ---
df_t = 99
xs_t = [(-5.0 + i * 10.0 / 400) for i in range(0, 401)]  # -5 .. 5
dump(os.path.join(here, "s9_t_df99.dat"), xs_t, lambda x: stats.t.pdf(x, df_t))
crit_t = stats.t.ppf(0.975, df_t)
print(f"  t_99 kriticka hodnota (alpha=0.05, oboustr.) = +-{crit_t:.4f}  (napoveda ~2)")
print(f"  pdf(crit) = {stats.t.pdf(crit_t, df_t):.5f}")
