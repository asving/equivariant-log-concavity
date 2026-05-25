"""Sanity check: verify bipartite incidence matrix rank for various matroids.
We test Mason's claim 'rank = min(f_k, f_{k+1})' against actual rank.

If it fails, then the claim is NOT a theorem of matroids and our PREPRINT_DRAFT's
Theorem 4 was bogus.
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from sparse_rank import sparse_rank_modp, M_Kn
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


def partial_rank_modp(N, k, P=10007):
    """Rank of partial : Indep_k(N) -> Indep_{k+1}(N) mod P."""
    indep_k = sorted(N.by_size.get(k, []), key=lambda s: sorted(s))
    indep_k1 = sorted(N.by_size.get(k+1, []), key=lambda s: sorted(s))
    idx_kp1 = {A: i for i, A in enumerate(indep_k1)}
    rows, cols, vals = [], [], []
    for j, A in enumerate(indep_k):
        for i in range(N.n):
            if i in A: continue
            Ap = A | frozenset([i])
            if Ap in idx_kp1:
                rows.append(idx_kp1[Ap])
                cols.append(j)
                vals.append(1)
    rk = sparse_rank_modp(rows, cols, vals, len(indep_k1), len(indep_k), P, verbose=False)
    return rk, len(indep_k), len(indep_k1)


def check(N, label, ks):
    print(f"\n=== {label}: n={N.n}, rank={N.rank}, f={N.f} ===")
    for k in ks:
        rk, fk, fk1 = partial_rank_modp(N, k)
        expected = min(fk, fk1)
        marker = "✓ FULL" if rk == expected else "✗ DEFICIT"
        print(f"  k={k}: f_k={fk:5d}  f_{{k+1}}={fk1:5d}  rank(∂)={rk:5d}  "
              f"min(fk,fk1)={expected:5d}  {marker}  deficit={expected-rk}")


if __name__ == "__main__":
    # Sanity check on uniforms (Mason's claim should hold).
    for r, n in [(3, 4), (3, 5), (3, 6), (4, 6), (4, 7), (4, 8), (5, 8), (5, 10)]:
        check(Matroid.uniform(r, n), f"U_{{{r},{n}}}", list(range(0, r)))

    # M(K_n)
    for nv in [4, 5, 6]:
        M = M_Kn(nv)
        check(M, f"M(K_{nv})", list(range(0, M.rank)))

    # The failing simple matroid N1.
    M = M_Kn(6)
    N1 = make_NC_U(M, frozenset(), frozenset(range(8)))
    check(N1, "N1 = M(K_6)|_{0..7}", list(range(0, N1.rank)))

    # And N2.
    N2 = make_NC_U(M, frozenset(), frozenset(list(range(7)) + [9]))
    check(N2, "N2 = M(K_6)|_{0..6,9}", list(range(0, N2.rank)))
