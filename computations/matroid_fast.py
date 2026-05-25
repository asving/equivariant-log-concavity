"""
Fast rank computation using mod-p (p=10007 say). Big matroids only.
"""
from __future__ import annotations
from itertools import combinations
import numpy as np

P = 10007  # small prime for mod-p rank

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
        return cls(n, [frozenset(c) for k in range(r+1) for c in combinations(range(n), k)])
    @classmethod
    def from_bases(cls, n, bases):
        indep = set()
        for B in bases:
            for k in range(len(B)+1):
                for c in combinations(B, k): indep.add(frozenset(c))
        return cls(n, indep)


def basis_in_external_degree(M, e):
    out = []
    for m in range(M.rank+1):
        sT = m - e
        if sT < 0 or sT > M.rank: continue
        for S in M.by_size.get(m, []):
            for T in M.by_size.get(sT, []):
                out.append((S, T))
    return out


def L_matrix_modp(M, e):
    src = basis_in_external_degree(M, e)
    tgt = basis_in_external_degree(M, e+2)
    tgt_idx = {st: i for i, st in enumerate(tgt)}
    A = np.zeros((len(tgt), len(src)), dtype=np.int64)
    for j, (S, T) in enumerate(src):
        for i in T:
            if i in S: continue
            Snew = S | {i}
            if not M.is_indep(Snew): continue
            Tnew = T - {i}
            row = tgt_idx[(frozenset(Snew), frozenset(Tnew))]
            A[row, j] += 1
    return A % P, src, tgt


def modp_rank(A):
    """Gaussian elimination mod P. A is int64."""
    A = A.copy()
    rows, cols = A.shape
    r = 0
    for c in range(cols):
        if r >= rows: break
        # find pivot
        pivot = -1
        for k in range(r, rows):
            if A[k, c] % P != 0:
                pivot = k; break
        if pivot < 0: continue
        if pivot != r: A[[r, pivot]] = A[[pivot, r]]
        # invert pivot
        inv = pow(int(A[r, c]) % P, P - 2, P)
        A[r] = (A[r] * inv) % P
        # eliminate
        for k in range(rows):
            if k == r: continue
            if A[k, c] % P != 0:
                A[k] = (A[k] - A[k, c] * A[r]) % P
        r += 1
    return r


def matmul_modp(A, B):
    return np.dot(A, B) % P


def report(M, label):
    rk = M.rank
    print(f"\n=== {label} n={M.n} rk={rk} f={M.f} ===", flush=True)
    for d in range(1, rk+1):
        A, _, _ = L_matrix_modp(M, -d)
        r1 = modp_rank(A.copy())
        ds, dt = A.shape[1], A.shape[0]
        msg = f"  d={d}: L: {ds}->{dt} rank={r1}"
        msg += "  INJ" if r1==ds else f"  ker={ds-r1}"
        msg += "  SURJ" if r1==dt else f"  coker={dt-r1}"
        print(msg, flush=True)
        # L^d
        Ap = A.copy()
        for k in range(1, d):
            B, _, _ = L_matrix_modp(M, -d + 2*k)
            Ap = matmul_modp(B, Ap)
        rp = modp_rank(Ap.copy())
        dsp, dtp = Ap.shape[1], Ap.shape[0]
        iso = rp == dsp == dtp
        print(f"        L^{d}: {dsp}->{dtp} rank={rp} {'ISO' if iso else 'NOT-ISO'}", flush=True)


# --- Matroids ---
def Pappus():
    lines = [(0,1,2),(3,4,5),(6,7,8),
             (0,3,7),(1,4,8),(2,5,6),
             (0,4,6),(1,5,7),(2,3,8)]
    lines = [frozenset(l) for l in lines]
    bases = [b for b in combinations(range(9),3) if frozenset(b) not in lines]
    return Matroid.from_bases(9, bases)

def NonPappus():
    # Non-Pappus matroid: same as Pappus but with one line removed (not a line in NP).
    # Standard non-Pappus: drop the line (2,5,6) or similar; results in non-realizable matroid.
    lines = [(0,1,2),(3,4,5),(6,7,8),
             (0,3,7),(1,4,8),
             (0,4,6),(1,5,7),(2,3,8)]
    lines = [frozenset(l) for l in lines]
    bases = [b for b in combinations(range(9),3) if frozenset(b) not in lines]
    return Matroid.from_bases(9, bases)

def Vamos():
    CH = [frozenset(c) for c in [(0,1,2,3),(0,1,4,5),(2,3,4,5),(2,3,6,7),(4,5,6,7)]]
    bases = [b for b in combinations(range(8),4) if frozenset(b) not in CH]
    return Matroid.from_bases(8, bases)

def AG32():
    bases = []
    for B in combinations(range(8),4):
        s = 0
        for p in B: s ^= p
        if s != 0: bases.append(B)
    return Matroid.from_bases(8, bases)

def M_K5():
    # K5: 10 edges, rank 4. Encode edges by 2-subset of {0..4}.
    es = list(combinations(range(5),2))
    edge_of = {i:e for i,e in enumerate(es)}
    def is_ST(B):
        # spanning tree if and only if 4 edges, no cycle
        if len(B) != 4: return False
        p = {v:v for v in range(5)}
        def f(x):
            while p[x]!=x: p[x]=p[p[x]]; x=p[x]
            return x
        for i in B:
            u,v = edge_of[i]
            ru,rv = f(u),f(v)
            if ru == rv: return False
            p[ru] = rv
        return True
    bases = [b for b in combinations(range(10), 4) if is_ST(b)]
    return Matroid.from_bases(10, bases)


if __name__ == "__main__":
    import sys
    todo = sys.argv[1:] if len(sys.argv) > 1 else ['vamos','ag32','pappus','nonpappus','k5']
    for name in todo:
        if name == 'pappus': report(Pappus(), "Pappus")
        elif name == 'nonpappus': report(NonPappus(), "NonPappus")
        elif name == 'vamos': report(Vamos(), "Vamos V_8")
        elif name == 'ag32': report(AG32(), "AG(3,2)")
        elif name == 'k5': report(M_K5(), "M(K_5)")
        else: print("unknown:", name)
