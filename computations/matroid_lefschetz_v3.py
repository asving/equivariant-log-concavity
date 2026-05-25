"""
v3: probes
  (A) kernel of L : S_{-1} -> S_1 for non-uniform — identify its structure.
  (B) generic Lefschetz : L_g = sum c_i x_i\otimes x_i with random c_i (do we still get hard Lefschetz at d≥2?)
  (C) two-form Lefschetz : (l1 \otimes l2) where l1 = sum a_i x_i acts (mult) on left and l2 = sum b_i x_i acts (contraction) on right.
"""
from __future__ import annotations
from itertools import combinations
import sympy as sp
from sympy import zeros, Matrix, symbols, Rational
import random

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


def L_matrix(M, e, c=None):
    """L_c = sum_i c_i * (x_i op x_i). c=None → all-ones diagonal."""
    if c is None: c = [1]*M.n
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
            A[row, j] += c[i]
    return A, src, tgt


def Ltwo_matrix(M, e, a, b):
    """Generic 2-form Lefschetz: L_{a,b} = (sum a_i x_i) \otimes (sum b_j x_j), as operator.
    Acts as (x_a a) on left and (contraction by b) on right.
    """
    src = basis_in_external_degree(M, e)
    tgt = basis_in_external_degree(M, e+2)
    tgt_idx = {st: i for i, st in enumerate(tgt)}
    A = zeros(len(tgt), len(src))
    for j, (S, T) in enumerate(src):
        for i in range(M.n):
            if a[i] == 0 or i in S: continue
            Snew = S | {i}
            if not M.is_indep(Snew): continue
            for k in range(M.n):
                if b[k] == 0 or k not in T: continue
                Tnew = T - {k}
                row = tgt_idx[(frozenset(Snew), frozenset(Tnew))]
                A[row, j] += a[i] * b[k]
    return A, src, tgt


def Lpow_with_coeffs(M, e, p, c=None):
    A, _, _ = L_matrix(M, e, c)
    for k in range(1, p):
        B, _, _ = L_matrix(M, e + 2*k, c)
        A = B * A
    return A


def kernel_basis_with_supports(M, e):
    A, src, _ = L_matrix(M, e)
    if A.rank() == A.shape[1]:
        return None, src
    K = A.nullspace()
    return K, src


# --- Specific matroids ---
def M_K4():
    edges = {0:(1,2),1:(1,3),2:(1,4),3:(2,3),4:(2,4),5:(3,4)}
    def is_ST(B):
        if len(B)!=3: return False
        p={v:v for v in range(1,5)}
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
    return Matroid.from_bases(7, [b for b in combinations(range(7),3) if frozenset(b) not in lines])

def NonFano():
    lines = [frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6)]]
    return Matroid.from_bases(7, [b for b in combinations(range(7),3) if frozenset(b) not in lines])

def U2plus2plus2():
    """U_{2,2}+U_{2,2}+U_{2,2} = three parallel pairs. Rank 3 on 6 elts.
    elts 0,1 are parallel; 2,3 parallel; 4,5 parallel. Indep iff no pair {0,1},{2,3},{4,5}."""
    bad_pairs = [{0,1},{2,3},{4,5}]
    indep = []
    for k in range(4):
        for c in combinations(range(6), k):
            S = set(c)
            if not any(p.issubset(S) for p in bad_pairs):
                indep.append(frozenset(S))
    return Matroid(6, indep)


# --- Report ---
def report_kernel(M, label):
    print(f"\n=== {label}  f={M.f}  Kernel of L: S_{-1} -> S_1 ===")
    K, src = kernel_basis_with_supports(M, -1)
    if K is None:
        print(f"  L is injective on S_-1 — no kernel.")
        return
    print(f"  kernel dim = {len(K)}")
    # group basis elements by internal degree m = |S|
    by_m = {}
    for k_idx, v in enumerate(K):
        # find a representative monomial: take all (S,T) with nonzero coeff, group by m
        for i, val in enumerate(v):
            if val != 0:
                S, T = src[i]
                m = len(S)
                by_m.setdefault(m, []).append(k_idx)
                break
    # Show a few
    for k_idx, v in enumerate(K[:8]):
        terms = []
        for i, val in enumerate(v):
            if val != 0:
                S, T = src[i]
                terms.append(f"{val}*(x{sorted(S)}⊗y{sorted(T)})")
        print(f"  k_{k_idx}: " + " + ".join(terms))


def check_hard_lefschetz(M, label, n_random=2):
    print(f"\n=== {label} hard-Lefschetz with diagonal vs generic ===")
    rk = M.rank
    # diagonal
    for d in range(2, rk+1):
        A = Lpow_with_coeffs(M, -d, d)
        rk_d = A.rank()
        iso = rk_d == A.shape[0] == A.shape[1]
        print(f"  diag L^{d}: {A.shape[1]}->{A.shape[0]} rank={rk_d} {'ISO' if iso else 'NOT-ISO'}")
    # random diagonal coefficients
    rng = random.Random(42)
    for trial in range(n_random):
        c = [rng.randint(1, 100) for _ in range(M.n)]
        print(f"  random c={c}:")
        for d in range(2, rk+1):
            A = Lpow_with_coeffs(M, -d, d, c)
            rk_d = A.rank()
            iso = rk_d == A.shape[0] == A.shape[1]
            print(f"    L_c^{d}: rank={rk_d} {'ISO' if iso else 'NOT-ISO'}")
    # generic two-form (l1, l2) different
    for trial in range(n_random):
        a = [rng.randint(1, 100) for _ in range(M.n)]
        b = [rng.randint(1, 100) for _ in range(M.n)]
        print(f"  generic two-form a={a}, b={b}:")
        for d in range(2, rk+1):
            A, _, _ = Ltwo_matrix(M, -d, a, b)
            for k in range(1, d):
                B, _, _ = Ltwo_matrix(M, -d + 2*k, a, b)
                A = B * A
            rk_d = A.rank()
            iso = rk_d == A.shape[0] == A.shape[1]
            print(f"    L_{{a,b}}^{d}: rank={rk_d} {'ISO' if iso else 'NOT-ISO'}")


if __name__ == "__main__":
    print("=== KERNEL of L at d=1 ===")
    for fn, name in [(M_K4, "M(K_4)"), (Fano, "Fano"), (NonFano, "NonFano"), (U2plus2plus2, "U22+U22+U22")]:
        report_kernel(fn(), name)
    print("\n\n=== GENERIC LEFSCHETZ CHECK ===")
    for fn, name in [(M_K4, "M(K_4)"), (Fano, "Fano"), (NonFano,"NonFano"), (U2plus2plus2,"U22+U22+U22")]:
        check_hard_lefschetz(fn(), name)
