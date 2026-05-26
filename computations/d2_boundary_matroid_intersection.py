"""Verify X_m(M) = Indep(M) ∩ Indep(M*) at d=2 boundary for multiple matroids.

The structural identification (notes/34):
  At d=2 boundary, m = corank.
  A ∈ X_m iff A indep AND E\A indep, with |A|=corank, |E\A|=rank.
  "E\A indep with |E\A|=rank" ⟺ "E\A is a basis" ⟺ "rank(E\A)=rank" ⟺ "A ∈ Indep(M*)".

So X_m = Indep(M)_m ∩ Indep(M*)_m at d=2 boundary.

This connects the project's conjecture at d=2 boundary to matroid intersection / ALOV.
"""
from __future__ import annotations
import sys
from itertools import combinations
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid
from test_hard_lefschetz_x import x_sets
from d2_boundary_connected import build_graphic_matroid


def dual_matroid(M):
    """Compute the dual matroid M*. Bases of M* = complements of bases of M."""
    n = M.n
    rank_M = M.rank
    corank = n - rank_M
    # bases of M*: B* = E\B for B basis of M.
    M_bases = M.by_size.get(rank_M, [])
    Mdual_bases = []
    E = frozenset(range(n))
    for B in M_bases:
        Mdual_bases.append(E - B)
    # build indep sets from bases (downward closure)
    indep_dual = set()
    for B in Mdual_bases:
        for k in range(len(B) + 1):
            for c in combinations(B, k):
                indep_dual.add(frozenset(c))
    indep_dual.add(frozenset())
    return Matroid(n, list(indep_dual))


def verify_intersection(M, label):
    print(f"\n{'='*65}")
    print(f"  {label}: n={M.n}, rank={M.rank}, corank={M.n - M.rank}")
    print(f"{'='*65}")
    n = M.n
    r = M.rank
    corank = n - r

    # d=2 boundary check
    d = 2
    m = (n - d) // 2
    if 2*m + d != n or m + d != r:
        print(f"  Not at d=2 boundary (m+d={m+d}, rank={r}). Skipping.")
        return None
    print(f"  d=2 boundary at m={m}={corank} ✓")

    # X_m
    X_m = set(x_sets(M, m))
    print(f"  |X_m| = {len(X_m)}")

    # Indep(M*)_m
    M_dual = dual_matroid(M)
    print(f"  M* has rank {M_dual.rank} (should = corank = {corank})")
    Indep_dual_m = set(M_dual.by_size.get(m, []))
    print(f"  |Indep(M*)_m| = {len(Indep_dual_m)}")

    # Indep(M)_m
    Indep_M_m = set(M.by_size.get(m, []))
    print(f"  |Indep(M)_m| = {len(Indep_M_m)}")

    # Intersection
    intersection = Indep_M_m & Indep_dual_m
    print(f"  |Indep(M)_m ∩ Indep(M*)_m| = {len(intersection)}")

    # Verify they're the same set
    match_set = (X_m == intersection)
    match_size = (len(X_m) == len(intersection))
    print(f"  X_m == Indep(M)∩Indep(M*) at size m? size: {match_size}, sets: {match_set}")
    if not match_set:
        only_in_X = X_m - intersection
        only_in_int = intersection - X_m
        print(f"    Only in X_m: {sorted([tuple(sorted(s)) for s in only_in_X])[:5]}")
        print(f"    Only in intersection: {sorted([tuple(sorted(s)) for s in only_in_int])[:5]}")
    return match_set


def main():
    # M(5-cycle + chord)
    edges1 = [(0,1), (1,2), (2,3), (3,4), (4,0), (0,2)]
    M1 = build_graphic_matroid(edges1, 5)
    verify_intersection(M1, "M(5-cycle + chord)")

    # M(K_{2,3})
    edges2 = [(0,2), (0,3), (0,4), (1,2), (1,3), (1,4)]
    M2 = build_graphic_matroid(edges2, 5)
    verify_intersection(M2, "M(K_{2,3})")

    # M(theta graph) — different drawing of K_{2,3}
    edges3 = [(0,2), (2,1), (0,3), (3,1), (0,4), (4,1)]
    M3 = build_graphic_matroid(edges3, 5)
    verify_intersection(M3, "M(theta = K_{2,3})")

    # U(3, 4) — uniform, d=2 boundary
    M4 = Matroid.uniform(3, 4)
    verify_intersection(M4, "U(3, 4)")

    # U(4, 6) — uniform, d=2 boundary
    M5 = Matroid.uniform(4, 6)
    verify_intersection(M5, "U(4, 6)")

    # U(5, 8) — uniform, d=2 boundary
    M6 = Matroid.uniform(5, 8)
    verify_intersection(M6, "U(5, 8)")


if __name__ == "__main__":
    main()
