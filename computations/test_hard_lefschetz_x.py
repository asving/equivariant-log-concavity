"""Cheap algebraic check: does the X-restriction R(M)|_X satisfy Hard Lefschetz?

For a matroid M of rank r on n elements, the X-vector is supported on k ∈ [n-r, r]
and satisfies |X_k| = |X_{n-k}| by complementation A ↔ E\A.

Hard Lefschetz statement on R(M)|_X:
  ∂*^{n-2k}: X_k → X_{n-k} is an isomorphism for every k ≤ n/2 with X_k ≠ 0.

If this holds across many test matroids:
  → R(M)|_X has Poincaré duality (Gorenstein-like).
  → Bilinear pairing on the X-restriction is non-degenerate.
  → Plausible target for compact manifold realization.

If it fails:
  → R(M)|_X is not Gorenstein.
  → Even the X-restricted geometric route is blocked.
  → Returns us toward the combinatorial Hodge theory approach.

We test by composing the X-bipartite operators and checking full rank mod p.
"""

from __future__ import annotations
import sys
import numpy as np
from itertools import combinations
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid, M_Kn, Vamos


P = 10007


def x_sets(M, k):
    E = frozenset(range(M.n))
    return [A for A in M.by_size.get(k, []) if (E - A) in M.indep]


def bipartite_matrix(M, k):
    """Single-step ∂*: X_k → X_{k+1} as integer numpy matrix."""
    Xk = x_sets(M, k)
    Xk1 = x_sets(M, k + 1)
    if not Xk or not Xk1:
        return np.zeros((len(Xk1), len(Xk)), dtype=np.int64)
    idx = {A: i for i, A in enumerate(Xk1)}
    mat = np.zeros((len(Xk1), len(Xk)), dtype=np.int64)
    for j, A in enumerate(Xk):
        for i in range(M.n):
            if i in A:
                continue
            Ap = A | frozenset([i])
            if Ap in idx:
                mat[idx[Ap], j] += 1
    return mat


def L_power(M, k_start, power):
    """∂*^power: X_{k_start} → X_{k_start + power}."""
    n_k = len(x_sets(M, k_start))
    if power == 0:
        return np.eye(n_k, dtype=np.int64)
    result = bipartite_matrix(M, k_start)
    for j in range(1, power):
        nxt = bipartite_matrix(M, k_start + j)
        result = (nxt @ result) % P  # keep entries small
    return result


def rank_modp(mat):
    A = (mat.astype(np.int64) % P).copy()
    m, n = A.shape
    if m == 0 or n == 0:
        return 0
    r = 0
    for c in range(n):
        if r >= m:
            break
        col = A[r:, c]
        nz = np.nonzero(col)[0]
        if len(nz) == 0:
            continue
        piv_row = r + nz[0]
        if piv_row != r:
            tmp = A[r].copy()
            A[r] = A[piv_row]
            A[piv_row] = tmp
        inv = pow(int(A[r, c]), P - 2, P)
        A[r] = (A[r] * inv) % P
        for k in range(m):
            if k != r and A[k, c] != 0:
                A[k] = (A[k] - A[k, c] * A[r]) % P
        r += 1
    return r


def test_hard_lefschetz(M, label):
    print(f"\n{'='*60}")
    print(f"  {label}: n={M.n}, rank={M.rank}")
    print(f"{'='*60}")
    n, r = M.n, M.rank
    xv = [len(x_sets(M, k)) for k in range(n + 1)]
    support = [k for k in range(n + 1) if xv[k] > 0]
    if not support:
        print("  X-vector zero — skipping.")
        return None
    xv_disp = xv[support[0]:support[-1]+1]
    print(f"  X-vector (support [{support[0]},{support[-1]}]): {xv_disp}")

    # Single-step ∂* injectivity check (sanity)
    print(f"  Single-step ∂* injectivity:")
    for k in support:
        if k + 1 not in support:
            break
        mat = bipartite_matrix(M, k)
        rk = rank_modp(mat)
        flag = "INJ" if rk == xv[k] else f"ker={xv[k] - rk}"
        if k <= n / 2:
            print(f"    ∂*: X_{k}({xv[k]}) → X_{k+1}({xv[k+1]}): rank={rk}  [{flag}]")

    # Hard Lefschetz: ∂*^{n-2k}: X_k → X_{n-k}
    print(f"  Hard Lefschetz test:")
    all_iso = True
    middle = n // 2
    for k in support:
        target = n - k
        if target <= k:
            continue
        if target not in support:
            continue
        power = target - k
        if xv[k] != xv[target]:
            print(f"    k={k}→{target}: |X_k|={xv[k]} vs |X_{{n-k}}|={xv[target]} -- SYMMETRY FAILS")
            all_iso = False
            continue
        mat = L_power(M, k, power)
        rk = rank_modp(mat)
        flag = "ISO ✓" if rk == xv[k] else f"NOT ISO (rank {rk}/{xv[k]})"
        print(f"    ∂*^{power}: X_{k}({xv[k]}) → X_{target}({xv[target]}): rank={rk}  [{flag}]")
        if rk != xv[k]:
            all_iso = False

    verdict = "HL HOLDS" if all_iso else "HL FAILS"
    print(f"  → {verdict} on R(M)|_X")
    return all_iso


def free_sum(M, k):
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
    for k in range(n + 1):
        for S in combinations(range(n), k):
            S = frozenset(S)
            if {0, 1, 2}.issubset(S):
                continue
            indep.append(S)
    return Matroid(n, indep)


def main():
    matroids = [
        # Paving (known: HL holds via KW proof; sanity check)
        (Matroid.uniform(3, 4), "U(3,4)  [uniform/paving]"),
        (Matroid.uniform(4, 6), "U(4,6)  [uniform/paving]"),
        (Matroid.uniform(5, 8), "U(5,8)  [uniform/paving]"),
        # Non-paving examples we've tested before
        (single_triangle(2), "Triangle ⊕ U_{2,2}  [non-paving]"),
        (single_triangle(3), "Triangle ⊕ U_{3,3}  [non-paving]"),
        (single_triangle(4), "Triangle ⊕ U_{4,4}  [non-paving]"),
        (single_triangle(5), "Triangle ⊕ U_{5,5}  [non-paving]"),
        (free_sum(M_Kn(4), 3), "M(K_4) ⊕ U_{3,3}  [non-paving graphic]"),
        (free_sum(M_Kn(4), 4), "M(K_4) ⊕ U_{4,4}  [non-paving graphic]"),
        # Vámos: rank 4, n=8, X-support [4, 4] only (singleton), trivial HL
        (Vamos(), "Vámos V_8  [non-paving, X trivial]"),
    ]
    results = []
    for M, label in matroids:
        r = test_hard_lefschetz(M, label)
        results.append((label, r))
    print(f"\n{'='*60}\nSUMMARY")
    for label, r in results:
        marker = "✓" if r is True else ("✗" if r is False else "—")
        print(f"  {marker}  {label}")


if __name__ == "__main__":
    main()
