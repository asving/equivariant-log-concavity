"""Verify whether L_amb(I_M^source) ⊆ I_M^target — the descent claim used in PAPER.md §4.5.

For paving M = U_{5,8} + 1 CH F = {0,1,2,3,4} at (m=3, d=2):
- I_M^source has dim 56 (= contributions from y_F where F = CH).
- I_M^target has dim 0 (= no ideal at target degree).

Take a specific v = x_S ⊗ y_F ∈ I_M^source. Compute L_amb(v) and check if it's in I_M^target.
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from sparse_rank import sparse_rank_modp
from gpu_rank import Matroid


def make_uniform_with_chs(r, n, chs):
    indep = []
    for k in range(r + 1):
        for S in combinations(range(n), k):
            S = frozenset(S)
            if k == r and S in chs:
                continue
            indep.append(S)
    return Matroid(n, indep)


def main():
    n, r = 8, 5
    F = frozenset({0, 1, 2, 3, 4})
    M = make_uniform_with_chs(r, n, {F})
    print(f"M = U_{{{r},{n}}} + 1 CH F = {sorted(F)}")
    print(f"f-vector: {M.f}")
    print(f"rank: {M.rank}")

    m, d = 3, 2
    # Take v = x_S ⊗ y_F where S = {5,6,7} (disjoint from F)
    S = frozenset({5, 6, 7})
    T = F
    print(f"\nv = x_{sorted(S)} ⊗ y_{sorted(T)}")
    print(f"  |S| = {len(S)}, |T| = {len(T)}")
    print(f"  S indep? {S in M.indep}, T indep? {T in M.indep}")
    print(f"  T = F is a CH (= dependent in M)")
    print(f"  Hence y_T = 0 in R^∨(M), so v ∈ I_M^source")

    # Apply L_amb: L(x_S ⊗ y_T) = Σ_{i ∈ T\S} x_{S∪i} ⊗ y_{T\i}
    print(f"\nL_amb(v) = Σ_{{i ∈ T\\S}} x_{{S∪i}} ⊗ y_{{T\\i}}")
    summands = []
    for i in sorted(T - S):
        Sp = S | frozenset([i])
        Tp = T - frozenset([i])
        in_R = Sp in M.indep
        in_Rstar = Tp in M.indep
        in_ideal_target = (not in_R) or (not in_Rstar)
        print(f"  i={i}: x_{sorted(Sp)} ⊗ y_{sorted(Tp)}")
        print(f"    S' = {sorted(Sp)} indep? {in_R}")
        print(f"    T' = {sorted(Tp)} indep? {in_Rstar}")
        print(f"    Summand in I_M^target (= S' or T' dep)? {in_ideal_target}")
        summands.append((i, Sp, Tp, in_R, in_Rstar, in_ideal_target))

    # Verdict
    all_in_ideal = all(s[5] for s in summands)
    any_outside = not all_in_ideal
    print(f"\n--- Verdict ---")
    print(f"All L_amb(v) summands in I_M^target? {all_in_ideal}")
    if any_outside:
        outside = [s for s in summands if not s[5]]
        print(f"At least one summand NOT in I_M^target: {len(outside)} of {len(summands)}")
        print(f"This means L_amb(I_M^source) ⊄ I_M^target.")
        print(f"The §4.5 'Gui-Xiong descent' proof is INVALID.")
    else:
        print(f"All summands in I_M^target — §4.5 descent claim holds for this example.")


if __name__ == "__main__":
    main()
