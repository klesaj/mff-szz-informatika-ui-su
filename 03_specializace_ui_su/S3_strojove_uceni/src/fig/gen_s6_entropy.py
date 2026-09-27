#!/usr/bin/env python3
"""Generuje data binární entropie B(q) = -q log2 q - (1-q) log2(1-q)
pro pgfplots (sekce S6 -- rozhodovací stromy). Výstup: s6_entropy.dat
(sloupce q  B(q)), pokrytí q in (0,1) s ošetřeným okrajem.
"""
import math
import os

out = os.path.join(os.path.dirname(__file__), "s6_entropy.dat")


def B(q):
    if q <= 0.0 or q >= 1.0:
        return 0.0
    return -q * math.log2(q) - (1 - q) * math.log2(1 - q)


qs = [i / 400 for i in range(0, 401)]
with open(out, "w") as f:
    f.write("q B\n")
    for q in qs:
        f.write(f"{q:.5f} {B(q):.6f}\n")

print(f"napsano: {out}  ({len(qs)} bodu)")
print(f"  B(0.5) = {B(0.5):.4f} (max, ocekavano 1)")
print(f"  B(1/3) = {B(1/3):.4f}")
print(f"  B(2/6) = {B(2/6):.4f}")
