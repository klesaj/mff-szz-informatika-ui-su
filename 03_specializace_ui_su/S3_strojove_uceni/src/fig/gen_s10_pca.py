#!/usr/bin/env python3
"""Generuje data pro VYKLADOVY PCA obrazek v s10_uceni_bez_ucitele.tex.

Protahly 2D Gaussovsky mrak (korelovany), centrovany, + smer 1. a 2. hlavni
komponenty (vlastni vektory kovariancni matice, skalovane sqrt(vl. cislo) pro
vizualni delku ~ smerodatna odchylka). FIXNI seed kvuli reprodukovatelnosti.

Vystup (do src/fig/, latexmk cte relativne k src/):
  s10_pca_cloud.dat   -- sloupce: x y     (centrovany mrak bodu)
  s10_pca_axes.dat    -- radky:  x y dx dy len  (pocatek a smer hl. komponent)
"""
import numpy as np

np.random.seed(11)
N = 120
# Korelovany Gauss: protahly podel smeru (1, 0.55), uzky kolmo.
mean = np.array([0.0, 0.0])
# kovariancni matice s vyraznou hlavni osou
ang = np.radians(28.0)
R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
S = R @ np.diag([1.6**2, 0.45**2]) @ R.T
X = np.random.multivariate_normal(mean, S, size=N)
X = X - X.mean(axis=0)   # centrovani (PCA krok 1)

# Kovariancni matice dat + vlastni rozklad (PCA krok 2-3).
cov = np.cov(X.T)
w, V = np.linalg.eigh(cov)
order = w.argsort()[::-1]
w = w[order]
V = V[:, order]
# Orientuj 1. komponentu do prvniho kvadrantu (kosmeticke).
if V[0, 0] < 0:
    V[:, 0] = -V[:, 0]
if V[1, 1] < 0:
    V[:, 1] = -V[:, 1]

with open("s10_pca_cloud.dat", "w") as f:
    f.write("x y\n")
    for x, y in X:
        f.write(f"{x:.4f} {y:.4f}\n")

# Delka sipky ~ 2*smerodatna odchylka v dane komponente (pro nazornost).
with open("s10_pca_axes.dat", "w") as f:
    f.write("x y dx dy len\n")
    for k in range(2):
        L = 2.0 * np.sqrt(w[k])
        dx, dy = V[0, k] * L, V[1, k] * L
        f.write(f"0 0 {dx:.4f} {dy:.4f} {np.sqrt(w[k]):.4f}\n")

print("eigvals (rozptyly):", w, " pomer PC1:", w[0] / w.sum())
print("PC1 smer:", V[:, 0], " PC2 smer:", V[:, 1])
print("napsano s10_pca_cloud.dat, s10_pca_axes.dat")
