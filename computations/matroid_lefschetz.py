"""
Test the QLC conjecture for small matroids.

R = k[x_1,..,x_n] / (x_I : I dependent ; x_i^2 for non-loop i).
R^v = graded dual; R_d has basis {x_S : S indep of size d}.
S = R \otimes R^v.   Bigrading: (m, e) where m = |S|, e = |S|-|T|.

L = sum_i x_i \otimes x_i,
  L(x_S \otimes y_T) = sum_{i in T, i not in S, S \cup {i} indep}
                          x_{S u {i}} \otimes y_{T \ {i}}.

For each matroid + each external degree e <= 0, build L : S_e -> S_{e+2} and
report its rank, source/target dims, and (failing-cases) the cokernel structure.
"""

from __future__ import annotations
from fractions import Fraction
from itertools import combinations, product
from typing import Iterable

import numpy as np
import sympy as sp


# ---------------- Matroid as set of independent sets ----------------

class Matroid:
    def __init__(self, n: int, independents: Iterable[frozenset]):
        self.n = n
        self.indep = set(map(frozenset, independents))
        # cache by size
        self.by_size: dict[int, list[frozenset]] = {}
        for S in self.indep:
            self.by_size.setdefault(len(S), []).append(S)
        for d in self.by_size:
            self.by_size[d].sort(key=lambda s: sorted(s))
        self.rank = max(self.by_size) if self.by_size else 0
        self.f = tuple(len(self.by_size.get(d, [])) for d in range(self.rank + 1))

    def is_indep(self, S) -> bool:
        return frozenset(S) in self.indep

    @classmethod
    def uniform(cls, r: int, n: int):
        indep = []
        for k in range(r + 1):
            for c in combinations(range(n), k):
                indep.append(frozenset(c))
        return cls(n, indep)

    @classmethod
    def from_bases(cls, n: int, bases: Iterable[Iterable[int]]):
        bases = [frozenset(b) for b in bases]
        indep = set()
        for B in bases:
            for k in range(len(B) + 1):
                for c in combinations(B, k):
                    indep.add(frozenset(c))
        return cls(n, indep)


# ---------------- S = R \otimes R^v basis & L matrix ----------------

def basis_in_external_degree(M: Matroid, e: int):
    """Basis of S_e: list of (S, T) with |S| - |T| = e and S, T independent."""
    out = []
    for m in range(M.rank + 1):
        sizeT = m - e
        if sizeT < 0 or sizeT > M.rank:
            continue
        for S in M.by_size.get(m, []):
            for T in M.by_size.get(sizeT, []):
                out.append((S, T))
    return out


def L_matrix(M: Matroid, e: int, ring=sp.Rational):
    """Build matrix of L : S_e -> S_{e+2} in monomial bases."""
    src = basis_in_external_degree(M, e)
    tgt = basis_in_external_degree(M, e + 2)
    src_idx = {st: i for i, st in enumerate(src)}
    tgt_idx = {st: i for i, st in enumerate(tgt)}

    # Use a dense sympy Matrix for exact rank
    rows = len(tgt)
    cols = len(src)
    A = sp.zeros(rows, cols)
    for j, (S, T) in enumerate(src):
        for i in T:
            if i in S:
                continue
            Snew = S | {i}
            if not M.is_indep(Snew):
                continue
            Tnew = T - {i}
            row = tgt_idx[(frozenset(Snew), frozenset(Tnew))]
            A[row, j] = A[row, j] + 1
    return A, src, tgt


def Lpow_matrix(M: Matroid, e: int, p: int):
    """Build matrix of L^p : S_e -> S_{e + 2p}."""
    A, src, tgt = L_matrix(M, e)
    for k in range(1, p):
        B, _, _ = L_matrix(M, e + 2 * k)
        A = B * A
        src_now = None
    return A


def report(M: Matroid, label: str, max_d: int = None):
    rk = M.rank
    if max_d is None:
        max_d = rk
    print(f"\n=== {label}  (n={M.n}, rank={rk}, f={M.f}) ===")
    # iterate over e = -d for d = 1..rk
    for d in range(1, max_d + 1):
        e = -d

        # L : S_{-d} -> S_{-d+2}
        A1, src, tgt = L_matrix(M, e)
        r1 = A1.rank()
        ds, dt = A1.shape[1], A1.shape[0]
        inj1 = (r1 == ds)
        surj1 = (r1 == dt)
        flag = "INJ" if inj1 else ("?inj" )
        flag2 = "SURJ" if surj1 else ""
        print(f"  d={d}: L: S_{-d}({ds}) -> S_{-d+2}({dt})  rank={r1}  {flag} {flag2}")

        # L^{d-1} : S_{-d} -> S_{d-2}  if d >= 2
        if d >= 2:
            A = A1.copy()
            for k in range(1, d - 1):
                B, _, _ = L_matrix(M, e + 2 * k)
                A = B * A
            rp = A.rank()
            dsp, dtp = A.shape[1], A.shape[0]
            inj = (rp == dsp)
            surj = (rp == dtp)
            print(f"        L^{d-1}: S_{-d}({dsp}) -> S_{d-2}({dtp})  rank={rp}  "
                  f"{'INJ' if inj else '?inj'} {'SURJ' if surj else ''}")

        # Hard Lefschetz: L^d : S_{-d} -> S_d
        A = A1.copy()
        for k in range(1, d):
            B, _, _ = L_matrix(M, e + 2 * k)
            A = B * A
        rp = A.rank()
        dsp, dtp = A.shape[1], A.shape[0]
        iso = (rp == dsp == dtp)
        print(f"        L^{d}: S_{-d}({dsp}) -> S_{d}({dtp})  rank={rp}  "
              f"{'ISO' if iso else 'NOT-ISO'}")


# ---------------- Specific matroids ----------------

def M_K4():
    # graphic matroid of K_4: 6 edges, rank 3, bases = spanning trees
    # edges: 0=12, 1=13, 2=14, 3=23, 4=24, 5=34
    # incident pairs as above
    edges = {
        0: (1,2), 1: (1,3), 2: (1,4), 3: (2,3), 4: (2,4), 5: (3,4),
    }
    def is_spanning_tree(B):
        # union-find
        parent = {v:v for v in range(1,5)}
        def find(x):
            while parent[x]!=x:
                parent[x]=parent[parent[x]]; x=parent[x]
            return x
        if len(B) != 3: return False
        for e in B:
            u,v = edges[e]
            ru, rv = find(u), find(v)
            if ru == rv: return False
            parent[ru] = rv
        return True
    bases = [b for b in combinations(range(6), 3) if is_spanning_tree(b)]
    return Matroid.from_bases(6, bases)


def Fano():
    # Fano plane F_7: rank 3 on 7 elements
    # 7 lines (3-element circuits / dependent sets); bases = 3-subsets not on a line
    lines = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
    lines = [frozenset(l) for l in lines]
    bases = []
    for B in combinations(range(7), 3):
        Bf = frozenset(B)
        if Bf not in lines:
            bases.append(B)
    return Matroid.from_bases(7, bases)


def NonFano():
    lines = [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6)]
    lines = [frozenset(l) for l in lines]
    bases = []
    for B in combinations(range(7), 3):
        Bf = frozenset(B)
        if Bf not in lines:
            bases.append(B)
    return Matroid.from_bases(7, bases)


# ---------------- Run ----------------

if __name__ == "__main__":
    # Smallest cases
    for r, n in [(1,2), (2,3), (2,4), (3,4), (2,5), (3,5)]:
        M = Matroid.uniform(r, n)
        report(M, f"U_{{{r},{n}}}", max_d=r)
    report(M_K4(), "M(K_4)")
    report(Fano(), "Fano")
    report(NonFano(), "NonFano (F_7^-)")
