"""Stress-test Hall's condition on (X_k, X_{k+1}) across all distinct N(C, U)
sub-matroids harvested from M(K_n) and other test matroids.

If Hall fails on ANY case, that case would also violate Theorem 4'-II
(empirically nothing violates this, so Hall should hold universally).

This corroborates Hall as the right combinatorial reduction of Theorem 4'-II.
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from sparse_rank import M_Kn
from gpu_rank import Matroid, Vamos, AG_n_2


def Fano():
    lines = [frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
    bases = [b for b in combinations(range(7), 3) if frozenset(b) not in lines]
    return Matroid.from_bases(7, bases)


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
        comp = E - A
        if comp not in N.indep: continue
        out.append(A)
    return out


def hopcroft_karp_matching(adj, left_set):
    """Find max matching using simple DFS-augmenting paths.
    adj: dict mapping left vertex -> list of right vertices.
    Returns size of max matching from left side."""
    matchR = {}  # right -> left
    def try_dfs(u, visited):
        for v in adj.get(u, []):
            if v in visited: continue
            visited.add(v)
            if v not in matchR or try_dfs(matchR[v], visited):
                matchR[v] = u
                return True
        return False
    count = 0
    for u in left_set:
        if try_dfs(u, set()):
            count += 1
    return count


def check_hall(N, k):
    """Return (|X_k|, |X_{k+1}|, max_matching_size). If max_matching == |X_k|, Hall holds."""
    Xk = X_k_set(N, k)
    Xkp1 = set(X_k_set(N, k+1))
    if not Xk: return (0, len(Xkp1), 0)
    adj = {}
    for A in Xk:
        adj[A] = []
        for i in range(N.n):
            if i in A: continue
            Ap = A | frozenset([i])
            if Ap in Xkp1:
                adj[A].append(Ap)
    msize = hopcroft_karp_matching(adj, Xk)
    return (len(Xk), len(Xkp1), msize)


def harvest_test(M, label, max_orbits=500):
    """Harvest all N(C, U) orbits up to max, check Hall on each at appropriate (k, d)."""
    print(f"\n=== {label}: n={M.n}, rank={M.rank} ===")
    seen = set()
    orbit_results = []
    hall_failures = []
    for m_ in range(M.rank + 1):
        for d_ in range(2, M.rank - m_ + 1):
            pairs = 0
            for S in M.by_size.get(m_, []):
                for T in M.by_size.get(m_+d_, []):
                    pairs += 1
                    if pairs > max_orbits: break
                    C, U = S & T, S | T
                    key = (frozenset(C), frozenset(U))
                    if key in seen: continue
                    seen.add(key)
                    N = make_NC_U(M, C, U)
                    # k in N's frame: k = m_ - |C|.
                    k_in_N = m_ - len(C)
                    if k_in_N < 0 or k_in_N + 1 > N.rank:
                        continue
                    src, tgt, msize = check_hall(N, k_in_N)
                    if src == 0: continue
                    orbit_results.append((src, tgt, msize, k_in_N, d_, len(C)))
                    if msize < src:
                        hall_failures.append((C, U, k_in_N, d_, src, tgt, msize, N.f))
                if pairs > max_orbits: break
    return orbit_results, hall_failures


def main():
    print("=" * 70)
    print("Hall's condition stress test on X-bipartite graph")
    print("=" * 70)
    matroids = [
        ("M(K_4)", M_Kn(4)),
        ("M(K_5)", M_Kn(5)),
        ("M(K_6)", M_Kn(6)),
        ("Fano", Fano()),
        ("AG(3,2)", AG_n_2(3)),
        ("Vamos", Vamos()),
    ]
    total_orbits = 0
    total_failures = 0
    all_failures = []
    for label, M in matroids:
        results, failures = harvest_test(M, label, max_orbits=400)
        n_orbits = len(results)
        n_fails = len(failures)
        total_orbits += n_orbits
        total_failures += n_fails
        all_failures.extend([(label, *f) for f in failures])
        # Find tightest Hall margin (min over orbits of |X_{k+1}| - |X_k|).
        if results:
            tightest = min(results, key=lambda r: r[1] - r[0])
            print(f"  {n_orbits} orbits tested, {n_fails} Hall failures.  "
                  f"Tightest: |X_k|={tightest[0]} |X_{{k+1}}|={tightest[1]} matching={tightest[2]}")

    print(f"\n=== TOTAL: {total_orbits} distinct orbits, {total_failures} Hall failures ===")
    if all_failures:
        print(f"\nHall failures found:")
        for label, C, U, k, d, src, tgt, msize, fvec in all_failures[:10]:
            print(f"  {label}  C={sorted(C)} U={sorted(U)} k={k} d={d}  "
                  f"|X_k|={src} |X_{{k+1}}|={tgt} matching={msize}  fN={fvec}")
    else:
        print("\nNO Hall failures. Hall's condition holds on every tested orbit.")


if __name__ == "__main__":
    main()
