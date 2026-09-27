#!/usr/bin/env python3
# Numerická verifikace SZZ příkladů okruhu S1 (Základy UI).
# Ground truth pro výklad: SZZ otázky bez oficiálního náčrtu řešení MUSÍ být ověřeny.
# Spuštění: python3 src/fig/verify_szz.py
import itertools, heapq, math

def hr(t): print("\n" + "="*70 + f"\n{t}\n" + "="*70)

# ---------------------------------------------------------------------------
hr("1) 8-puzzle (SZZ jaro 2024) -- heuristiky + řešitelnost")
start=(2,8,3,1,6,4,7,0,5); goal=(1,2,3,4,5,6,7,8,0)
gp={v:(i//3,i%3) for i,v in enumerate(goal)}
h1=sum(1 for i,v in enumerate(start) if v and v!=goal[i])
h2=sum(abs(i//3-gp[v][0])+abs(i%3-gp[v][1]) for i,v in enumerate(start) if v)
inv=lambda s:[v for v in s if v]
def invcount(s):
    a=inv(s); return sum(1 for i in range(len(a)) for j in range(i+1,len(a)) if a[i]>a[j])
print(f"h1 (misplaced) = {h1}   h2 (Manhattan) = {h2}")
print(f"inverze start = {invcount(start)} (liché), cíl = {invcount(goal)} (sudé) -> NEŘEŠITELNÉ")

# ---------------------------------------------------------------------------
hr("2) AC-3 (SZZ jaro 2026) -- hranová konzistence")
# proměnné A,B,C,D; domény; binární podmínky
D={'A':{1},'B':{1,2,3},'C':{1,2,3},'D':{1,2,3}}
# podmínky jako (X,Y,relace) -- relace(x,y) True pokud x,y konzistentní
cons=[('C','D',lambda x,y:x+y==4),('D','C',lambda x,y:y+x==4),
      ('A','B',lambda x,y:x+y<=3),('B','A',lambda x,y:y+x<=3),
      ('B','C',lambda x,y:x+y>=4),('C','B',lambda x,y:y+x>=4)]
def revise(X,Y,rel):
    removed=False
    for x in set(D[X]):
        if not any(rel(x,y) for y in D[Y]):
            D[X].discard(x); removed=True
    return removed
queue=list(cons)
while queue:
    X,Y,rel=queue.pop(0)
    if revise(X,Y,rel):
        for (P,Q,r) in cons:
            if Q==X and P!=Y: queue.append((P,Q,r))
print("výsledné domény:",{k:sorted(v) for k,v in D.items()})
print("náčrt SZZ: A={1}, B={1,2}, C={2,3}, D={1,2}")

# ---------------------------------------------------------------------------
hr("3) Bayesovská síť P1->P2->{P3,P4} (SZZ léto 2024)")
# P(P1=T)=0.4 ; P(P2=T|P1)= T:0.8,F:0.5 ; P(P3=T|P2)= T:0.2,F:0.3 ; P(P4=T|P2)= T:0.8,F:0.5
def p1(v): return 0.4 if v else 0.6
def p2(v,P1): t=0.8 if P1 else 0.5; return t if v else 1-t
def p3(v,P2): t=0.2 if P2 else 0.3; return t if v else 1-t
def p4(v,P2): t=0.8 if P2 else 0.5; return t if v else 1-t
# query P(P1=T | P3=F, P4=T): vyčíslíme přes P2
num={}  # P1 -> joint with P3=F,P4=T
for P1 in (True,False):
    s=0.0
    for P2 in (True,False):
        s+=p1(P1)*p2(P2,P1)*p3(False,P2)*p4(True,P2)
    num[P1]=s
Z=num[True]+num[False]
print(f"P(P1=T, P3=F,P4=T)={num[True]:.5f}  P(P1=F,...)={num[False]:.5f}")
print(f"P(P1=T | P3=F,P4=T) = {num[True]/Z:.5f}")

# ---------------------------------------------------------------------------
hr("4) HMM deštník (SZZ léto 2023) -- filtrace 2 dny, P(X2=P|E1=D,E2=D)")
# stavy P,S; transition; sensor; prior X0
T={('P','P'):0.7,('P','S'):0.3,('S','P'):0.3,('S','S'):0.7}  # (prev,cur)
O={('D','P'):0.9,('N','P'):0.1,('D','S'):0.2,('N','S'):0.8}   # (obs,state)
f={'P':0.5,'S':0.5}   # f_{1:0}=P(X0)
def step(f,obs):
    pred={c:sum(T[(p,c)]*f[p] for p in ('P','S')) for c in ('P','S')}
    upd={c:O[(obs,c)]*pred[c] for c in ('P','S')}
    Z=sum(upd.values()); return {c:upd[c]/Z for c in upd}
f1=step(f,'D'); f2=step(f1,'D')
print(f"f1 (po E1=D): P={f1['P']:.4f}, S={f1['S']:.4f}")
print(f"f2 (po E2=D): P={f2['P']:.4f}, S={f2['S']:.4f}  <- P(X2=P|D,D)")

# ---------------------------------------------------------------------------
hr("5) MDP (SZZ léto 2025) -- vyhodnocení strategie B->C, C->D, D->F, gamma=0.9")
import numpy as np
g=0.9; R={'B':-3,'C':1,'D':1,'E':5,'F':6}
UE,UF=R['E'],R['F']   # terminální užitky = odměna
# U(B)=R(B)+g[0.8 U(C)+0.2 U(D)]
# U(C)=R(C)+g[0.8 U(D)+0.2 U(E)]
# U(D)=R(D)+g[0.8 U(F)+0.2 U(B)]
# řešíme lineární systém pro [U(B),U(C),U(D)]
A=np.array([[1,-g*0.8,-g*0.2],[0,1,-g*0.8],[-g*0.2,0,1]],float)
b=np.array([R['B'], R['C']+g*0.2*UE, R['D']+g*0.8*UF],float)
UB,UC,UD=np.linalg.solve(A,b)
print(f"U(B)={UB:.4f}  U(C)={UC:.4f}  U(D)={UD:.4f}  U(E)={UE}  U(F)={UF}")

# ---------------------------------------------------------------------------
hr("6) Bayesovské učení -- jablka (SZZ jaro 2025)")
prior={'A':1/2,'B':1/3,'C':1/6}
# MLE rozdělení velikostí (9,10,11) z četností
counts={'A':[5,4,1],'B':[9,8,3],'C':[1,8,1]}
Pml={h:[c/sum(cs) for c in cs] for h,cs in counts.items()}
print("MLE rozdělení:",{h:[round(x,3) for x in v] for h,v in Pml.items()})
# data = pozorování 10cm a 11cm (indexy 1 a 2)
like={h:Pml[h][1]*Pml[h][2] for h in prior}
print("P(data|h):",{h:round(v,4) for h,v in like.items()}," -> MLE hypotéza:",max(like,key=like.get))
post={h:prior[h]*like[h] for h in prior}; Zp=sum(post.values())
post={h:post[h]/Zp for h in post}
print("posterior P(h|data):",{h:round(v,4) for h,v in post.items()})
pred10=sum(Pml[h][1]*post[h] for h in prior)
print(f"Bayesovsky optimální predikce P(příští=10cm) = {pred10:.4f}")

# ---------------------------------------------------------------------------
hr("7) Rozhodovací strom -- entropie a information gain (restaurace AIMA)")
def B(q):
    if q in (0,1): return 0.0
    return -(q*math.log2(q)+(1-q)*math.log2(1-q))
# 12 příkladů, 6+/6-; Patrons: None(0+,2-), Some(4+,0-), Full(2+,4-)
groups=[(0,2),(4,0),(2,4)]
rem=sum((p+n)/12*B(p/(p+n)) if p+n else 0 for p,n in groups)
gain=B(6/12)-rem
print(f"B(1/2)={B(0.5):.3f}  Remainder(Patrons)={rem:.4f}  Gain(Patrons)={gain:.4f}")
# Type: French(1+,1-),Italian(1+,1-),Thai(2+,2-),Burger(2+,2-) -> Gain=0
gt=[(1,1),(1,1),(2,2),(2,2)]
remt=sum((p+n)/12*B(p/(p+n)) for p,n in gt)
print(f"Gain(Type)={B(6/12)-remt:.4f} (očekáváno 0)")

# ---------------------------------------------------------------------------
hr("8) Jednotahové hry (SZZ podzim 2025) -- dominantní str., Nash, Pareto")
games={
 1:{('L','L'):(10,5),('L','R'):(7,8),('R','L'):(0,6),('R','R'):(15,7)},
 2:{('L','L'):(100,100),('L','R'):(0,0),('R','L'):(0,0),('R','R'):(50,50)},
 3:{('L','L'):(20,20),('L','R'):(0,40),('R','L'):(40,0),('R','R'):(10,10)},
}
acts=['L','R']
for gi,M in games.items():
    # dominantní strategie A: existuje a t.ž. pro všechny b je A(a,b) >= A(a',b) a někde >
    def dominant(player):
        idx=0 if player=='A' else 1
        best=[]
        for a in acts:
            other=[x for x in acts if x!=a][0]
            ge=all((M[(a,b)] if player=='A' else M[(b,a)])[idx] >=
                    (M[(other,b)] if player=='A' else M[(b,other)])[idx] for b in acts)
            gt_=any((M[(a,b)] if player=='A' else M[(b,a)])[idx] >
                    (M[(other,b)] if player=='A' else M[(b,other)])[idx] for b in acts)
            if ge and gt_: best.append(a)
        return best
    # Nash (pure)
    nash=[]
    for a in acts:
        for b in acts:
            aBest=all(M[(a,b)][0]>=M[(a2,b)][0] for a2 in acts)
            bBest=all(M[(a,b)][1]>=M[(a,b2)][1] for b2 in acts)
            if aBest and bBest: nash.append(((a,b),M[(a,b)]))
    # Pareto optimální výsledky
    outs=list(M.values()); pareto=[]
    for o in M.values():
        dominated=any((o2[0]>=o[0] and o2[1]>=o[1] and o2!=o and (o2[0]>o[0] or o2[1]>o[1])) for o2 in outs)
        if not dominated and o not in [p for p in pareto]: pareto.append(o)
    print(f"Hra {gi}: dom(A)={dominant('A')} dom(B)={dominant('B')} "
          f"Nash={nash} Pareto={sorted(set(pareto))}")

print("\nHOTOVO.")
