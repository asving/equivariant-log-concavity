"""Test the conjecture: the tightest Hall subsets in G_X(M) are exactly the
Aut(M)-orbits in X_k.

If true: then Hall reduces to proving the conjecture per-Aut(M)-orbit, which
is a cleaner combinatorial / representation-theoretic statement.

For each test matroid, compute Aut(M), find orbits in X_k, check Hall's
inequality |N(orbit)| ≥ |orbit|.
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations, permutations
from collections import defaultdict
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


def compute_aut_group(N, sample_limit=None):
    """Brute force: permutations of [n] that preserve the indep set family.
    Returns list of permutations as tuples.

    For small N (n ≤ 8), this is feasible. For larger, sample or skip."""
    n = N.n
    if n > 8:
        return None
    aut = []
    for sigma in permutations(range(n)):
        # Check sigma preserves Indep
        ok = True
        for S in N.indep:
            T = frozenset(sigma[i] for i in S)
            if T not in N.indep:
                ok = False; break
        if ok: aut.append(sigma)
        if sample_limit and len(aut) >= sample_limit: break
    return aut


def aut_orbits(N, X_k, aut_group):
    """Partition X_k into Aut(N)-orbits."""
    if aut_group is None: return None
    orbit_id = {}
    next_id = 0
    seen = set()
    orbits = []
    for A in X_k:
        if A in seen: continue
        # Compute orbit of A
        orbit = set()
        orbit.add(A)
        frontier = [A]
        while frontier:
            curr = frontier.pop()
            for sigma in aut_group:
                B = frozenset(sigma[i] for i in curr)
                if B not in orbit and B in set(X_k):
                    orbit.add(B); frontier.append(B)
        orbits.append(orbit)
        seen.update(orbit)
    return orbits


def X_k_set(N, k):
    E = frozenset(range(N.n))
    out = []
    for A in combinations(range(N.n), k):
        A = frozenset(A)
        if A not in N.indep: continue
        if (E - A) not in N.indep: continue
        out.append(A)
    return out


def bipartite_adj(N, Xk, Xkp1_set):
    adj = {}
    for A in Xk:
        adj[A] = []
        for i in range(N.n):
            if i in A: continue
            Ap = A | frozenset([i])
            if Ap in Xkp1_set:
                adj[A].append(Ap)
    return adj


def analyze(N, label, k):
    print(f"\n=== {label}: n={N.n}, rank={N.rank}, k={k} ===")
    Xk = X_k_set(N, k)
    Xkp1 = X_k_set(N, k+1)
    if not Xk:
        print(f"  X_k empty, skip"); return
    Xkp1_set = set(Xkp1)
    adj = bipartite_adj(N, Xk, Xkp1_set)
    print(f"  |X_k|={len(Xk)}, |X_{{k+1}}|={len(Xkp1)}")

    aut = compute_aut_group(N)
    if aut is None:
        print(f"  matroid too large for Aut computation, skip"); return
    print(f"  |Aut(N)| = {len(aut)}")
    orbits = aut_orbits(N, Xk, aut)
    print(f"  # orbits of Aut(N) in X_k: {len(orbits)}")
    print(f"  Orbit sizes: {sorted([len(o) for o in orbits], reverse=True)}")

    # For each orbit, compute |N(orbit)| (= union of extensions).
    print(f"  Hall check per Aut-orbit:")
    for orbit in orbits:
        S = orbit
        nbhd = set()
        for A in S:
            nbhd.update(adj[A])
        ok = "✓" if len(nbhd) >= len(S) else "✗"
        print(f"    |orbit|={len(S):3d}  |N(orbit)|={len(nbhd):3d}  ratio={len(nbhd)/len(S):.3f}  {ok}")

    # Find tightest UNION of orbits.
    print(f"  Best candidate 'tight' subset (union of orbits):")
    best_ratio = float('inf')
    best_subset_desc = None
    from itertools import chain, combinations as C
    if len(orbits) <= 8:
        for r_ in range(1, len(orbits)+1):
            for sel_idxs in C(range(len(orbits)), r_):
                S = set()
                for i in sel_idxs: S.update(orbits[i])
                nbhd = set()
                for A in S: nbhd.update(adj[A])
                ratio = len(nbhd)/len(S)
                if ratio < best_ratio:
                    best_ratio = ratio
                    best_subset_desc = (sel_idxs, len(S), len(nbhd))
        idxs, sz, nbh = best_subset_desc
        print(f"    Tightest: union of orbits {idxs}: |S|={sz}, |N|={nbh}, ratio={best_ratio:.3f}")


if __name__ == "__main__":
    M = M_Kn(6)
    N1 = make_NC_U(M, frozenset(), frozenset(range(8)))
    analyze(N1, "N1 = M(K_6)|_{0..7}", 3)
    N2 = make_NC_U(M, frozenset(), frozenset(list(range(7))+[9]))
    analyze(N2, "N2 = M(K_6)|_{0..6,9}", 3)
    # Failing parallel-rich
    N_fail = make_NC_U(M, frozenset({0}), frozenset({0,1,2,3,4,5,6}))
    analyze(N_fail, "failing parallel-rich orbit", 2)
    # M(K_4)
    analyze(M_Kn(4), "M(K_4)", 1)
    # Uniform U_{4,6}
    analyze(Matroid.uniform(4, 6), "U_{4,6}", 2)
    # Uniform U_{5,8}
    analyze(Matroid.uniform(5, 8), "U_{5,8}", 3)
