"""Extract the sl(2)-Lefschetz decomposition of R(M)|_X.

If HL holds on R(M)|_X with operator L = ∂* and palindromic dims about n/2,
then R(M)|_X decomposes into Lefschetz strings (irreducible sl(2)-reps).
The "primitive" dimensions P_k = dim ker(L^{n-2k+1}: X_k → X_{n-k+1}) are
the count of strings whose lowest grade is k.

Each primitive vector v at grade k generates a Lefschetz string
v, Lv, L²v, ..., L^{n-2k}v of length n-2k+1, contributing 1 to each grade
in [k, n-k].

The triple of invariants (X-vector, primitive vector, string decomposition)
encodes the matroid's "X-restricted Hodge structure".

We compute primitive dimensions for our test matroids and look for
matroid-theoretic structure in the numbers.
"""

from __future__ import annotations
import sys
import numpy as np
from itertools import combinations
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid, M_Kn, Vamos
from test_hard_lefschetz_x import (
    x_sets, bipartite_matrix, L_power, rank_modp, P,
    free_sum, single_triangle,
)


def primitive_dim(M, k):
    """P_k = dim ker(L^{n-2k+1}: X_k → X_{n-k+1})."""
    n = M.n
    target = n - k + 1
    Xk = x_sets(M, k)
    if not Xk:
        return 0
    if target > n:
        return len(Xk)
    Xtgt = x_sets(M, target)
    if not Xtgt:
        return len(Xk)  # whole space is in kernel
    power = target - k
    if power <= 0:
        return 0
    mat = L_power(M, k, power)
    rk = rank_modp(mat)
    return len(Xk) - rk


def lefschetz_decomp(M, label):
    print(f"\n{'='*60}")
    print(f"  {label}: n={M.n}, rank={M.rank}")
    print(f"{'='*60}")
    n = M.n
    xv = [len(x_sets(M, k)) for k in range(n + 1)]
    support = [k for k in range(n + 1) if xv[k] > 0]
    if not support:
        print("  X-vector zero. Skipping.")
        return None
    mid = n // 2
    print(f"  X-vector at support [{support[0]},{support[-1]}]: {[xv[k] for k in support]}")
    print(f"  Midpoint n/2 = {n/2}")

    # Primitive dims for k from support[0] up to floor(n/2)
    prim = {}
    for k in support:
        if k > mid:
            break
        P_k = primitive_dim(M, k)
        prim[k] = P_k
    print(f"  Primitive dims P_k:")
    for k, p in sorted(prim.items()):
        weight = n - 2 * k  # Lefschetz string of "weight" weight, length weight+1
        length = weight + 1
        # Each P_k primitive element generates a string of length n-2k+1
        # spanning grades k, k+1, ..., n-k.
        print(f"    k={k}: P_k={p}  (each gives Lefschetz string of length {length}, weight {weight})")

    # Verify: X_d = Σ_{k ≤ min(d, n-d)} P_k for each d
    print(f"  Verification (X-vector reconstruction from primitives):")
    valid = True
    for d in support:
        if d > mid:
            # By palindrome symmetry, X_d = X_{n-d}
            equivalent_d = n - d
        else:
            equivalent_d = d
        expected = sum(prim.get(k, 0) for k in range(equivalent_d + 1) if k in prim)
        actual = xv[d]
        ok = expected == actual
        if not ok:
            valid = False
        marker = "✓" if ok else "✗"
        print(f"    {marker} X_{d}={actual}, Σ_{{k≤{equivalent_d}}} P_k={expected}")
    if valid:
        print(f"  → Lefschetz decomposition consistent with HL")
    else:
        print(f"  → Lefschetz decomposition INCONSISTENT — HL may not hold here")
    return prim


def main():
    matroids = [
        (Matroid.uniform(3, 4), "U(3,4)"),
        (Matroid.uniform(4, 6), "U(4,6)"),
        (Matroid.uniform(5, 8), "U(5,8)"),
        (single_triangle(2), "Triangle ⊕ U_{2,2}"),
        (single_triangle(3), "Triangle ⊕ U_{3,3}"),
        (single_triangle(4), "Triangle ⊕ U_{4,4}"),
        (free_sum(M_Kn(4), 3), "M(K_4) ⊕ U_{3,3}"),
        (free_sum(M_Kn(4), 4), "M(K_4) ⊕ U_{4,4}"),
    ]
    all_primitives = {}
    for M, label in matroids:
        prim = lefschetz_decomp(M, label)
        all_primitives[label] = (M, prim)

    print(f"\n{'='*60}")
    print(f"PATTERN HUNT — looking for structure in primitive dims")
    print(f"{'='*60}")
    for label, (M, prim) in all_primitives.items():
        if prim is None:
            continue
        # Format: (n, r) and primitive vector
        sorted_p = [prim[k] for k in sorted(prim)]
        keys = sorted(prim)
        print(f"  {label}: (n={M.n}, r={M.rank}) primitives at k={keys}: {sorted_p}")
        # Total primitive count
        print(f"    Σ P_k = {sum(sorted_p)}  (= dim of 'top' weight space = X_{{n/2}} if n even)")


if __name__ == "__main__":
    main()
