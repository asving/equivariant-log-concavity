"""Test if G̃_M(z_1, ..., z_n; w_1, ..., w_n) := sum_{(A, B) ord. indep partition} z^A w^B
is Lorentzian in 2n variables for small matroids.

Method: For a degree-d homogeneous polynomial p in N variables, p is Lorentzian iff:
  1. coefficients are non-negative (automatic for our p),
  2. support is M-convex (we don't check this — would need matroid hypothesis),
  3. For every (d-2)-fold partial derivative D, the Hessian of D · p has at most one
     positive eigenvalue.

For G̃_M of degree n in 2n vars: (n-2)-fold partials give quadratic polynomials.
We compute the Hessian of each such quadratic and check its signature.

If Lorentzian: every Hessian has at most 1 positive eigenvalue.
If NOT: at least one Hessian has 2+ positive eigenvalues.
"""
import sys
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


def indep_partitions(M):
    """List all (A, B) with A ⊔ B = E, both indep in M."""
    E = set(range(M.n))
    parts = []
    for k_ in range(M.n + 1):
        for A_tup in combinations(range(M.n), k_):
            A = frozenset(A_tup); B = frozenset(E - A)
            if A in M.indep and B in M.indep:
                parts.append((A, B))
    return parts


def compute_hessian(M, I_z, I_w):
    """Given I_z, I_w (disjoint subsets of E, |I_z|+|I_w|=n-2),
    compute the 4x4 Hessian of ∂_{I_z, I_w} G̃_M.
    Returns the 4 coefficients (c_AA, c_AB, c_BA, c_BB) and the eigenvalues.
    Free indices = E \ (I_z ∪ I_w) = {m_1, m_2}."""
    E = set(range(M.n))
    fixed = I_z | I_w
    free = sorted(E - fixed)
    assert len(free) == 2, f"need exactly 2 free, got {len(free)}"
    m1, m2 = free

    # Compute c_{AA}, c_{AB}, c_{BA}, c_{BB}
    # c_AA: partition with m1, m2 both in A, I_z subset A, I_w subset B
    #   A = I_z ∪ {m1, m2}, B = I_w
    A_aa = frozenset(I_z) | {m1, m2}; B_aa = frozenset(I_w)
    A_ab = frozenset(I_z) | {m1}; B_ab = frozenset(I_w) | {m2}
    A_ba = frozenset(I_z) | {m2}; B_ba = frozenset(I_w) | {m1}
    A_bb = frozenset(I_z); B_bb = frozenset(I_w) | {m1, m2}

    c_aa = 1 if (A_aa in M.indep and B_aa in M.indep) else 0
    c_ab = 1 if (A_ab in M.indep and B_ab in M.indep) else 0
    c_ba = 1 if (A_ba in M.indep and B_ba in M.indep) else 0
    c_bb = 1 if (A_bb in M.indep and B_bb in M.indep) else 0

    # Build Hessian. Variable order: (z_{m1}, w_{m1}, z_{m2}, w_{m2})
    # Quadratic: c_aa z_{m1} z_{m2} + c_ab z_{m1} w_{m2} + c_ba w_{m1} z_{m2} + c_bb w_{m1} w_{m2}.
    H = np.array([
        [0, 0, c_aa, c_ab],
        [0, 0, c_ba, c_bb],
        [c_aa, c_ba, 0, 0],
        [c_ab, c_bb, 0, 0],
    ], dtype=float)
    eigs = np.linalg.eigvalsh(H)
    return (c_aa, c_ab, c_ba, c_bb), eigs


def lorentzian_test(M, label):
    print(f"\n=== {label}: n={M.n}, rank={M.rank}, f={M.f} ===")
    failures = 0
    total = 0
    # Enumerate all (I_z, I_w) with disjoint, |I_z|+|I_w|=n-2
    E = list(range(M.n))
    n = M.n
    if n < 2:
        print(f"  n too small, skip"); return
    if n - 2 == 0:
        # Special case: no differentiation, polynomial itself is degree n with 2n vars.
        # Need to check its Hessian.
        print(f"  n={n}=2, trivial case (G̃_M itself is degree 2). Skipping.")
        return

    # All ways to choose I_z ⊆ E and I_w ⊆ E \ I_z with |I_z| + |I_w| = n-2
    found_any = False
    bad_cases = []
    for size_z in range(n - 1):
        size_w = (n - 2) - size_z
        if size_w < 0 or size_w > n - size_z: continue
        for Iz_tup in combinations(E, size_z):
            Iz = frozenset(Iz_tup)
            rest = [e for e in E if e not in Iz]
            for Iw_tup in combinations(rest, size_w):
                Iw = frozenset(Iw_tup)
                total += 1
                coeffs, eigs = compute_hessian(M, Iz, Iw)
                # Count positive eigenvalues
                pos = sum(1 for e in eigs if e > 1e-9)
                found_any = True
                if pos > 1:
                    failures += 1
                    if len(bad_cases) < 5:
                        bad_cases.append((Iz, Iw, coeffs, eigs.tolist(), pos))
    print(f"  Tested {total} (n-2)-fold partials")
    print(f"  Lorentzian failures (>1 positive eigenvalue): {failures}")
    if bad_cases:
        print(f"  First bad cases:")
        for Iz, Iw, c, eigs, pos in bad_cases:
            print(f"    I_z={sorted(Iz)}, I_w={sorted(Iw)}: c=(AA={c[0]}, AB={c[1]}, BA={c[2]}, BB={c[3]}), eigs={['%.3f'%e for e in eigs]}, #pos={pos}")
    if failures == 0:
        print(f"  ✓ G̃_M is Lorentzian on these tests.")
    else:
        print(f"  ✗ G̃_M is NOT Lorentzian.")


if __name__ == "__main__":
    # Smallest non-boolean matroid: U_{2,3}
    lorentzian_test(Matroid.uniform(2, 3), "U_{2,3}")
    # Boolean U_{4,4}
    lorentzian_test(Matroid.uniform(4, 4), "U_{4,4} (boolean)")
    # U_{3, 4}
    lorentzian_test(Matroid.uniform(3, 4), "U_{3,4}")
    # U_{3, 5}
    lorentzian_test(Matroid.uniform(3, 5), "U_{3,5}")
    # U_{4, 6}
    lorentzian_test(Matroid.uniform(4, 6), "U_{4,6}")
    # M(K_4)
    lorentzian_test(M_Kn(4), "M(K_4)")
    # The failing N1
    M6 = M_Kn(6)
    N1 = make_NC_U(M6, frozenset(), frozenset(range(8)))
    lorentzian_test(N1, "N1 = M(K_6)|_{0..7}")
