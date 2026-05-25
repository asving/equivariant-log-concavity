"""Dissect the depth-3 failure: a paired operator (P, Q) where ∂*_{P,Q} is NOT injective,
even though it arises as a sub-block of an injective parent operator.

This shows the naive "induction via diagonal-block injectivity" cannot close;
the off-diagonal +e block does real work.

Trace: Triangle ⊕ U_{3,3} at (k=2, d=2), decompose by e=0, then e=0, then e=1.
After 3 deletions/contractions, we hit a pair (P, Q) on |E|=3 with ∂*: Y_k=2 → Y_{k+1}=?, rank=1.
"""
from __future__ import annotations
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from gpu_rank import Matroid
from test_block_decomp_recursive import (
    single_triangle, delete, contract, y_sets, paired_bipartite_entries, rank_of
)

P_MOD = 10007


def describe(M, name):
    print(f"  {name}: n={M.n}, rank={M.rank}, f={M.f}")
    # list independents by size
    for k in range(M.rank + 1):
        sets = sorted([sorted(s) for s in M.by_size.get(k, [])])
        print(f"     |·|={k}: {sets[:8]}{' ...' if len(sets) > 8 else ''}  (total {len(sets)})")


def show_paired_operator(P, Q, k, label):
    print(f"\n  Paired operator {label}: Y_{k}(P,Q) → Y_{k+1}(P,Q)")
    Yk = y_sets(P, Q, k)
    Ykp1 = y_sets(P, Q, k + 1)
    print(f"    Y_{k}    = {[sorted(s) for s in Yk]}  (count {len(Yk)})")
    print(f"    Y_{k+1}  = {[sorted(s) for s in Ykp1]}  (count {len(Ykp1)})")
    rows, cols, vals = paired_bipartite_entries(Yk, Ykp1, P.n)
    r = rank_of(rows, cols, vals, len(Ykp1), len(Yk))
    inj = (r == len(Yk))
    print(f"    rank = {r}  [{'INJ' if inj else f'col-kernel dim {len(Yk)-r}'}]")

    # Print the matrix explicitly
    print(f"    Matrix (rows = Y_{k+1}, cols = Y_{k}):")
    mat = [[0] * len(Yk) for _ in range(len(Ykp1))]
    for r_i, c_i, v in zip(rows, cols, vals):
        mat[r_i][c_i] = (mat[r_i][c_i] + v) % P_MOD
    header = "         " + " ".join(f"{i:>4d}" for i in range(len(Yk)))
    print(header)
    for i, row in enumerate(mat):
        print(f"      {i:2d}: " + " ".join(f"{v:>4d}" for v in row) + f"   ← {sorted(Ykp1[i])}")
    return Yk, Ykp1, mat, r


def main():
    print("=" * 70)
    print("Tracing the depth-3 failure on Triangle ⊕ U_{3,3}, (k=2, d=2)")
    print("=" * 70)
    N = single_triangle(3)
    print("\nStart: matroid N = Triangle ⊕ U_{3,3}")
    print(f"  Triangle on {{0,1,2}}, free elements {{3,4,5}}")

    # Depth 0: pair (N, N), k=2, d=2.
    # Decompose by e=0 → take (N\0, N/0) branch (first sub-block, grade k=2).
    print("\n--- Step: decompose pair (N, N) at k=2 by e=0, take (N\\0, N/0) at k=2 ---")
    P1 = delete(N, 0)
    Q1 = contract(N, 0)
    print(f"  P1 = N\\0:  re-indexed elements 0..{P1.n-1} (= old 1,2,3,4,5)")
    describe(P1, "P1 = N\\0")
    describe(Q1, "Q1 = N/0")

    show_paired_operator(P1, Q1, 2, "(P1, Q1) at k=2  (depth 1)")

    # Depth 1: pair (P1, Q1) on E_1 = {0,...,4}. Decompose by e=0.
    print("\n--- Step: decompose pair (P1, Q1) at k=2 by e=0, take (P1\\0, Q1/0) at k=2 ---")
    P2 = delete(P1, 0)
    Q2 = contract(Q1, 0)
    describe(P2, "P2 = P1\\0")
    describe(Q2, "Q2 = Q1/0")

    show_paired_operator(P2, Q2, 2, "(P2, Q2) at k=2  (depth 2)")

    # Depth 2: pair (P2, Q2) on E_2 = {0,1,2,3}. Decompose by e=1.
    print("\n--- Step: decompose pair (P2, Q2) at k=2 by e=1, take (P2\\1, Q2/1) at k=2 ---")
    P3 = delete(P2, 1)
    Q3 = contract(Q2, 1)
    describe(P3, "P3 = P2\\1")
    describe(Q3, "Q3 = Q2/1")

    show_paired_operator(P3, Q3, 2, "(P3, Q3) at k=2  (depth 3) — THIS IS THE FAILURE")

    # Also show the other sibling block at the same depth (∂*_{has e}: P2/1, Q2\1, grade k-1=1).
    print("\n--- Sibling block at depth 3: (P2/1, Q2\\1) at k=1 ---")
    P3s = contract(P2, 1)
    Q3s = delete(Q2, 1)
    show_paired_operator(P3s, Q3s, 1, "(P2/1, Q2\\1) at k=1  — sibling block")


if __name__ == "__main__":
    main()
