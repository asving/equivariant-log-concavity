"""Test if the KW relaxation proof extends to all paving matroids (not just sparse paving).

Construct a paving non-sparse-paving matroid M satisfying our hypothesis, and verify
Theorem 4'-II computationally.

Concrete construction: take U_{5, 8} and add CHs F_1 = {0,1,2,3,4}, F_2 = {0,1,2,3,5}.
By the matroid axioms, this forces 4 more CHs:
  {0,1,2,4,5}, {0,1,3,4,5}, {0,2,3,4,5}, {1,2,3,4,5}
giving 6 CHs total — all 5-subsets of {0,...,5}.

This matroid has rank 5 on 8 elements:
  - {0,...,5} is a rank-4 flat (its 6 5-subsets are all CHs).
  - Circuits include 6 CHs of size 5 AND 15 circuits of size 6 (= subsets containing
    both 6 and 7 with 4 elements from {0,...,5}).
  - Hence circuits of size > rank → NOT sparse paving.

The matroid is a truncation: M = T_5(U_{4,6} ⊕ U_{2,2}) on {0,...,5} ⊔ {6, 7}.

We verify Theorem 4'-II at the relevant bigrade (k=3, d=2).
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from sparse_rank import sparse_rank_modp
from gpu_rank import Matroid


def make_paving_M():
    """Construct M = U_{5,8} with all 5-subsets of {0,...,5} as CHs.
    This is paving (no circuit smaller than rank 5) but NOT sparse paving
    (the 5-subsets {0,...,5} pairwise overlap in 4 = r-1 elements)."""
    n = 8
    r = 5
    bases_outside_flat = {0,1,2,3,4,5}
    indep = []
    for k in range(r + 1):
        for S in combinations(range(n), k):
            S = frozenset(S)
            # S indep iff not a CH and "constructively indep"
            # CHs: all 5-subsets of {0,...,5}
            if k == r:
                # 5-subset: indep iff not a 5-subset of {0,...,5}
                if S <= bases_outside_flat:
                    continue  # CH, skip
            # For larger sizes: indep iff no CH-superset...
            # Wait, indep sets are downward closed; we just need to NOT include CHs
            # of all sizes. For paving: all <r-subsets indep. For r-subsets: indep iff not CH.
            # No (r+1)-subsets are indep (would have rank > r).
            indep.append(S)
    return Matroid(n, indep)


def x_k_set(N, k):
    E = frozenset(range(N.n))
    out = []
    for A in combinations(range(N.n), k):
        A = frozenset(A)
        if A not in N.indep: continue
        if (E - A) not in N.indep: continue
        out.append(A)
    return out


def bipartite_rank(N, k, P=10007):
    Xk = x_k_set(N, k)
    Xkp1 = x_k_set(N, k+1)
    Xkp1_idx = {A: i for i, A in enumerate(Xkp1)}
    rows, cols, vals = [], [], []
    for j, A in enumerate(Xk):
        for i in range(N.n):
            if i in A: continue
            Ap = A | frozenset([i])
            if Ap in Xkp1_idx:
                rows.append(Xkp1_idx[Ap]); cols.append(j); vals.append(1)
    if not rows: return 0, len(Xk), len(Xkp1)
    r = sparse_rank_modp(rows, cols, vals, len(Xkp1), len(Xk), P, verbose=False)
    return r, len(Xk), len(Xkp1)


def is_sparse_paving(N):
    """Check if N is sparse paving: paving + dual paving.
    For rank r matroid on n elts: dual is paving iff every cocircuit has size ≥ n-r+1."""
    r = N.rank
    n = N.n
    # Find all CHs (= circuits of size r = size-r dep sets)
    chs = []
    for S in combinations(range(n), r):
        if frozenset(S) not in N.indep:
            chs.append(frozenset(S))
    # Sparse paving iff pairwise CHs intersect in ≤ r-2 elements
    for i, F1 in enumerate(chs):
        for F2 in chs[i+1:]:
            if len(F1 & F2) > r - 2:
                return False, chs
    return True, chs


def main():
    print("=" * 70)
    print("Testing whether KW relaxation extends to paving (non-sparse) matroids")
    print("=" * 70)

    N = make_paving_M()
    print(f"\nMatroid M: n={N.n}, rank={N.rank}, f-vector={N.f}")

    sp, chs = is_sparse_paving(N)
    print(f"Sparse paving? {sp}")
    print(f"# CHs (5-subsets that are dependent): {len(chs)}")
    print(f"CHs: {[sorted(c) for c in chs[:6]]}{'...' if len(chs) > 6 else ''}")

    # Check pairwise CH overlaps
    if chs:
        overlap_dist = {}
        for i, F1 in enumerate(chs):
            for F2 in chs[i+1:]:
                k = len(F1 & F2)
                overlap_dist[k] = overlap_dist.get(k, 0) + 1
        print(f"Pairwise CH overlap distribution: {overlap_dist}")
        max_overlap = max(overlap_dist) if overlap_dist else 0
        print(f"Max CH overlap: {max_overlap} (sparse paving requires ≤ {N.rank - 2})")

    # Test Theorem 4'-II at (k=3, d=2)
    k, d = 3, 2
    print(f"\nAt bigrade (k={k}, d={d}): 2k+d = {2*k+d}, k+d = {k+d}, rank = {N.rank}")
    rk, sd, td = bipartite_rank(N, k)
    print(f"  |X_k| = {sd}, |X_{{k+1}}| = {td}")
    print(f"  Bipartite incidence rank: {rk}")
    print(f"  Theorem 4'-II: {'✓ HOLDS (rank = |X_k|)' if rk == sd else '✗ FAILS'}")

    # Also: compare to the predicted shrinkage from the KW argument.
    # U_{5,8} has |X_3(U_{5,8})| = C(8,3) = 56.
    # Each CH that's a 5-subset of {0,...,5} removes a 3-subset from X_3
    # (= the complement, which is a 3-subset containing {6, 7} and one of {0,...,5}).
    print(f"\nKW argument prediction:")
    print(f"  Starting |X_k(U_{{5,8}})| = C(8, 3) = 56")
    print(f"  Each CH removes one complement → |X_k(M)| = 56 - {len(chs)} = {56 - len(chs)}")
    print(f"  Predicted bipartite rank (full column rank) = {56 - len(chs)}")
    print(f"  Empirically observed rank = {rk}")
    print(f"  Match: {'✓' if rk == 56 - len(chs) else '✗'}")


if __name__ == "__main__":
    main()
