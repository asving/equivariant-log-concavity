"""Investigate the d=2 boundary case of the project's conjecture for non-paving
matroids — the genuinely open part not covered by Hall (notes/33) or the paving
theorem (PAPER §4).

Test matroids: connected non-uniform with rank exactly (n+2)/2 (= d=2 boundary).

For each: verify ∂* injective empirically, then look for structural patterns
in the kernel (= linear dependencies among rows of ∂*).

If ∂* injective + structural pattern visible, we have hints for a proof.
"""

from __future__ import annotations
import sys
from itertools import combinations
import numpy as np
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid
from test_hard_lefschetz_x import x_sets, bipartite_matrix, rank_modp


def build_rank4_on6_triangle():
    """M with rank 4 on E={0..5} with one triangle circuit C={0,1,2}.

    Indep sets: subsets not containing the triangle.
    rank = 4 since we can find indep 4-sets like {0,1,3,4}.
    """
    n = 6
    triangle = frozenset({0, 1, 2})
    indep = []
    for k in range(n + 1):
        for S in combinations(range(n), k):
            S = frozenset(S)
            if triangle.issubset(S):
                continue  # contains the triangle, so dependent
            indep.append(S)
    return Matroid(n, indep)


def build_rank_r_on_2r_minus_2_one_triangle():
    """Family: rank r on 2r-2 elements with one triangle circuit.
    Parameterized by r ≥ 3."""
    def f(r):
        n = 2*r - 2
        triangle = frozenset({0, 1, 2})
        indep = []
        for k in range(n + 1):
            for S in combinations(range(n), k):
                S = frozenset(S)
                if triangle.issubset(S):
                    continue
                indep.append(S)
        return Matroid(n, indep)
    return f


def analyze(M, label):
    print(f"\n{'='*70}")
    print(f"  {label}: n={M.n}, rank={M.rank}")
    print(f"{'='*70}")
    print(f"  f-vector: {M.f}")
    n, r = M.n, M.rank
    xv = [len(x_sets(M, k)) for k in range(n + 1)]
    while xv and xv[-1] == 0: xv.pop()
    print(f"  X-vector: {xv}")

    # Find d=2 boundary bigrade if any
    # 2m+d=n, m+d ≤ r, d ≥ 2; d=2 boundary means d=2.
    d = 2
    m = (n - d) // 2
    if 2*m + d == n and m + d <= r and m >= 0:
        print(f"  d=2 boundary bigrade: m={m}, d={d}")
        if m < len(xv) and m+1 < len(xv):
            mat = bipartite_matrix(M, m)
            rk = rank_modp(mat)
            print(f"  ∂*: X_{m}({xv[m]}) → X_{m+1}({xv[m+1]}): rank={rk}")
            inj = (rk == xv[m])
            print(f"  Injective: {inj}")
            return inj, m, mat, xv
    return None, None, None, xv


def main():
    results = []

    # Test 1: rank 4 on 6 with one triangle circuit
    M1 = build_rank4_on6_triangle()
    r1, m1, mat1, xv1 = analyze(M1, "Rank-4-on-6 with triangle {0,1,2}")
    results.append(("Rank-4-on-6 with triangle", r1))

    # Test 2: family for r = 3, 4, 5
    factory = build_rank_r_on_2r_minus_2_one_triangle()
    for r in [3, 4, 5]:
        M = factory(r)
        result, m, mat, xv = analyze(M, f"Rank-{r}-on-{2*r-2} with triangle {{0,1,2}}")
        results.append((f"Rank-{r}-on-{2*r-2}", result))

    print(f"\n{'='*70}")
    print("Summary at d=2 boundary:")
    for label, r in results:
        flag = "INJ" if r is True else ("FAIL" if r is False else "—")
        print(f"  {label}: {flag}")


if __name__ == "__main__":
    main()
