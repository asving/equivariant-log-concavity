"""Compare the 'difficulty' / information content of three proof strategies on the
same set of matroids:

  (A) Direct: compute rank of bipartite incidence matrix ∂*|_{X_k}, check = |X_k|.
  (B) Hall: find a max matching, check = |X_k|.
  (C) Aut-orbit Hall: compute Aut-orbits, verify |N(O)| ≥ |O| per orbit.

For each strategy, count "operations" / orbits / equations:
  - For A and B: roughly |X_k| × |X_{k+1}| work.
  - For C: # orbits checks, each at most |X_k| × |X_{k+1}| effort (typically much less).

The win is when # orbits << |X_k|.
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations, permutations
from sparse_rank import M_Kn, sparse_rank_modp
from gpu_rank import Matroid, Vamos


def K_mn(m, n_outer):
    """Bipartite K_{m, n_outer}."""
    edges = [(i, m+j) for i in range(m) for j in range(n_outer)]
    n_verts = m + n_outer
    def is_tree(B):
        if len(B) != n_verts - 1: return False
        p = list(range(n_verts))
        def f(x):
            while p[x] != x: p[x] = p[p[x]]; x = p[x]
            return x
        for ei in B:
            u, v = edges[ei]
            ru, rv = f(u), f(v)
            if ru == rv: return False
            p[ru] = rv
        return True
    nE = len(edges)
    bases = [b for b in combinations(range(nE), n_verts-1) if is_tree(b)]
    return Matroid.from_bases(nE, bases)


def X_k_set(N, k):
    E = frozenset(range(N.n))
    out = []
    for A in combinations(range(N.n), k):
        A = frozenset(A)
        if A not in N.indep: continue
        if (E - A) not in N.indep: continue
        out.append(A)
    return out


def compute_aut(N):
    if N.n > 8: return None  # too slow brute force
    aut = []
    for sigma in permutations(range(N.n)):
        ok = all(frozenset(sigma[i] for i in S) in N.indep for S in N.indep)
        if ok: aut.append(sigma)
    return aut


def get_orbits(items, action_group, item_set):
    if action_group is None: return None
    seen = set(); orbits = []
    for x in items:
        if x in seen: continue
        orbit = {x}; frontier = [x]
        while frontier:
            c = frontier.pop()
            for sigma in action_group:
                y = frozenset(sigma[i] for i in c)
                if y in item_set and y not in orbit:
                    orbit.add(y); frontier.append(y)
        orbits.append(orbit); seen.update(orbit)
    return orbits


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


def bipartite_rank(N, Xk, Xkp1, P=10007):
    Xkp1_idx = {A: i for i, A in enumerate(Xkp1)}
    rows, cols, vals = [], [], []
    for j, A in enumerate(Xk):
        for i in range(N.n):
            if i in A: continue
            Ap = A | frozenset([i])
            if Ap in Xkp1_idx:
                rows.append(Xkp1_idx[Ap]); cols.append(j); vals.append(1)
    if not rows: return 0
    return sparse_rank_modp(rows, cols, vals, len(Xkp1), len(Xk), P, verbose=False)


def hopcroft_karp(adj, left):
    matchR = {}
    def try_dfs(u, visited):
        for v in adj.get(u, []):
            if v in visited: continue
            visited.add(v)
            if v not in matchR or try_dfs(matchR[v], visited):
                matchR[v] = u; return True
        return False
    count = 0
    for u in left:
        if try_dfs(u, set()): count += 1
    return count


def analyze_matroid(N, label, k):
    print(f"\n{'='*60}")
    print(f"{label} (n={N.n}, rank={N.rank})")
    print(f"{'='*60}")
    Xk = X_k_set(N, k); Xkp1 = X_k_set(N, k+1)
    if not Xk:
        print(f"  X_k empty; skip"); return
    Xkp1_set = set(Xkp1)
    print(f"  |X_k| = {len(Xk)}, |X_{{k+1}}| = {len(Xkp1)}")

    # (A) Rank
    rk = bipartite_rank(N, Xk, Xkp1)
    print(f"  (A) Direct rank check: rank = {rk}/{len(Xk)}  {'✓' if rk == len(Xk) else '✗'}")

    # (B) Matching
    adj = bipartite_adj(N, Xk, Xkp1_set)
    msize = hopcroft_karp(adj, Xk)
    print(f"  (B) Matching check: matching = {msize}/{len(Xk)}  {'✓' if msize == len(Xk) else '✗'}")

    # (C) Aut-orbit
    aut = compute_aut(N)
    if aut is None:
        print(f"  (C) Aut-orbit: matroid too large for brute-force Aut, skip"); return
    orbits = get_orbits(Xk, aut, set(Xk))
    print(f"  (C) Aut-orbit: |Aut| = {len(aut)}, # orbits = {len(orbits)}")
    print(f"      Orbit sizes: {sorted([len(o) for o in orbits], reverse=True)}")
    all_ok = True
    for i, orbit in enumerate(orbits):
        nbhd = set()
        for A in orbit: nbhd.update(adj[A])
        ok = len(nbhd) >= len(orbit)
        all_ok &= ok
        print(f"      Orbit {i}: |O| = {len(orbit):3d}, |N(O)| = {len(nbhd):3d}, {'✓' if ok else '✗'}")
    print(f"  Aut-orbit Hall result: {'all orbits OK ✓' if all_ok else 'FAILS'}")

    # Compute "proof effort":
    print(f"\n  Comparison of proof effort:")
    print(f"    (A) Direct rank: O({len(Xkp1)} × {len(Xk)}) = {len(Xkp1) * len(Xk)} matrix entries to process.")
    print(f"    (B) Matching: O({len(Xk)}^2 × max-deg) augmentations.")
    print(f"    (C) Aut-orbit: {len(orbits)} per-orbit checks, each O(|O|).")


if __name__ == "__main__":
    # The standard "tractable for Aut-orbit" cases
    analyze_matroid(K_mn(2, 3), "M(K_{2,3})", 2)
    analyze_matroid(K_mn(2, 4), "M(K_{2,4})", 3)
    analyze_matroid(K_mn(3, 3), "M(K_{3,3})", 4)
    analyze_matroid(Vamos(), "Vamos V_8", 3)
    analyze_matroid(M_Kn(6), "M(K_6) [as a whole]", 3)
