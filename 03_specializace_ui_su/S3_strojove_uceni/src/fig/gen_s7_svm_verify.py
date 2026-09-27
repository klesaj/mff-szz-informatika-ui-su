#!/usr/bin/env python3
"""Numerická verifikace SZZ léto 2024 č. 30 (SVM) pro sekci S3 §7.

Třída A (křížky, t=+1): (1,1),(2,2),(2,0)
Třída B (kolečka, t=-1): (0,0),(1,0),(0,1)

Zjistí: skutečný separátor (w,b), podpůrné vektory, margin.
Ověří efekt přidání vzdáleného bodu (3,3) do A.
Demonstruje, proč lineární SVM selže na soustředných kruzích a RBF pomůže.
"""
import numpy as np
from sklearn.svm import SVC

A = np.array([[1, 1], [2, 2], [2, 0]], dtype=float)   # t = +1
B = np.array([[0, 0], [1, 0], [0, 1]], dtype=float)   # t = -1
X = np.vstack([A, B])
y = np.array([1, 1, 1, -1, -1, -1])

clf = SVC(kernel="linear", C=1e6)
clf.fit(X, y)
w = clf.coef_[0]
b = clf.intercept_[0]
print("=== SZZ léto 2024 č. 30 ===")
print(f"w = {w}, b = {b:.4f}")
# normalize for readability
print(f"separátor: {w[0]:.4f}*x1 + {w[1]:.4f}*x2 + {b:.4f} = 0")
nw = np.linalg.norm(w)
print(f"||w|| = {nw:.4f}   margin (2/||w||) = {2/nw:.4f}")
print("podpůrné vektory (indexy):", clf.support_)
print("podpůrné vektory (body):")
for i in clf.support_:
    print(f"   {X[i]}  t={y[i]}  funkční hodnota y={(w@X[i]+b):+.4f}")
print("dual coefs (a_i*t_i):", clf.dual_coef_)

# decision values for all points
print("\nfunkční hodnoty y(x) pro všechny body (mají být >=+1 pro A, <=-1 pro B):")
for xi, ti in zip(X, y):
    print(f"   {xi} t={ti:+d}  y={(w@xi+b):+.4f}  t*y={ti*(w@xi+b):+.4f}")

# Try a clean simple separator candidate x1 + x2 = 1.5 (i.e. w=(1,1), b=-1.5)?
# Check the analytic max-margin guess: separator x2 = -x1 + 1.5 -> w ~ (1,1), b=-1.5
print("\n--- ručně odhadnutý separátor w=(1,1), b=-1.5 (přímka x1+x2=1.5) ---")
for xi, ti in zip(X, y):
    val = xi[0] + xi[1] - 1.5
    print(f"   {xi} t={ti:+d}  x1+x2-1.5={val:+.3f}  t*val={ti*val:+.3f}")

# === Effect of adding (3,3) to A ===
print("\n=== Přidání bodu (3,3) do třídy A ===")
X2 = np.vstack([X, [3, 3]])
y2 = np.append(y, 1)
clf2 = SVC(kernel="linear", C=1e6)
clf2.fit(X2, y2)
w2 = clf2.coef_[0]
b2 = clf2.intercept_[0]
print(f"w2 = {w2}, b2 = {b2:.4f}")
print(f"separátor: {w2[0]:.4f}*x1 + {w2[1]:.4f}*x2 + {b2:.4f} = 0")
print("podpůrné vektory po přidání:", X2[clf2.support_])
print(f"je (3,3) podpůrný vektor? {'ANO' if (X2[clf2.support_]==[3,3]).all(axis=1).any() else 'NE'}")
same = np.allclose(w / np.linalg.norm(w), w2 / np.linalg.norm(w2), atol=1e-3) and \
       np.isclose(b / np.linalg.norm(w), b2 / np.linalg.norm(w2), atol=1e-3)
print(f"separátor stejný (po normalizaci)? {'ANO' if same else 'NE'}")

# === RBF demo: concentric circles ===
print("\n=== Lineární vs RBF na soustředných kruzích ===")
rng = np.random.default_rng(0)
n = 60
r_in = 1.0 + 0.15 * rng.standard_normal(n)
th_in = rng.uniform(0, 2 * np.pi, n)
inner = np.c_[r_in * np.cos(th_in), r_in * np.sin(th_in)]
r_out = 3.0 + 0.2 * rng.standard_normal(n)
th_out = rng.uniform(0, 2 * np.pi, n)
outer = np.c_[r_out * np.cos(th_out), r_out * np.sin(th_out)]
Xc = np.vstack([inner, outer])
yc = np.array([1] * n + [-1] * n)
lin = SVC(kernel="linear", C=1.0).fit(Xc, yc)
rbf = SVC(kernel="rbf", C=1.0, gamma=0.5).fit(Xc, yc)
print(f"lineární SVM accuracy na kruzích: {lin.score(Xc, yc):.3f}")
print(f"RBF SVM accuracy na kruzích:      {rbf.score(Xc, yc):.3f}")
