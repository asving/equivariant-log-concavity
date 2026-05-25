"""Recursive test of the block-triangular decomposition.

After one decomposition of ∂*_{N} by e, we get two paired operators:
  ∂*_{(N\e, N/e)}  on  ground set E \ {e}
  ∂*_{(N/e, N\e)}  on  ground set E \ {e}, shifted index by 1
(Both are X-bipartite operators on a PAIR of matroids.)

For the recursive proof to close, we need:
  ∂*_{(P, Q)} is injective for ALL pairs (P, Q) arising in the recursion.

This test descends recursively. At each level, we:
  - Verify ∂*_{(P,Q)} is injective on Y_k(P,Q) → Y_{k+1}(P,Q).
  - For each e in the common ground set, decompose; verify both diagonal blocks injective.
  - Recurse on the two resulting paired sub-operators.

We bound depth ≤ MAX_DEPTH and ground-set size to avoid blowup.

Paired definitions (for pair (P, Q) on common ground set E):
  Y_k(P, Q) = {A ⊆ E, |A|=k, A indep in P, E\A indep in Q}
  ∂*_{P,Q}(A) = Σ_{i ∈ E\A, A∪i ∈ Y_{k+1}(P, Q)} (A∪i)

Block decomposition by e ∈ E:
  Y_k^{no e}(P, Q)  = Y_k(P\e, Q/e)   (matroids on E \ {e})
  Y_k^{has e}(P, Q) = Y_{k-1}(P/e, Q\e)
  Diagonal blocks: ∂*_{(P\e, Q/e)} (grade k) and ∂*_{(P/e, Q\e)} (grade k-1).
"""

from __future__ import annotations
import sys
from itertools import combinations
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid, M_Kn
from sparse_rank import sparse_rank_modp

P_MOD = 10007


# --------- Matroid operations: deletion and contraction ---------

def delete(M, e):
    """M \\ e: restrict to E \\ {e}. Re-index elements 0..n-2 by skipping e."""
    new_indep = set()
    for A in M.indep:
        if e in A:
            continue
        # re-index: elements > e shift down by 1
        new_A = frozenset(x if x < e else x - 1 for x in A)
        new_indep.add(new_A)
    return Matroid(M.n - 1, list(new_indep))


def contract(M, e):
    """M / e: A indep in M/e iff A ∪ {e} indep in M (for e a non-loop)."""
    new_indep = set()
    for A in M.indep:
        if e in A:
            # Remove e and re-index
            B = A - frozenset([e])
            new_B = frozenset(x if x < e else x - 1 for x in B)
            new_indep.add(new_B)
    # Make sure to add the empty set if M/e has rank ≥ 0
    if not new_indep:
        new_indep.add(frozenset())
    return Matroid(M.n - 1, list(new_indep))


def y_sets(P, Q, k):
    """Y_k(P, Q) = {A ⊆ E, |A|=k, A indep in P, E\A indep in Q}.
       P, Q must have the same ground set size."""
    assert P.n == Q.n
    n = P.n
    E = frozenset(range(n))
    out = []
    for A in P.by_size.get(k, []):
        if (E - A) in Q.indep:
            out.append(A)
    return out


def paired_bipartite_entries(Yk, Ykp1, n):
    row_idx = {A: i for i, A in enumerate(Ykp1)}
    rows, cols, vals = [], [], []
    for j, A in enumerate(Yk):
        for i in range(n):
            if i in A:
                continue
            Ap = A | frozenset([i])
            if Ap in row_idx:
                rows.append(row_idx[Ap])
                cols.append(j)
                vals.append(1)
    return rows, cols, vals


def rank_of(rows, cols, vals, m, n):
    if n == 0 or m == 0 or not rows:
        return 0
    return sparse_rank_modp(rows, cols, vals, m, n, P_MOD, verbose=False)


def paired_injective(P, Q, k):
    """Return (injective?, |Y_k|, |Y_{k+1}|, rank)."""
    Yk = y_sets(P, Q, k)
    Ykp1 = y_sets(P, Q, k + 1)
    if not Yk:
        return True, 0, len(Ykp1), 0  # vacuously
    rows, cols, vals = paired_bipartite_entries(Yk, Ykp1, P.n)
    r = rank_of(rows, cols, vals, len(Ykp1), len(Yk))
    return (r == len(Yk)), len(Yk), len(Ykp1), r


def recurse_decomp(P, Q, k, depth, max_depth, indent=""):
    """Recursively decompose ∂*_{(P,Q)} on Y_k(P,Q) → Y_{k+1}(P,Q).
       Return (all_levels_injective_to_depth, summary_lines)."""
    if P.n == 0 or k < 0 or k >= P.n:
        return True, []

    # Verify full operator is injective.
    inj, ny_k, ny_k1, r = paired_injective(P, Q, k)
    if not inj:
        return False, [f"{indent}✗ FAILS at depth {depth}: |Y_k|={ny_k}, rank={r}"]

    lines = [f"{indent}depth {depth}: ground n={P.n}, k={k}, |Y_k|={ny_k:4d}, |Y_{{k+1}}|={ny_k1:4d}, ∂* INJ"]

    if depth >= max_depth or P.n == 0:
        return True, lines

    # Pick e and decompose. Try ALL e to make sure no e fails.
    all_ok = True
    for e in range(P.n):
        # Block 1: ∂*_{(P\e, Q/e)} on Y_k → Y_{k+1}
        Pdel = delete(P, e)
        Qcon = contract(Q, e)
        # Block 2: ∂*_{(P/e, Q\e)} on Y_{k-1} → Y_k
        Pcon = contract(P, e)
        Qdel = delete(Q, e)

        ok1, lines1 = recurse_decomp(Pdel, Qcon, k, depth + 1, max_depth,
                                     indent + "  ")
        ok2, lines2 = recurse_decomp(Pcon, Qdel, k - 1, depth + 1, max_depth,
                                     indent + "  ")
        if not (ok1 and ok2):
            lines.append(f"{indent}  Failure under e={e}:")
            lines.extend(lines1 if not ok1 else [])
            lines.extend(lines2 if not ok2 else [])
            all_ok = False
            break
        # Suppress success details to keep output manageable

    if all_ok:
        lines.append(f"{indent}  ✓ All e ∈ {{0,...,{P.n-1}}} yield injective sub-blocks at depth {depth+1}")

    return all_ok, lines


# --------- Matroid constructions ---------

def free_sum(M, k):
    """M ⊕ U_{k,k} — add k free elements."""
    extra = list(range(M.n, M.n + k))
    new_indep = []
    for A in M.indep:
        for s in range(k + 1):
            for fs in combinations(extra, s):
                new_indep.append(A | frozenset(fs))
    return Matroid(M.n + k, new_indep)


def single_triangle(extra_free):
    n = 3 + extra_free
    indep = []
    for kk in range(n + 1):
        for S in combinations(range(n), kk):
            S = frozenset(S)
            if {0, 1, 2}.issubset(S):
                continue
            indep.append(S)
    return Matroid(n, indep)


def main():
    tests = []
    # Pair (N, N) for various non-paving N. The pair starts as the diagonal.
    tests.append((single_triangle(3), 'Triangle ⊕ U_{3,3}'))
    tests.append((free_sum(M_Kn(4), 3), 'M(K_4) ⊕ U_{3,3}'))

    MAX_DEPTH = 3

    for N, label in tests:
        print(f"\n{'='*70}")
        print(f"  Recursive test: {label}, n={N.n}, rank={N.rank}")
        print(f"{'='*70}")
        # Find bigrade with d ≥ 2 (= original hypothesis).
        for k in range(N.n + 1):
            d = N.n - 2 * k
            if d < 2: continue
            if N.rank < k + d: continue
            if k + 1 > N.rank: continue
            print(f"\n--- Bigrade k={k}, d={d}, recursing to depth ≤ {MAX_DEPTH} ---")
            ok, lines = recurse_decomp(N, N, k, 0, MAX_DEPTH)
            for L in lines:
                print(L)
            print(f"  Verdict for k={k}, d={d}: {'ALL DEPTHS INJECTIVE' if ok else 'FAILS'}")


if __name__ == "__main__":
    main()
