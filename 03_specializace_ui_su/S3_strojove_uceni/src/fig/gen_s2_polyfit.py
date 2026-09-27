#!/usr/bin/env python3
"""Generuje data pro obrázek podfit / dobrý fit / přefit (S3 §2).

Zašuměná data z funkce f(x) = sin(2*pi*x) na [0,1] + gaussovský šum,
proložená polynomy stupně 1 (podfit), 3 (dobrý fit) a 9 (přefit).

Výstup do .dat souborů (čtené v LaTeXu přes \addplot table):
  s2_poly_data.dat   -- N zašuměných trénovacích bodů (x  t)
  s2_poly_true.dat    -- pravá křivka sin(2*pi*x)
  s2_poly_deg1.dat    -- proložený polynom stupně 1
  s2_poly_deg3.dat    -- proložený polynom stupně 3
  s2_poly_deg9.dat    -- proložený polynom stupně 9

Předloha: NPFL129, lecture 02, sin_overfitting.svgz (Straka/Libovický).
FIXNÍ seed kvůli reprodukovatelnosti vyrenderovaného obrázku.
"""
import os
import numpy as np

SEED = 42
N = 11            # počet trénovacích bodů
NOISE_STD = 0.18  # směrodatná odchylka šumu

HERE = os.path.dirname(os.path.abspath(__file__))


def true_fn(x):
    return np.sin(2.0 * np.pi * x)


def main():
    rng = np.random.default_rng(SEED)
    x = np.linspace(0.0, 1.0, N)
    t = true_fn(x) + rng.normal(0.0, NOISE_STD, size=N)

    # hladké mřížky pro křivky
    xg = np.linspace(0.0, 1.0, 200)

    # zápis trénovacích bodů
    with open(os.path.join(HERE, "s2_poly_data.dat"), "w") as f:
        f.write("x t\n")
        for xi, ti in zip(x, t):
            f.write(f"{xi:.6f} {ti:.6f}\n")

    # pravá křivka
    with open(os.path.join(HERE, "s2_poly_true.dat"), "w") as f:
        f.write("x y\n")
        for xi, yi in zip(xg, true_fn(xg)):
            f.write(f"{xi:.6f} {yi:.6f}\n")

    # proložené polynomy (nejmenší čtverce na trénovacích bodech)
    for deg in (1, 3, 9):
        coef = np.polyfit(x, t, deg)
        yg = np.polyval(coef, xg)
        # ořež extrémní hodnoty u stupně 9, ať se graf nerozjede mimo osy
        yg = np.clip(yg, -2.2, 2.2)
        fname = os.path.join(HERE, f"s2_poly_deg{deg}.dat")
        with open(fname, "w") as f:
            f.write("x y\n")
            for xi, yi in zip(xg, yg):
                f.write(f"{xi:.6f} {yi:.6f}\n")

        # trénovací RMSE pro kontext (vytiskni do konzole)
        rmse = np.sqrt(np.mean((np.polyval(coef, x) - t) ** 2))
        print(f"deg {deg}: train RMSE = {rmse:.4f}")


if __name__ == "__main__":
    main()
