"""Push on the remaining open case: d=2 boundary at m=3 for low-girth matroids.

Test matroid: M(K_{2,4}) — bipartite graph K_{2,4}.
  n = 8 edges, rank = 5 (= 6 vertices - 1).
  corank = 3 = m at d=2 boundary.
  girth = 4 = corank + 1 (= boundary of "girth > corank+1" theorem in notes/36).

So M(K_{2,4}) is right at the edge where notes/36's theorem fails.

If ∂*: X_3 → X_4 is injective here, the project's conjecture extends.
If not, we have a counterexample — but project conjecture is empirically true
(verified across 200k+ orbits), so should be injective.

Goal: verify, then look for structural reasons.
"""
from __future__ import annotations
import sys
from itertools import combinations
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid
from test_hard_lefschetz_x import x_sets, bipartite_matrix, rank_modp
from d2_boundary_connected import build_graphic_matroid


def main():
    # K_{2,4}: vertices {0, 1} on "L" side, {2, 3, 4, 5} on "R" side.
    # 8 edges = a-c for a ∈ {0,1}, c ∈ {2,3,4,5}.
    edges_K24 = []
    for a in [0, 1]:
        for c in [2, 3, 4, 5]:
            edges_K24.append((a, c))
    M = build_graphic_matroid(edges_K24, 6)
    print(f"M(K_{{2,4}}): n={M.n}, rank={M.rank}, corank={M.n - M.rank}")
    print(f"  f-vector: {M.f}")
    xv = [len(x_sets(M, k)) for k in range(M.n + 1)]
    while xv and xv[-1] == 0: xv.pop()
    print(f"  X-vector: {xv}")

    n, r = M.n, M.rank
    # d=2 boundary at m = n/2 - 1 = 3
    m = 3
    assert 2*m + 2 == n and m + 2 == r, f"Not at d=2 boundary: m+2={m+2}, rank={r}"
    print(f"  d=2 boundary at m={m}, d=2")
    print(f"  |X_3| = {xv[3]}, |X_4| = {xv[4]}")

    # Compute ∂*: X_3 → X_4
    mat = bipartite_matrix(M, 3)
    print(f"  ∂* matrix shape: {mat.shape}")
    rk = rank_modp(mat)
    inj = (rk == xv[3])
    print(f"  Rank: {rk}  [{'INJ ✓' if inj else 'NOT INJ ✗'}]")

    if inj:
        print(f"\n  ∂* is INJECTIVE at m=3 d=2 boundary for M(K_{{2,4}}).")
        print(f"  This confirms project conjecture holds for this matroid.")
        print(f"  Now examine: WHY is it injective even though girth = corank+1?")

        # Look at forward degree distribution
        from collections import Counter
        X3 = x_sets(M, 3)
        fwds = []
        for A in X3:
            fwd_count = 0
            for i in range(M.n):
                if i in A: continue
                Aplus = A | frozenset([i])
                if Aplus in M.indep:
                    # Check Aplus ∈ X_4
                    E_complement = frozenset(range(M.n)) - Aplus
                    if E_complement in M.indep:
                        fwd_count += 1
            fwds.append(fwd_count)
        print(f"\n  Forward degree distribution:")
        for fwd, count in sorted(Counter(fwds).items()):
            print(f"    fwd={fwd}: {count} A's in X_3")
        print(f"  Min forward degree: {min(fwds)}")
        print(f"  Average: {sum(fwds)/len(fwds):.2f}")

        # Now back degrees
        X4 = x_sets(M, 4)
        bwds = []
        for A_p in X4:
            bwd_count = 0
            for e in A_p:
                A_minus = A_p - frozenset([e])
                if A_minus in [x for x in X3 if x == A_minus]:  # slow but OK
                    bwd_count += 1
            # faster: check directly
            bwd_count = 0
            for e in A_p:
                A_minus = A_p - frozenset([e])
                # A_minus ∈ X_3 iff A_minus indep AND E\A_minus indep
                if A_minus not in M.indep:
                    continue
                E_complement = frozenset(range(M.n)) - A_minus
                if E_complement in M.indep:
                    bwd_count += 1
            bwds.append(bwd_count)
        print(f"\n  Back degree distribution (X_4 → X_3):")
        for bwd, count in sorted(Counter(bwds).items()):
            print(f"    bwd={bwd}: {count} A's in X_4")
        print(f"  Max back degree: {max(bwds)}")

        print(f"\n  For Hall: min fwd {min(fwds)} ≥ max bwd {max(bwds)}? {'YES' if min(fwds) >= max(bwds) else 'NO'}")
        if min(fwds) < max(bwds):
            print(f"  → Hall via uniform min-fwd/max-bwd FAILS.")
            print(f"  → Need finer argument for injectivity.")


if __name__ == "__main__":
    main()
