"""Revised proof strategy: characterize ker(∂* on ℝ^{Indep_k(N)}) and check
whether it's disjoint from ℝ^{X_k(N)}.

Conjecture (Kernel-disjoint-from-X): For matroid N on E with rank r' >= k+d,
n' = 2k+d, d >= 2:
   ker(∂*: ℝ^{Indep_k(N)} → ℝ^{Indep_{k+1}(N)}) projects to {0} on the X_k
   coordinates, i.e., ker(∂*) ⊆ ℝ^{Indep_k(N) \ X_k(N)} (or in matroid language,
   the kernel is supported on indep_k sets whose complement is DEPENDENT in N).

If proven, this immediately gives Theorem 4'.

We test this by:
  (1) For each test matroid N (esp the failing ones), compute ker(∂*) explicitly
      over Q (rationals).
  (2) Project to X_k coordinates and check the projection is 0.
  (3) Additionally inspect WHICH non-X_k indep sets appear in the kernel support.
"""
import sys, time
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
import numpy as np
from sparse_rank import M_Kn
from gpu_rank import Matroid


def make_NC_U(M, C, U):
    UC = U - C
    UC_list = sorted(UC)
    idx = {e: i for i, e in enumerate(UC_list)}
    n_new = len(UC_list)
    indep = []
    for k_ in range(n_new + 1):
        for A in combinations(UC_list, k_):
            if (frozenset(A) | C) in M.indep:
                indep.append(frozenset(idx[e] for e in A))
    return Matroid(n_new, indep)


def X_k(N, k):
    E = frozenset(range(N.n))
    out = []
    for A in combinations(range(N.n), k):
        A = frozenset(A)
        if A not in N.indep: continue
        if (E - A) not in N.indep: continue
        out.append(A)
    return out


def build_partial(N, k):
    """Build the matrix M of partial^* on Indep_k -> Indep_{k+1} as a numpy
    int matrix.  Rows = Indep_{k+1}, cols = Indep_k.
    Returns (M, Indep_k_list, Indep_{k+1}_list)."""
    indep_k = sorted(N.by_size.get(k, []), key=lambda S: sorted(S))
    indep_k1 = sorted(N.by_size.get(k+1, []), key=lambda S: sorted(S))
    idx_kp1 = {A: i for i, A in enumerate(indep_k1)}
    n_rows, n_cols = len(indep_k1), len(indep_k)
    M = np.zeros((n_rows, n_cols), dtype=np.int64)
    for j, A in enumerate(indep_k):
        for i in range(N.n):
            if i in A: continue
            Ap = A | frozenset([i])
            if Ap in idx_kp1:
                M[idx_kp1[Ap], j] = 1
    return M, indep_k, indep_k1


def main():
    print("=" * 70)
    print("Kernel-disjoint-from-X test (revised Theorem 4' strategy)")
    print("=" * 70)

    M = M_Kn(6)
    cases = [
        ("N1 = M(K_6)|_{0..7}",  frozenset(), frozenset(range(8)), 3),
        ("N2 = M(K_6)|_{0..6,9}", frozenset(), frozenset(list(range(7)) + [9]), 3),
    ]

    for label, C, U, k in cases:
        print(f"\n--- {label}, k={k} ---")
        N = make_NC_U(M, C, U)
        print(f"  N: n'={N.n}, rank={N.rank}, f={N.f}")
        partial, indep_k_list, indep_k1_list = build_partial(N, k)
        print(f"  partial: shape {partial.shape}  (rows = Indep_{k+1}, cols = Indep_{k})")

        # Compute kernel of partial over Q (via float SVD, then validate).
        # For exactness use scipy or sympy if needed; numpy SVD should be fine for small.
        # Better: use rational arithmetic via sympy.
        from sympy import Matrix as SyMatrix, Rational
        SM = SyMatrix(partial.tolist())
        ker = SM.nullspace()
        print(f"  ker dim = {len(ker)}")

        # X_k indices.
        Xk = X_k(N, k)
        idx_k = {A: i for i, A in enumerate(indep_k_list)}
        Xk_indices = sorted(idx_k[A] for A in Xk)
        print(f"  |X_k| = {len(Xk_indices)}  (of {len(indep_k_list)} indep_k)")

        # Check: each kernel vector projects to 0 on X_k indices.
        ker_proj_zero = True
        for kvec_idx, kvec in enumerate(ker):
            v = [Rational(kvec[i, 0]) for i in range(kvec.rows)]
            nonzero_idx = [i for i, x in enumerate(v) if x != 0]
            X_in_supp = [i for i in nonzero_idx if i in set(Xk_indices)]
            nonX_in_supp = [i for i in nonzero_idx if i not in set(Xk_indices)]
            print(f"  kernel vec #{kvec_idx}: |supp|={len(nonzero_idx)}, in X_k: {len(X_in_supp)}, not in X_k: {len(nonX_in_supp)}")
            if X_in_supp:
                ker_proj_zero = False
                # Show one or two examples.
                for i in X_in_supp[:3]:
                    print(f"    *** kernel touches X_k at index {i}, set {sorted(indep_k_list[i])}, coeff={v[i]}")
        if ker_proj_zero:
            print(f"  [✓] Kernel is supported ENTIRELY outside X_k (Conjecture holds)")
        else:
            print(f"  [✗] Kernel touches X_k somewhere (Conjecture would fail)")

        # Now: the conjecture says kernel ⊆ ℝ^{Indep_k \ X_k}.  We've checked the projection.
        # Let's also see: which non-X_k indep sets are "involved"?  Specifically, look at
        # one kernel vector and decode its supp into matroid terms.
        if ker:
            v = [Rational(ker[0][i, 0]) for i in range(ker[0].rows)]
            print(f"\n  Decoding kernel vector #0:")
            nonzero = [(i, v[i]) for i in range(len(v)) if v[i] != 0]
            for i, c in nonzero[:10]:
                A = indep_k_list[i]
                in_X = i in set(Xk_indices)
                comp_indep = (frozenset(range(N.n)) - A) in N.indep
                print(f"    A = {sorted(A)}  coeff={c}  complement_indep={comp_indep}  in_X={in_X}")
            if len(nonzero) > 10:
                print(f"    ... and {len(nonzero) - 10} more entries")


if __name__ == "__main__":
    main()
