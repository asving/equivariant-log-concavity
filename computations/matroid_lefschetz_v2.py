"""
v2: bigger matroids + kernel extraction at d=1 + generic-l variant + L^d vs Delta_d test.
"""
from __future__ import annotations
from itertools import combinations
import sympy as sp
from sympy import Rational, Matrix, zeros, eye

# ------------------- Matroid -------------------

class Matroid:
    def __init__(self, n, independents):
        self.n = n
        self.indep = set(frozenset(s) for s in independents)
        self.by_size = {}
        for S in self.indep:
            self.by_size.setdefault(len(S), []).append(S)
        for d in self.by_size:
            self.by_size[d].sort(key=lambda s: sorted(s))
        self.rank = max(self.by_size) if self.by_size else 0
        self.f = tuple(len(self.by_size.get(d, [])) for d in range(self.rank + 1))

    def is_indep(self, S): return frozenset(S) in self.indep

    @classmethod
    def uniform(cls, r, n):
        indep = []
        for k in range(r+1):
            for c in combinations(range(n), k): indep.append(frozenset(c))
        return cls(n, indep)

    @classmethod
    def from_bases(cls, n, bases):
        bases = [frozenset(b) for b in bases]
        indep = set()
        for B in bases:
            for k in range(len(B)+1):
                for c in combinations(B, k): indep.add(frozenset(c))
        return cls(n, indep)

# ------------------- Basis & L matrix -------------------

def basis_in_external_degree(M, e):
    out = []
    for m in range(M.rank+1):
        sT = m - e
        if sT < 0 or sT > M.rank: continue
        for S in M.by_size.get(m, []):
            for T in M.by_size.get(sT, []):
                out.append((S, T))
    return out

def L_matrix(M, e, coeffs=None):
    """coeffs: tuple (c_1,...,c_n) — operator becomes sum_i c_i * (x_i op x_i).
    Default: all-ones (the diagonal L)."""
    if coeffs is None: coeffs = [1]*M.n
    src = basis_in_external_degree(M, e)
    tgt = basis_in_external_degree(M, e+2)
    tgt_idx = {st: i for i, st in enumerate(tgt)}
    A = zeros(len(tgt), len(src))
    for j, (S, T) in enumerate(src):
        for i in T:
            if i in S: continue
            Snew = S | {i}
            if not M.is_indep(Snew): continue
            Tnew = T - {i}
            row = tgt_idx[(frozenset(Snew), frozenset(Tnew))]
            A[row, j] += coeffs[i]
    return A, src, tgt

def L_pow(M, e, p, coeffs=None):
    A, src, tgt = L_matrix(M, e, coeffs)
    for k in range(1, p):
        B, _, _ = L_matrix(M, e + 2*k, coeffs)
        A = B * A
    return A

# ------------------- Reporting -------------------

def report(M, label, do_kernels=False):
    rk = M.rank
    print(f"\n=== {label}  n={M.n}, rank={rk}, f={M.f} ===")
    for d in range(1, rk+1):
        e = -d
        A, src, tgt = L_matrix(M, e)
        r = A.rank()
        ds, dt = A.shape[1], A.shape[0]
        msg = f"  d={d}: L: S_{e}({ds})->S_{e+2}({dt}) rank={r}"
        msg += "  INJ" if r == ds else f"  ker={ds-r}"
        msg += "  SURJ" if r == dt else f"  coker={dt-r}"
        print(msg)
        # L^d -> S_d
        Ap = A.copy()
        for k in range(1, d):
            B, _, _ = L_matrix(M, e + 2*k)
            Ap = B * Ap
        rp = Ap.rank()
        dsp, dtp = Ap.shape[1], Ap.shape[0]
        flag = "ISO" if rp == dsp == dtp else ("INJ-only" if rp == dsp else ("SURJ-only" if rp == dtp else "NEITHER"))
        print(f"        L^{d}: S_{-d}({dsp})->S_{d}({dtp}) rank={rp} [{flag}]")

        if do_kernels and r < ds:
            ker = A.nullspace()
            print(f"        ker basis size = {len(ker)}")
            # print supports
            for v in ker[:6]:
                supp = []
                for i, val in enumerate(v):
                    if val != 0:
                        S, T = src[i]
                        supp.append(f"{val}*(x_{sorted(S)}⊗y_{sorted(T)})")
                print(f"          ker elt: " + " + ".join(supp))

# ------------------- Specific matroids -------------------

def M_K4():
    edges = {0:(1,2),1:(1,3),2:(1,4),3:(2,3),4:(2,4),5:(3,4)}
    def is_ST(B):
        if len(B)!=3: return False
        p = {v:v for v in range(1,5)}
        def f(x):
            while p[x]!=x: p[x]=p[p[x]]; x=p[x]
            return x
        for e in B:
            u,v=edges[e]; ru,rv=f(u),f(v)
            if ru==rv: return False
            p[ru]=rv
        return True
    return Matroid.from_bases(6, [b for b in combinations(range(6),3) if is_ST(b)])

def Fano():
    lines = [frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
    bases = [b for b in combinations(range(7),3) if frozenset(b) not in lines]
    return Matroid.from_bases(7, bases)

def NonFano():
    lines = [frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6)]]
    bases = [b for b in combinations(range(7),3) if frozenset(b) not in lines]
    return Matroid.from_bases(7, bases)

def Vamos():
    # Vamos V_8: rank 4 on 8 elements. Circuit-hyperplanes (size 4): five specific 4-sets.
    # Standard def: V_8 has 5 circuit-hyperplanes (4-circuits): {1,2,3,4}, {1,2,5,6},
    # {3,4,5,6}, {3,4,7,8}, {5,6,7,8}.  Other 4-subsets are bases.
    CH = [frozenset(c) for c in [(0,1,2,3),(0,1,4,5),(2,3,4,5),(2,3,6,7),(4,5,6,7)]]
    bases = [b for b in combinations(range(8),4) if frozenset(b) not in CH]
    return Matroid.from_bases(8, bases)

def Pappus():
    # 9-point Pappus matroid, rank 3. Lines:
    lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(0,4,7),(0,5,8),
             (1,3,7),(1,4,8),(1,5,6),(2,3,8),(2,4,6),(2,5,7)]
    # actually Pappus has 9 lines. Let me use the standard one:
    lines = [(0,1,2),(3,4,5),(6,7,8),
             (0,3,7),(1,4,8),(2,5,6),
             (0,4,6),(1,5,7),(2,3,8)]
    lines = [frozenset(l) for l in lines]
    bases = [b for b in combinations(range(9),3) if frozenset(b) not in lines]
    return Matroid.from_bases(9, bases)

def AG32():
    # AG(3,2) = affine geometry, rank 4 on 8 points. 14 planes of size 4.
    # Identify points of GF(2)^3 with 0-7. A 4-set is a circuit iff sums to 0 (an affine plane).
    bases = []
    for B in combinations(range(8),4):
        # Test: is B a dependent 4-set (affine plane)?
        # A 4-set in F_2^3 is dependent iff sum = 0 (mod 2 componentwise).
        s = 0
        for p in B: s ^= p
        if s != 0: bases.append(B)
    return Matroid.from_bases(8, bases)


if __name__ == "__main__":
    # Bigger uniform
    for r,n in [(2,6),(3,6),(4,6),(3,7),(4,7)]:
        print(f"\n--- U_{r},{n}", flush=True)
        report(Matroid.uniform(r,n), f"U_{{{r},{n}}}")
    # Non-uniform
    for fn, name in [(M_K4, "M(K_4)"), (Fano, "Fano"), (NonFano,"NonFano"),
                     (Pappus,"Pappus"), (Vamos,"Vamos V_8"), (AG32,"AG(3,2)")]:
        print(f"\n--- {name}", flush=True)
        try:
            report(fn(), name)
        except Exception as e:
            print(f"ERR {name}: {e}")
