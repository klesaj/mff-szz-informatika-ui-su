"""
Numericka verifikace SZZ jaro 2026 c.29: ensemble vetsinovym hlasovanim 3 modelu.
M1,M2,M3 accuracy 0.70, 0.75, 0.80 na binarni klasifikaci.
Vetsinove hlasovani 3 modelu: vzorek spravne <=> aspon 2 ze 3 modelu spravne.

Chybove mnoziny: E_i = vzorky, ktere model M_i klasifikuje SPATNE.
|E1|=30, |E2|=25, |E3|=20 (na N=100). Ensemble je SPATNE na vzorku x
<=> x lezi aspon ve DVOU z E1,E2,E3.  err_ens = |{x: x ve >=2 mnozinach}|.
acc_ens = 1 - err_ens/N.

Rozlozeni N vzorku do 8 regionu Vennova diagramu (clenstvi v E1,E2,E3):
  a=onlyE1, b=onlyE2, c=onlyE3, d=E1&E2, e=E1&E3, f=E2&E3, g=E1&E2&E3, h=none.
Omezeni: a+d+e+g=30 ; b+d+f+g=25 ; c+e+f+g=20 ; soucet=100 ; vse >=0.
err_ens = d+e+f+g  (regiony s aspon dvema 1).

UPLNE (vycerpavajici) celociselne prohledani na N=100 -- ne jen nasobky 5.
"""
N = 100
s1, s2, s3 = 30, 25, 20

best = None   # nejvyssi acc_ens
worst = None  # nejnizsi acc_ens
best_arg = worst_arg = None

# vycerpavajici prochazeni vsech celociselnych rozlozeni Vennova diagramu
for g in range(0, s3 + 1):                 # trojny prunik <= min margin
    for d in range(0, s2 - g + 1):         # E1&E2
        for e in range(0, s3 - g + 1):     # E1&E3
            for f in range(0, s3 - g + 1): # E2&E3
                a = s1 - d - e - g
                b = s2 - d - f - g
                c = s3 - e - f - g
                if a < 0 or b < 0 or c < 0:
                    continue
                h = N - (a + b + c + d + e + f + g)
                if h < 0:
                    continue
                err = d + e + f + g
                acc = (N - err) / N
                arg = dict(E1only=a, E2only=b, E3only=c, E1E2=d, E1E3=e,
                           E2E3=f, E1E2E3=g, none=h)
                if best is None or acc > best:
                    best, best_arg = acc, arg
                if worst is None or acc < worst:
                    worst, worst_arg = acc, arg

print("=== SZZ jaro 2026 c.29: ensemble bounds (vetsinove hlasovani 3 modelu) ===")
print("acc: M1=0.70 M2=0.75 M3=0.80 ; |E1|,|E2|,|E3| = 30,25,20 (N=100)")
print(f"NEJLEPSI dosazitelna acc_ens = {best:.2f}  ({best*100:.0f}%)")
print(f"   rozlozeni = {best_arg}")
print(f"NEJHORSI dosazitelna acc_ens = {worst:.2f}  ({worst*100:.0f}%)")
print(f"   rozlozeni = {worst_arg}")
print(f"   (spojita dolni mez = 1 - (0.30+0.25+0.20)/2 = {1-(s1+s2+s3)/200:.3f})")
print()
print("Komentar k mezim:")
print(" * NEJLEPSI = 1.00: |E1|+|E2|+|E3| = 75 <= 100, lze rozlozit DISJUNKTNE -> err=0.")
print(" * E2 podmnozina E1            -> err >= |E2| = 25 -> acc <= 0.75.")
print(" * E2 c E1 a (E1\\E2) c E3      -> cela E1 ma >=2 chyby -> err >= 30 -> acc <= 0.70.")
print(" * NEJHORSI = 0.63: parove pruniky 17/12/8 (trojny 0) -> err = 37 -> acc = 0.63.")
print(" * Ensemble lepsi nez nejlepsi model (acc>0.80) <=> err_ens < 20 (malo korelovane chyby).")
