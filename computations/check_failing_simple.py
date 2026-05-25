"""Check: does Theorem 4' (|X_k| <= |X_{k+1}|) still hold on the SIMPLE matroid
where Simple-Lemma-5 fails?

The failing case: N = M(K_6) restricted to edges {0,1,2,3,4,5,6,7} (8 edges of K_6),
which is a simple graphic matroid with f_3 = 53 > 52 = f_4 (so Lemma 5 fails).

We compute:
  |X_k(N)| = #{A subset of E(N), |A|=k, A indep, complement indep}
  |X_{k+1}(N)| similar.
  Plus the bipartite incidence rank.
"""
import sys, time
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from sparse_rank import M_Kn
from gpu_rank import Matroid


def make_NC_U(M, C, U):
    UC = U - C
    UC_list = sorted(UC)
    idx = {e: i for i, e in enumerate(UC_list)}
    n_new = len(UC_list)
    indep = []
    for k in range(n_new + 1):
        for A in combinations(UC_list, k):
            if (frozenset(A) | C) in M.indep:
                indep.append(frozenset(idx[e] for e in A))
    return Matroid(n_new, indep)


def X_k(N, k):
    """Set of A subset of [N.n], |A|=k, A indep, complement (E\\A) indep."""
    out = []
    E = frozenset(range(N.n))
    for A in combinations(range(N.n), k):
        A = frozenset(A)
        if A not in N.indep: continue
        comp = E - A
        if comp not in N.indep: continue
        out.append(A)
    return out


def bipartite_incidence_rank(N, X_k_list, X_kp1_list, P=10007):
    """Build bipartite incidence (A -> A+i) on X_k -> X_{k+1}, compute rank mod P."""
    from sparse_rank import sparse_rank_modp
    X_kp1_idx = {A: i for i, A in enumerate(X_kp1_list)}
    rows, cols, vals = [], [], []
    for j, A in enumerate(X_k_list):
        for i in range(N.n):
            if i in A: continue
            Ap = A | {i}
            if Ap not in N.indep: continue
            if Ap not in X_kp1_idx: continue  # land in X_{k+1}
            rows.append(X_kp1_idx[Ap])
            cols.append(j)
            vals.append(1)
    if not rows:
        return 0
    r = sparse_rank_modp(rows, cols, vals, len(X_kp1_list), len(X_k_list), P, verbose=False)
    return r


def main():
    M = M_Kn(6)
    print(f"M(K_6): n={M.n}, rank={M.rank}", flush=True)
    # The failing orbit:
    C = frozenset()
    U = frozenset({0, 1, 2, 3, 4, 5, 6, 7})
    N = make_NC_U(M, C, U)
    print(f"N = M(K_6)|_{{0,...,7}}: n'={N.n}, rank={N.rank}, f={N.f}", flush=True)
    print(f"  Is simple? loops: {[i for i in range(N.n) if frozenset([i]) not in N.indep]}, "
          f"parallels: {[(i,j) for i,j in combinations(range(N.n),2) if frozenset([i,j]) not in N.indep]}",
          flush=True)

    # k=3, d=2.
    k, d = 3, 2
    X3 = X_k(N, k)
    X4 = X_k(N, k+1)
    print(f"\n(k, d) = ({k}, {d}):  n'={N.n}=2k+d, r'={N.rank}>=k+d={k+d}")
    print(f"  f_k(N) = {len(N.by_size.get(k,[]))}  f_{{k+1}}(N) = {len(N.by_size.get(k+1,[]))}")
    print(f"  Lemma 5 (f_k <= f_{{k+1}}): {'✓' if len(N.by_size.get(k,[])) <= len(N.by_size.get(k+1,[])) else '✗ FAILS'}")
    print(f"  |X_k(N)| = {len(X3)}  |X_{{k+1}}(N)| = {len(X4)}")
    print(f"  Theorem 4' dim (|X_k| <= |X_{{k+1}}|): {'✓' if len(X3) <= len(X4) else '✗'}")

    rk = bipartite_incidence_rank(N, X3, X4)
    print(f"  Bipartite incidence rank (X_k -> X_{{k+1}}): {rk}  / source dim {len(X3)}  "
          f"{'INJ ✓' if rk == len(X3) else 'NOT INJ ✗'}")

    # Also the second failing case.
    U2 = frozenset({0, 1, 2, 3, 4, 5, 6, 9})
    print(f"\n--- Second failing case: U={{0,1,2,3,4,5,6,9}} ---")
    N2 = make_NC_U(M, C, U2)
    print(f"N = M(K_6)|_U: n'={N2.n}, rank={N2.rank}, f={N2.f}")
    print(f"  Is simple? loops: {[i for i in range(N2.n) if frozenset([i]) not in N2.indep]}, "
          f"parallels: {[(i,j) for i,j in combinations(range(N2.n),2) if frozenset([i,j]) not in N2.indep]}")
    X3b = X_k(N2, 3)
    X4b = X_k(N2, 4)
    print(f"  f_3={len(N2.by_size.get(3,[]))}, f_4={len(N2.by_size.get(4,[]))}")
    print(f"  |X_3|={len(X3b)}, |X_4|={len(X4b)}")
    rk2 = bipartite_incidence_rank(N2, X3b, X4b)
    print(f"  Bipartite rank: {rk2} / {len(X3b)}  {'INJ ✓' if rk2 == len(X3b) else 'NOT INJ ✗'}")

    # Decode the underlying graph.
    edges = list(combinations(range(6), 2))
    print(f"\nDecode: M(K_6)|_{{0,...,7}} edges = {[edges[i] for i in range(8)]}")
    print(f"        M(K_6)|_U2 edges = {[edges[i] for i in sorted(U2)]}")


if __name__ == "__main__":
    main()
