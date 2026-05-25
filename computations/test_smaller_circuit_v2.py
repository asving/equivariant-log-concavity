"""Test smaller-circuit relaxation with VALID matroids only.

Key issue from v1: "U_{r,n} + several small circuits" may NOT satisfy matroid
axioms unless the circuits are chosen carefully. The circuit elimination axiom
(C_1, C_2 circuits, e ∈ C_1 ∩ C_2 ⇒ ∃ C_3 ⊆ (C_1 ∪ C_2)\\{e} circuit) may force
additional circuits.

This version verifies matroid validity before testing.
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from sparse_rank import sparse_rank_modp
from gpu_rank import Matroid


def make_with_circuits(r, n, declared_circuits):
    """Construct M with rank ≤ r on [n] where the declared subsets are circuits.
    Returns the matroid IF the indep system is valid, else None."""
    declared = [frozenset(C) for C in declared_circuits]
    indep_sets = []
    for k in range(min(r, n) + 1):
        for S in combinations(range(n), k):
            S = frozenset(S)
            # S indep iff S contains no declared circuit
            contains = any(C <= S for C in declared)
            if not contains:
                indep_sets.append(S)
    M = Matroid(n, indep_sets)
    return M


def is_valid_matroid(M):
    """Check matroid axioms (specifically augmentation)."""
    # Augmentation: for A, B indep, |A| < |B|, ∃ x ∈ B\\A with A∪x indep.
    indep_list = sorted(M.indep, key=lambda S: len(S))
    for A in indep_list:
        for B in indep_list:
            if len(A) >= len(B): continue
            found = False
            for x in B - A:
                if (A | frozenset([x])) in M.indep:
                    found = True; break
            if not found:
                return False, (A, B)
    return True, None


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


def test_matroid(name, r, n, circuits, k):
    """Test bipartite incidence rank for the matroid given by declared circuits."""
    print(f"\n--- {name} ---")
    M = make_with_circuits(r, n, circuits)
    print(f"  f-vector: {M.f}, rank={M.rank}")

    valid, witness = is_valid_matroid(M)
    print(f"  Matroid axioms valid? {valid}")
    if not valid:
        print(f"    Augmentation fails: A={sorted(witness[0])}, B={sorted(witness[1])}")
        return None

    rk, sd, td = bipartite_rank(M, k)
    print(f"  At k={k}: |X_k|={sd}, |X_{{k+1}}|={td}, rank={rk}, full rank: {rk == sd}")
    return (M.f, sd, td, rk)


if __name__ == "__main__":
    print("="*70)
    print("Smaller-circuit relaxation test (validity-checked)")
    print("Working at U_{5,8}, bigrade k=3, d=2")
    print("="*70)

    # Baseline: uniform
    test_matroid("U_{5,8} (no circuits)", 5, 8, [], 3)

    # Single 3-circuit (= triangle)
    test_matroid("U_{5,8} + 1 triangle {0,1,5}", 5, 8, [{0, 1, 5}], 3)

    # Two DISJOINT 3-circuits (should be valid)
    test_matroid("U_{5,8} + 2 disjoint triangles", 5, 8,
                 [{0, 1, 5}, {2, 3, 6}], 3)

    # Three disjoint 3-circuits: only possible if 8 ≥ 3*3 = 9, so 2 disjoint is max for n=8.
    # Try 2 triangles that share an element (NEEDS more circuits forced).
    print("\n\n--- Sharing one element: forces a 4-circuit ---")
    test_matroid("U_{5,8} + {0,1,5}, {0,2,6} alone", 5, 8,
                 [{0, 1, 5}, {0, 2, 6}], 3)
    print("\n  Now add the forced 4-circuit:")
    test_matroid("U_{5,8} + {0,1,5}, {0,2,6}, {1,2,5,6}", 5, 8,
                 [{0, 1, 5}, {0, 2, 6}, {1, 2, 5, 6}], 3)

    # Single 4-circuit
    test_matroid("U_{5,8} + 1 4-circuit {0,1,2,3}", 5, 8, [{0, 1, 2, 3}], 3)

    # Multiple disjoint 4-circuits (only one possible in n=8)
    # 1 4-circuit + 1 disjoint 3-circuit
    test_matroid("U_{5,8} + 4-circuit {0,1,2,3} + 3-circuit {4,5,6}", 5, 8,
                 [{0, 1, 2, 3}, {4, 5, 6}], 3)
