#!/usr/bin/env python3
"""Generuje data pro obrázky k-NN (S3 §3).

Dva výstupy:

1) Schematická dvě třídy pro VÝKLADOVÝ obrázek vlivu k na hranici
   (panely "malé k" vs "velké k"). Tady stačí ručně volené body
   v TikZ, takže tento skript je generuje jen pro kontrolu a tisk
   souřadnic do konzole, ne do .dat (panely jsou v TikZ schematicky).

2) Rekonstrukce dat SZZ jaro 2025 č. 28 pro ŘEŠENÝ PŘÍKLAD:
   dvě třídy (o = trida 1 vlevo nahore, x = trida 2 vpravo dole),
   dotaz q = (3, 2), k = 3. Skript spocita 3 nejblizsi sousedy
   eukleidovskou metrikou a vytiskne je (numericka kontrola toho,
   ze klasifikace dopadne na "o", jak uvadi oficialni nacrt reseni,
   a ze pro k = 7 se zmeni na "x").

Predloha bodu: priklady/src/fig/knn.png (orazly z PDF jaro 2025).
Souradnice odecteny z obrazku; jde o verny, ne pixel-presny prepis.
FIXNI seed neni potreba (body jsou zadane rucne).

Pozn. (oprava 26. 9. 2026): okoli dotazu (3,2) je preodecteno z knn.png
(teziste znacek, mrizka x: 311,5 + 117*x px, y: 731,5 - 117*y px). Drivejsi
rekonstrukce mela tri krouzky u dotazu posunute o +0,15..0,19 v x a jeden krizek
umele posunuty, aby 3-NN byly tri krouzky; to neodpovidalo obrazku. Skutecne
poradi: o 0,383, o 0,398, x 0,577, x 0,581, o 0,669 ~ x 0,670, x 0,699, x 0,89.
k=3 -> o (2:1), k=5 na hrane (5. a 6. soused v ramci presnosti stejne daleko),
k=7 -> x (3:4). Vzdalenejsi body zustavaji jako puvodni pribliny odecet.
"""
import numpy as np

# --- Data SZZ jaro 2025 c. 28 (odecteno z knn.png) ---
# Trida "o" (krouzky) -- vlevo nahore.
O = np.array([
    (-1.6, 3.87), (-0.7, 4.83), (-0.55, 3.73), (-0.6, 3.22),
    (-0.3, 4.05), (-0.25, 4.08), (-0.1, 4.15), (0.05, 4.15),
    (0.1, 3.40), (0.15, 2.95), (0.3, 3.45), (0.35, 3.10),
    (0.4, 3.10), (0.55, 4.30), (0.6, 3.12), (0.65, 2.50),
    (0.9, 3.68), (1.0, 4.73), (1.05, 3.62), (1.1, 3.68),
    (1.15, 4.48), (1.2, 3.65), (1.25, 4.10), (1.3, 3.08),
    (1.35, 2.87), (1.4, 3.90), (1.55, 3.63), (1.7, 3.25),
    (1.75, 2.82), (2.0, 2.45), (2.2, 4.27), (2.35, 3.25),
    (2.45, 4.80), (2.5, 4.47), (2.55, 3.22), (2.84, 2.65),
    (2.86, 2.37), (3.25, 2.29), (0.15, 2.32), (0.25, 2.10),
    (0.25, 1.90),
])
# Trida "x" (krizky) -- vpravo dole.
X = np.array([
    (0.6, 1.13), (0.65, 1.45), (0.7, 0.50), (0.75, 0.50),
    (0.9, 2.27), (0.95, 0.87), (1.0, 1.35), (1.1, 1.67),
    (1.2, 0.78), (1.25, 0.75), (1.3, 2.22), (1.3, 0.25),
    (1.35, 1.97), (1.35, 1.27), (1.4, 2.27), (1.45, 0.68),
    (1.5, 0.27), (1.6, 1.43), (1.7, 2.22), (1.75, -0.20),
    (2.0, 2.10), (2.0, 0.33), (2.05, -0.05), (2.1, 1.30),
    (2.35, 1.82), (2.68, 1.52), (2.6, 0.67), (2.81, 1.46),
    (2.7, 0.32), (2.95, 1.12), (3.0, 0.90), (3.0, 0.70),
    (3.05, 1.07), (3.16, 1.32), (3.2, 0.0), (3.2, 1.08),
    (2.45, 0.0), (2.7, -0.38), (1.35, -0.85), (1.35, -0.33),
    (3.95, 1.93), (4.1, 1.83), (4.2, 1.50), (4.5, 1.53),
])

Q = np.array([3.0, 2.0])


def knn(q, k):
    pts = np.vstack([O, X])
    lab = np.array(["o"] * len(O) + ["x"] * len(X))
    d = np.linalg.norm(pts - q, axis=1)
    idx = np.argsort(d)[:k]
    return pts[idx], lab[idx], d[idx]


def tikz_coords(pts):
    """Vytiskne souradnice ve formatu pro \\foreach v TikZ."""
    return ",".join(f"({p[0]:g},{p[1]:g})" for p in pts)


def main():
    for k in (1, 3, 5, 7, 9):
        pts, lab, d = knn(Q, k)
        votes = {c: int((lab == c).sum()) for c in ("o", "x")}
        pred = max(votes, key=votes.get)
        print(f"k={k:2d}: hlasy o={votes['o']} x={votes['x']} -> {pred}"
              f"   (nejblizsi vzdal.: {', '.join(f'{x:.2f}' for x in d)})")
    # detail pro k=3 a 1. krizek (kontrola poradi sousedu)
    pts, lab, d = knn(Q, 3)
    print("\nk=3 tri nejblizsi sousede k q=(3,2):")
    for p, l, dist in zip(pts, lab, d):
        print(f"  ({p[0]:.2f},{p[1]:.2f})  trida={l}  d={dist:.3f}")
    dx = np.linalg.norm(X - Q, axis=1)
    j = int(np.argmin(dx))
    print(f"nejblizsi krizek: ({X[j][0]:.2f},{X[j][1]:.2f}) d={dx[j]:.3f}"
          f"  (3. soused d={d[2]:.3f})")

    # --- TikZ souradnice (pro primy prepis do s3_knn.tex) ---
    print("\n% --- TikZ \\foreach souradnice (verna data SZZ jaro 2025 c.28) ---")
    print("% krouzky (trida o):")
    print(tikz_coords(O))
    print("% krizky (trida x):")
    print(tikz_coords(X))


if __name__ == "__main__":
    main()
