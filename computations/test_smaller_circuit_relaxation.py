"""Test the Schur-complement extension of KW relaxation to non-paving matroids.

Setup: M_1 = U_{5,8} with a single triangle (3-circuit) T = {0, 1, 5} added.
This is the simplest non-paving matroid satisfying our hypothesis (n=8, r=5, k=3, d=2).

In U_{5,8}: |X_3| = 56, |X_4| = 70, bipartite rank = 56 (boolean Lefschetz).
In M_1: ? Compute and compare.

Key question: under "add a small circuit" (NOT a CH), the bipartite incidence matrix
changes by both row AND column deletions. Does the rank still equal |X_k|?

If so, the Schur-complement extension applies and we have a path to non-paving ELC.
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
import numpy as np
from sparse_rank import sparse_rank_modp
from gpu_rank import Matroid


def make_uniform_with_small_circuits(r, n, small_circuits):
    """Construct M = U_{r,n} with specified subsets `small_circuits` declared as circuits.
    Each circuit must have size ≤ r. The matroid is valid as long as the circuits
    satisfy circuit elimination axiom.

    indep(M) = {S : S has size ≤ r AND S doesn't contain any circuit AND S not in extended dep set}.

    For a single small circuit C of size c < r: the resulting matroid has indep sets =
    {S : |S| ≤ r, S doesn't contain C}.
    """
    indep_sets = []
    for k in range(r+1):
        for S in combinations(range(n), k):
            S = frozenset(S)
            # Check if S contains any small circuit
            contains = any(C <= S for C in small_circuits)
            if contains:
                continue
            indep_sets.append(S)
    return Matroid(n, indep_sets)


def X_k_set(N, k):
    E = frozenset(range(N.n))
    out = []
    for A in combinations(range(N.n), k):
        A = frozenset(A)
        if A not in N.indep: continue
        if (E - A) not in N.indep: continue
        out.append(A)
    return out


def bipartite_rank(N, k, P=10007):
    Xk = X_k_set(N, k)
    Xkp1 = X_k_set(N, k+1)
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


def main():
    print("="*70)
    print("Smaller-circuit relaxation test: M_1 = U_{5,8} + one 3-circuit T")
    print("="*70)

    # M_0 = U_{5,8} (uniform, no small circuits)
    M0 = make_uniform_with_small_circuits(5, 8, [])
    print(f"\nM_0 = U_{{5,8}}: f-vector = {M0.f}")

    k = 3
    rk0, sd0, td0 = bipartite_rank(M0, k)
    print(f"  At (k={k}, d=2): |X_k|={sd0}, |X_{{k+1}}|={td0}, bipartite rank={rk0}")
    print(f"  Theorem 4'-II: {'✓' if rk0 == sd0 else '✗'}")

    # M_1 = U_{5,8} + single 3-circuit T = {0, 1, 5}
    T = frozenset({0, 1, 5})
    M1 = make_uniform_with_small_circuits(5, 8, [T])
    print(f"\nM_1 = U_{{5,8}} with 3-circuit T={sorted(T)}: f-vector = {M1.f}")

    # Verify M_1 is non-paving (has circuit of size < rank=5)
    print(f"  T is a {len(T)}-circuit in M_1; rank(M_1) = {M1.rank}. Non-paving: {len(T) < M1.rank}")

    rk1, sd1, td1 = bipartite_rank(M1, k)
    print(f"  At (k={k}, d=2): |X_k|={sd1}, |X_{{k+1}}|={td1}, bipartite rank={rk1}")
    print(f"  Theorem 4'-II: {'✓ FULL RANK' if rk1 == sd1 else f'✗ deficit {sd1 - rk1}'}")

    # Compare: how did X-set change?
    print(f"\nChange from M_0 to M_1:")
    print(f"  |X_k|: {sd0} → {sd1} (lost {sd0 - sd1})")
    print(f"  |X_{{k+1}}|: {td0} → {td1} (lost {td0 - td1})")
    print(f"  rank: {rk0} → {rk1} (decreased by {rk0 - rk1})")
    print(f"  Simple submatrix bound: rank decrease ≤ rows removed + cols removed = {(td0-td1) + (sd0-sd1)} = {td0-td1} + {sd0-sd1}")
    print(f"  Actual rank decrease: {rk0 - rk1}")
    print(f"  Match |X_k| shrinkage: {rk0 - rk1 == sd0 - sd1}")

    # Test with two small circuits
    print(f"\n" + "="*70)
    print("Multiple 3-circuits added:")
    print("="*70)

    for ch_set in [
        [frozenset({0, 1, 5})],
        [frozenset({0, 1, 5}), frozenset({0, 2, 6})],
        [frozenset({0, 1, 5}), frozenset({0, 2, 6}), frozenset({0, 3, 7})],
    ]:
        M = make_uniform_with_small_circuits(5, 8, ch_set)
        rk, sd, td = bipartite_rank(M, k)
        print(f"\n  CHs: {[sorted(c) for c in ch_set]}")
        print(f"    f-vector: {M.f}")
        print(f"    |X_k|={sd}, |X_{{k+1}}|={td}, rank={rk}, full rank: {rk == sd}")


if __name__ == "__main__":
    main()
