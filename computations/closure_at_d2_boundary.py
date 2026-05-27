"""TEST: at d=2 boundary, does closure_M(A) = A for every A ∈ X_m?

If TRUE in general: forward degree = m+2 uniformly, Hall holds, ∂* injective.
If FALSE: find counterexample.

The claim is interesting because A ∈ X_m means A indep AND E\A is a basis of M.
closure(A) > A would require a circuit C ⊂ A ∪ {e} with e ∉ A AND |C| ≤ m+1.

Equivalent: ∃ e ∈ E\A such that A ∪ {e} is dependent (= contains a circuit).

For e ∈ E\A = basis: e is "in the basis", so removing it from the basis drops rank.
But adding it to A could make A ∪ {e} dependent... depends on matroid.

Empirical test: build many connected non-uniform matroids at d=2 boundary and verify
closure(A) = A for all A ∈ X_m.
"""
from __future__ import annotations
import sys
from itertools import combinations
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid
from test_hard_lefschetz_x import x_sets
from d2_boundary_connected import build_graphic_matroid


def rank_of(M, A):
    """Rank of subset A in matroid M."""
    return max((len(B) for B in M.indep if B.issubset(A)), default=0)


def closure(M, A):
    """Closure of subset A in matroid M."""
    A = frozenset(A)
    rk_A = rank_of(M, A)
    closure_set = set(A)
    for e in range(M.n):
        if e in A:
            continue
        if rank_of(M, A | {e}) == rk_A:
            closure_set.add(e)
    return frozenset(closure_set)


def test_closure_property(M, label):
    print(f"\n{'='*65}")
    print(f"  {label}: n={M.n}, rank={M.rank}, corank={M.n - M.rank}")
    print(f"{'='*65}")
    n, r = M.n, M.rank
    corank = n - r
    if not (2*corank + 2 == n and corank + 2 == r):
        print(f"  Not at d=2 boundary. Skipping.")
        return
    m = corank
    X_m = x_sets(M, m)
    print(f"  |X_m| = {len(X_m)}")

    # Check closure(A) = A for each A ∈ X_m
    bad_count = 0
    bad_examples = []
    for A in X_m:
        cl = closure(M, A)
        if cl != A:
            bad_count += 1
            if len(bad_examples) < 3:
                bad_examples.append((A, cl))

    if bad_count == 0:
        print(f"  ✓ closure(A) = A for ALL {len(X_m)} elements of X_m.")
        print(f"  → fwd(A) = m+2 = {m+2} for all A.")
        print(f"  → max bwd ≤ m+1 = {m+1}.")
        print(f"  → Hall holds, ∂* INJECTIVE.")
    else:
        print(f"  ✗ closure(A) > A for {bad_count} / {len(X_m)} elements of X_m.")
        for A, cl in bad_examples:
            extras = cl - A
            print(f"    A = {sorted(A)}, closure has extras {sorted(extras)}")


def main():
    print("Testing the conjecture: at d=2 boundary, closure_M(A) = A for all A ∈ X_m\n")

    # K_{2,4}
    edges = [(a, c) for a in [0, 1] for c in [2, 3, 4, 5]]
    M = build_graphic_matroid(edges, 6)
    test_closure_property(M, "M(K_{2,4})")

    # 5-cycle + chord
    edges = [(0,1), (1,2), (2,3), (3,4), (4,0), (0,2)]
    M = build_graphic_matroid(edges, 5)
    test_closure_property(M, "M(5-cycle + chord)")

    # K_{3,3} - 1 edge: 8 edges, rank 5 on 6 vertices
    edges = []
    for a in [0, 1, 2]:
        for c in [3, 4, 5]:
            edges.append((a, c))
    edges = edges[:-1]  # Remove last edge to get 8 edges
    M = build_graphic_matroid(edges, 6)
    test_closure_property(M, "M(K_{3,3} - e)")

    # K_4 + 2 pendants (= K_4 with 2 extra vertices each connected by one edge)
    edges = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3), (0,4), (1,5)]
    M = build_graphic_matroid(edges, 6)
    test_closure_property(M, "M(K_4 + 2 pendants)")

    # M(theta) variant: 4 vertices with 2 vertices joined by 3 internally disjoint paths
    edges = [(0,2), (2,1), (0,3), (3,1), (0,4), (4,1), (0,5), (5,1)]
    M = build_graphic_matroid(edges, 6)
    test_closure_property(M, "M(theta-4) = K_{2,4}-ish")

    # 6-cycle: n=6, rank=5, corank=1. d=2 boundary at m=1, n=4. Not 6-cycle.
    # Skip pure 6-cycle.

    # n=10, rank=6, d=2 boundary at m=4
    # K_{3,4} has 12 edges. Too many.
    # K_{2,5} has 10 edges, 7 vertices, rank 6. d=2 boundary at m=4.
    edges_K25 = [(a, c) for a in [0, 1] for c in [2, 3, 4, 5, 6]]
    M = build_graphic_matroid(edges_K25, 7)
    test_closure_property(M, "M(K_{2,5})")


if __name__ == "__main__":
    main()


# Re-run with ∂* rank check for harder cases
def main2():
    from test_hard_lefschetz_x import bipartite_matrix, rank_modp
    print("\n\n=== ∂* RANK CHECK on harder cases ===")
    
    matroids = []
    
    # 5-cycle + chord
    edges = [(0,1), (1,2), (2,3), (3,4), (4,0), (0,2)]
    M = build_graphic_matroid(edges, 5)
    matroids.append(("M(5-cycle + chord)", M, 2))
    
    # K_{3,3} - 1 edge
    edges = []
    for a in [0, 1, 2]:
        for c in [3, 4, 5]:
            edges.append((a, c))
    edges = edges[:-1]
    M = build_graphic_matroid(edges, 6)
    matroids.append(("M(K_{3,3} - e)", M, 3))
    
    # K_4 + 2 pendants
    edges = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3), (0,4), (1,5)]
    M = build_graphic_matroid(edges, 6)
    matroids.append(("M(K_4 + 2 pendants)", M, 3))
    
    for label, M, m in matroids:
        X_m = x_sets(M, m)
        if not X_m:
            continue
        mat = bipartite_matrix(M, m)
        rk = rank_modp(mat)
        inj = (rk == len(X_m))
        print(f"  {label}: |X_{m}|={len(X_m)}, ∂* rank={rk}  [{'INJ ✓' if inj else 'NOT INJ ✗'}]")


if __name__ == "__main__":
    main2()
