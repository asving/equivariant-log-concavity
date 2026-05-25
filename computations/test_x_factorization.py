"""Investigate whether R(M)|_X factors / has product structure.

For direct sums M = N ⊕ U_{k,k}, we should get X-polynomial(M) = X-polynomial(N) × (1+t)^k.

Beyond that: do the X-vectors of arbitrary matroids factor as products of smaller polynomials?
If yes, that suggests R(M)|_X = H*(Y_N × (P^1)^k) for some Y_N.

Also: compute eigenvalues of the Lefschetz operator L: X_k → X_{k+1} on the X-restriction
of small matroids. If eigenvalues are all positive → Kähler-like. If mixed signs →
non-Kähler Lefschetz (more interesting / harder to realize geometrically).
"""

from __future__ import annotations
import sys
import numpy as np
from itertools import combinations
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid, M_Kn, Vamos
from test_hard_lefschetz_x import (
    x_sets, bipartite_matrix, free_sum, single_triangle,
)


def factor_polynomial(coeffs):
    """Try to factor a polynomial Σ coeffs[i] t^i as a × (1+t)^k × b(t).
    Return (a, k, b_coeffs) if factorization found, else None.

    Repeatedly divide by (1+t) while possible (= coefficient list is "binomial-divisible").
    """
    c = list(coeffs)
    k = 0
    while len(c) >= 2:
        # divide by (1+t): c_i / (1+t) gives new_c with c[0] / (1) ?
        # actually: if c(t) = (1+t)·d(t), then c[i] = d[i-1] + d[i].
        # given c, can we recover d? Yes via d[i] = Σ_{j=0..i} (-1)^j c[i-j]
        # but only if the recovered d has non-negative integer coefficients matching back.
        new_d = []
        running = 0
        for i in range(len(c)):
            running = c[i] - running
            new_d.append(running)
        # last entry: should be 0 if divisible (no remainder)
        if new_d[-1] != 0:
            break
        new_d = new_d[:-1]
        c = new_d
        k += 1
    # gcd of remaining coefficients
    from math import gcd
    g = abs(c[0])
    for v in c[1:]:
        g = gcd(g, abs(v))
    if g > 1:
        c_primitive = [v // g for v in c]
    else:
        c_primitive = c
    return g, k, c_primitive


def eigenvalues_of_L(M, k):
    """Compute eigenvalues of the (square) Lefschetz operator
    L^{n-2k}: X_k → X_{n-k} when |X_k| = |X_{n-k}|.
    """
    from test_hard_lefschetz_x import L_power
    n = M.n
    if k > n - k:
        return None
    Xk = x_sets(M, k)
    Xtgt = x_sets(M, n - k)
    if not Xk or len(Xk) != len(Xtgt):
        return None
    mat = L_power(M, k, n - 2 * k).astype(float)
    eigs = np.linalg.eigvals(mat)
    return sorted(np.real(eigs).round(6).tolist())


def report(M, label):
    print(f"\n{'='*60}")
    print(f"  {label}: n={M.n}, rank={M.rank}")
    print(f"{'='*60}")
    n = M.n
    xv = [len(x_sets(M, k)) for k in range(n + 1)]
    support = [k for k in range(n + 1) if xv[k] > 0]
    if not support:
        print("  X-vector zero — skip")
        return
    print(f"  X-vector: {xv[support[0]:support[-1]+1]}  (support [{support[0]},{support[-1]}])")

    # Try factoring: extract (1+t)^k factor
    full_coeffs = xv[support[0]:support[-1] + 1]
    a, k_factor, residual = factor_polynomial(full_coeffs)
    if k_factor > 0:
        # express residual as polynomial
        print(f"  X-poly = {a} · (1+t)^{k_factor} · ({' + '.join(f'{c}t^{i}' for i, c in enumerate(residual) if c != 0)})")
        print(f"    Interpretation: dim-matches {a} disjoint copies of (P^1)^{k_factor} × Y_core,")
        print(f"                    where Y_core has graded dims = {residual}")
    else:
        print(f"  X-poly does NOT factor (1+t) — no boolean-product simplification")

    # Eigenvalues of L^{n-2k}: X_k → X_{n-k} for k below midpoint with |X_k| = |X_{n-k}|
    mid = n // 2
    print(f"  Eigenvalues of L^{{n-2k}}: X_k → X_{{n-k}} (square Lefschetz operator):")
    for k in support:
        if k > mid:
            break
        target = n - k
        if target not in support:
            continue
        if xv[k] != xv[target]:
            continue
        eigs = eigenvalues_of_L(M, k)
        if eigs is None:
            continue
        # check signs
        pos = sum(1 for e in eigs if e > 0.001)
        neg = sum(1 for e in eigs if e < -0.001)
        zero = sum(1 for e in eigs if abs(e) <= 0.001)
        flag = "all positive ✓ (Kähler-like)" if neg == 0 and zero == 0 else \
               f"mixed signs (pos={pos}, neg={neg}, zero={zero}) — non-Kähler"
        # show first few distinct eigs
        distinct = sorted(set(round(e, 4) for e in eigs))
        if len(distinct) <= 6:
            disp = f"eigs = {distinct}"
        else:
            disp = f"eigs span [{min(eigs):.2f}, {max(eigs):.2f}], {len(distinct)} distinct"
        print(f"    k={k}: |X_k|={xv[k]}, {disp}  [{flag}]")


def main():
    matroids = [
        # Direct sum tests
        (single_triangle(0), "Triangle alone (3 elts, rank 2)"),
        (single_triangle(1), "Triangle ⊕ U_{1,1} (4 elts)"),
        (single_triangle(2), "Triangle ⊕ U_{2,2} (5 elts)"),
        (single_triangle(3), "Triangle ⊕ U_{3,3} (6 elts)"),
        # Uniform (no factorization expected)
        (Matroid.uniform(3, 4), "U(3,4)"),
        (Matroid.uniform(4, 6), "U(4,6)"),
        (Matroid.uniform(5, 8), "U(5,8)"),
        # M(K_4) variants
        (M_Kn(4), "M(K_4) alone"),
        (free_sum(M_Kn(4), 3), "M(K_4) ⊕ U_{3,3}"),
        (free_sum(M_Kn(4), 4), "M(K_4) ⊕ U_{4,4}"),
    ]
    for M, label in matroids:
        try:
            report(M, label)
        except Exception as ex:
            print(f"\nERROR on {label}: {ex}")
            import traceback; traceback.print_exc()


if __name__ == "__main__":
    main()
