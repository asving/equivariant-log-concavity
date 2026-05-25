"""Verify that at d≥2 bigrade hypothesis, f_m(M) ≤ f_{m+1}(M).

This is the key technical input needed for the geometric proof template to close.

For each matroid M satisfying d≥2 bigrade hypothesis at (m, d):
  - Check f_m(M) ≤ f_{m+1}(M).
  - If true universally, then by Mason's log-concavity (AHK 2018), the structural
    argument in notes/31 closes.

Mason's log-concavity says f_k^2 ≥ f_{k-1} · f_{k+1}. Hence f-vector unimodal.

For matroids in d≥2 hypothesis: m ≤ min((n-2)/2, rank-2). The claim is that
this puts m in the rising part of f-vector.
"""
from __future__ import annotations
import sys
from itertools import combinations
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid, M_Kn, Vamos
from test_hard_lefschetz_x import free_sum, single_triangle


def build_K4_minus_e():
    edges = [(0,2), (0,3), (1,2), (1,3), (2,3)]
    n = 5
    def is_forest(idxs):
        parent = list(range(4))
        def find(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v
        for i in idxs:
            u, v = edges[i]
            ru, rv = find(u), find(v)
            if ru == rv: return False
            parent[ru] = rv
        return True
    indep = []
    for k in range(n + 1):
        for S in combinations(range(n), k):
            if is_forest(S):
                indep.append(frozenset(S))
    return Matroid(n, indep)


def build_hexagon_chord():
    edges = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (0,3)]
    n_e = 7
    n_v = 6
    def is_forest(idxs):
        parent = list(range(n_v))
        def find(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v
        for i in idxs:
            u, v = edges[i]
            ru, rv = find(u), find(v)
            if ru == rv: return False
            parent[ru] = rv
        return True
    indep = []
    for k in range(n_e + 1):
        for S in combinations(range(n_e), k):
            if is_forest(S):
                indep.append(frozenset(S))
    return Matroid(n_e, indep)


def check(M, label):
    n, r = M.n, M.rank
    f = list(M.f)
    # find d≥2 bigrade hypothesis: 2m+d=n, m+d ≤ r, d ≥ 2 ⟹ m ≤ min((n-2)/2, r-2)
    m_max = min((n - 2) // 2, r - 2)
    print(f"\n  {label}: n={n}, rank={r}, f-vector = {f}")
    if m_max < 0:
        print(f"    No valid d≥2 bigrade.")
        return True

    all_ok = True
    for m in range(m_max + 1):
        # d = n - 2m (for the orbit (∅, E)). Check m + d = n - m ≤ rank.
        d = n - 2*m
        if d < 2:
            continue
        if m + d > r:
            continue
        fm = f[m] if m < len(f) else 0
        fmp1 = f[m+1] if m+1 < len(f) else 0
        ok = fm <= fmp1
        flag = "✓" if ok else "✗ FAILS"
        print(f"    bigrade (m={m}, d={d}): f_{m}={fm}, f_{m+1}={fmp1}  [{flag}]")
        if not ok:
            all_ok = False
    return all_ok


def main():
    matroids = [
        (Matroid.uniform(3, 4), "U(3,4)"),
        (Matroid.uniform(4, 5), "U(4,5)"),
        (Matroid.uniform(4, 6), "U(4,6)"),
        (Matroid.uniform(5, 7), "U(5,7)"),
        (Matroid.uniform(5, 8), "U(5,8)"),
        (single_triangle(2), "Triangle ⊕ U(2,2)"),
        (single_triangle(3), "Triangle ⊕ U(3,3)"),
        (single_triangle(4), "Triangle ⊕ U(4,4)"),
        (M_Kn(4), "M(K_4)"),
        (M_Kn(5), "M(K_5)"),
        (free_sum(M_Kn(4), 3), "M(K_4) ⊕ U(3,3)"),
        (free_sum(M_Kn(4), 4), "M(K_4) ⊕ U(4,4)"),
        (build_K4_minus_e(), "M(K_4 - e)"),
        (build_hexagon_chord(), "M(hexagon + chord)"),
    ]
    all_pass = True
    for M, label in matroids:
        if not check(M, label):
            all_pass = False
    print(f"\n{'='*60}")
    print(f"OVERALL: {'ALL PASS — Mason monotonicity at d≥2 hypothesis ✓' if all_pass else 'SOME FAIL'}")


if __name__ == "__main__":
    main()
