"""Explicit matching attempts on G_X = (X_k, X_{k+1}).

Try different deterministic strategies and see which give full matchings on
the tight cases (where Hall holds with small margin).

Strategy 1: Lex-greedy — process X_k in lex order, extend each by min element.
Strategy 2: "Min-degree first" — process A with smallest degree first.
Strategy 3: Augmenting path from arbitrary start.

The goal is to find a "matroid-natural" matching, which would give a proof template.
"""
import sys
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


def get_neighbors(N, A, Xkp1_set):
    out = []
    for i in range(N.n):
        if i in A: continue
        Ap = A | frozenset([i])
        if Ap in Xkp1_set: out.append((i, Ap))
    return out


def strategy_lex(N, Xk, Xkp1_set):
    """Process X_k in lex order; for each, pick the lex-smallest extension not yet used."""
    used = set()
    matching = {}
    Xk_sorted = sorted(Xk, key=lambda s: sorted(s))
    failures = []
    for A in Xk_sorted:
        neighs = get_neighbors(N, A, Xkp1_set)
        # pick lex-smallest extension i with Ap not yet used
        neighs.sort(key=lambda t: (t[0], sorted(t[1])))
        chosen = None
        for i, Ap in neighs:
            if Ap not in used:
                chosen = (i, Ap)
                break
        if chosen is None:
            failures.append((A, [i for i, _ in neighs]))
        else:
            used.add(chosen[1])
            matching[A] = chosen
    return matching, failures


def strategy_low_degree_first(N, Xk, Xkp1_set):
    """Process X_k starting with low-degree vertices."""
    used = set()
    matching = {}
    failures = []
    degrees = {A: len(get_neighbors(N, A, Xkp1_set)) for A in Xk}
    Xk_sorted = sorted(Xk, key=lambda A: (degrees[A], sorted(A)))
    for A in Xk_sorted:
        neighs = get_neighbors(N, A, Xkp1_set)
        chosen = None
        for i, Ap in sorted(neighs, key=lambda t: t[0]):
            if Ap not in used:
                chosen = (i, Ap); break
        if chosen is None:
            failures.append((A, neighs))
        else:
            used.add(chosen[1])
            matching[A] = chosen
    return matching, failures


def strategy_augment(N, Xk, Xkp1_set):
    """Full DFS-based bipartite matching (Hungarian-style)."""
    matchR = {}
    def try_dfs(u, visited, adj):
        for v in adj[u]:
            if v in visited: continue
            visited.add(v)
            if v not in matchR or try_dfs(matchR[v], visited, adj):
                matchR[v] = u
                return True
        return False
    adj = {A: [Ap for _, Ap in get_neighbors(N, A, Xkp1_set)] for A in Xk}
    matched = 0
    for A in Xk:
        if try_dfs(A, set(), adj):
            matched += 1
    return matched


def report(N, label, k):
    print(f"\n--- {label}: n={N.n}, rank={N.rank}, k={k} ---")
    Xk = X_k_set(N, k)
    Xkp1 = X_k_set(N, k+1)
    Xkp1_set = set(Xkp1)
    if not Xk:
        print(f"  X_k empty, skip")
        return
    print(f"  |X_k|={len(Xk)}, |X_{{k+1}}|={len(Xkp1)}")
    # Lex
    m, fails = strategy_lex(N, Xk, Xkp1_set)
    print(f"  Lex-greedy: matched {len(m)}/{len(Xk)}  {'✓' if len(fails)==0 else f'✗ failures: {len(fails)}'}")
    # Low-deg
    m2, fails2 = strategy_low_degree_first(N, Xk, Xkp1_set)
    print(f"  Low-deg-first: matched {len(m2)}/{len(Xk)}  {'✓' if len(fails2)==0 else f'✗ failures: {len(fails2)}'}")
    # Augment
    msize = strategy_augment(N, Xk, Xkp1_set)
    print(f"  Hungarian / augment: matched {msize}/{len(Xk)}  {'✓' if msize == len(Xk) else '✗'}")


if __name__ == "__main__":
    M = M_Kn(6)
    N1 = make_NC_U(M, frozenset(), frozenset(range(8)))
    report(N1, "N1 = M(K_6)|_{0..7}", 3)

    N2 = make_NC_U(M, frozenset(), frozenset(list(range(7)) + [9]))
    report(N2, "N2 = M(K_6)|_{0..6,9}", 3)

    # The failing M(K_6) orbit (parallel-rich N)
    failing_C = frozenset({0})
    failing_U = frozenset({0, 1, 2, 3, 4, 5, 6})
    N_fail = make_NC_U(M, failing_C, failing_U)
    report(N_fail, "failing orbit N", 2)

    # Uniform
    report(Matroid.uniform(5, 8), "U_{5,8}", 3)
    report(Matroid.uniform(4, 6), "U_{4,6}", 2)
