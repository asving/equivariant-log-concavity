"""Probe for adversarial matroids where Hall is tight.

We're looking for matroids on n=2k+d with d <= k (the "hard" regime) where
the bipartite graph (X_k, X_{k+1}) has many tight subsets, to understand what
structural fact prevents Hall failure.

In particular: matroids where forward-degree is exactly d (minimum) AND
back-degree is maximum (= k+1). The double-counting bound becomes tight
exactly at d|S| = (k+1)|N(S)|, hence |N(S)| = (d/(k+1))|S|.

For Hall to hold, we'd need additional structural input beyond degree bounds.
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from collections import defaultdict
from sparse_rank import M_Kn
from gpu_rank import Matroid, AG_n_2


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


def X_k_set(N, k):
    E = frozenset(range(N.n))
    out = []
    for A in combinations(range(N.n), k):
        A = frozenset(A)
        if A not in N.indep: continue
        if (E - A) not in N.indep: continue
        out.append(A)
    return out


def bipartite_degrees(N, k):
    """Compute forward and back degrees in G_X(k, k+1)."""
    Xk = X_k_set(N, k)
    Xkp1 = X_k_set(N, k+1)
    Xkp1_set = set(Xkp1)
    if not Xk or not Xkp1:
        return None
    fwd_deg = {}
    back_deg = defaultdict(int)
    for A in Xk:
        fwd_deg[A] = 0
        for i in range(N.n):
            if i in A: continue
            Ap = A | frozenset([i])
            if Ap in Xkp1_set:
                fwd_deg[A] += 1
                back_deg[Ap] += 1
    return Xk, Xkp1, fwd_deg, dict(back_deg)


def hopcroft_karp_matching(adj, left_set):
    matchR = {}
    def try_dfs(u, visited):
        for v in adj.get(u, []):
            if v in visited: continue
            visited.add(v)
            if v not in matchR or try_dfs(matchR[v], visited):
                matchR[v] = u; return True
        return False
    count = 0
    for u in left_set:
        if try_dfs(u, set()): count += 1
    return count


def probe(N, label, k):
    print(f"\n--- {label}, k={k} ---")
    res = bipartite_degrees(N, k)
    if not res:
        print(f"  empty case, skip"); return
    Xk, Xkp1, fwd_deg, back_deg = res
    fwd_vals = list(fwd_deg.values())
    back_vals = list(back_deg.values())
    d = N.n - 2*k
    print(f"  n={N.n}, rank={N.rank}, |X_k|={len(Xk)}, |X_{{k+1}}|={len(Xkp1)}, d={d}, k+1={k+1}")
    print(f"  forward-deg: min={min(fwd_vals)}, max={max(fwd_vals)}, avg={sum(fwd_vals)/len(fwd_vals):.2f}")
    print(f"  back-deg:    min={min(back_vals)}, max={max(back_vals)}, avg={sum(back_vals)/len(back_vals):.2f}")
    # Hall double-count predicted bound:
    expected_min_NS_over_S = min(fwd_vals) / max(back_vals)
    print(f"  Double-counting predicts: |N(S)|/|S| ≥ min_fwd / max_back = {min(fwd_vals)}/{max(back_vals)} = {expected_min_NS_over_S:.3f}")
    print(f"  Hall trivially follows iff predicted bound ≥ 1: {expected_min_NS_over_S >= 1}")
    # Actual matching
    adj = {}
    Xkp1_set = set(Xkp1)
    for A in Xk:
        adj[A] = []
        for i in range(N.n):
            if i in A: continue
            Ap = A | frozenset([i])
            if Ap in Xkp1_set:
                adj[A].append(Ap)
    msize = hopcroft_karp_matching(adj, Xk)
    print(f"  Actual max matching: {msize} {'(covers X_k ✓)' if msize == len(Xk) else f'(deficit {len(Xk)-msize})'}")
    is_d_le_k = d <= k
    if is_d_le_k:
        print(f"  ** d={d} <= k={k}: 'hard regime' — Hall by double-counting alone fails to apply.")


def main():
    M = M_Kn(6)
    # Failing-Lemma-5 simple matroids
    N1 = make_NC_U(M, frozenset(), frozenset(range(8)))
    probe(N1, "N1 = M(K_6)|_{0..7}", 3)
    N2 = make_NC_U(M, frozenset(), frozenset(list(range(7))+[9]))
    probe(N2, "N2 = M(K_6)|_{0..6,9}", 3)
    # Failing-Lemma-5 parallel-rich (smallest case)
    N_fail = make_NC_U(M, frozenset({0}), frozenset({0,1,2,3,4,5,6}))
    probe(N_fail, "failing parallel-rich orbit", 2)
    # Other failing orbits at M(K_6) m=3,d=2
    for U_extra in [8, 11, 13, 14]:
        N = make_NC_U(M, frozenset({0}), frozenset({0,1,2,3,5,6,U_extra}))
        probe(N, f"M(K_6) m=3 d=2 C={{0}} U={{0..3,5,6,{U_extra}}}", 2)
    # Uniforms in hard regime (d <= k)
    probe(Matroid.uniform(5, 8), "U_{5,8}", 3)  # d=2, k=3
    probe(Matroid.uniform(7, 12), "U_{7,12}", 5)  # d=2, k=5
    # AG(3,2)
    probe(AG_n_2(3), "AG(3,2)", 2)


if __name__ == "__main__":
    main()
