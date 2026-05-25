"""Test Hall's condition on the bipartite graph (X_k, X_{k+1}) for various matroids.

Hall's condition: for every S ⊆ X_k, |N(S)| ≥ |S|, where N(S) ⊆ X_{k+1} is the
set of all valid extensions A ∪ {i} for A ∈ S.

If Hall holds, there is a matching covering X_k. A matching implies that the
bipartite incidence ∂*|_{X_k} has full column rank (= injective).

We test Hall directly only for small examples; for larger ones we check the
necessary condition deg(A) ≥ 1 (trivially satisfied) plus look at "deficiency"
across all subsets via the bipartite-matching algorithm.
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from sparse_rank import M_Kn
from gpu_rank import Matroid, Vamos


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


def bipartite_edges(N, Xk, Xkp1):
    """Edges (A, A') with A ∈ X_k, A' ∈ X_{k+1}, A ⊂ A'."""
    Xkp1_set = set(Xkp1)
    edges_per_A = {}  # A -> list of A'
    edges_per_Ap = {}  # A' -> list of A
    for A in Xk:
        edges_per_A[A] = []
        for i in range(N.n):
            if i in A: continue
            Ap = A | frozenset([i])
            if Ap in Xkp1_set:
                if (Ap not in N.indep): continue  # extra safety
                edges_per_A[A].append(Ap)
                edges_per_Ap.setdefault(Ap, []).append(A)
    return edges_per_A, edges_per_Ap


def matching_size(edges_per_A):
    """Find max matching from X_k side using Hopcroft–Karp / Hungarian.
    Implements a simple DFS-based bipartite matching."""
    # Convert: A is "left", A' is "right". Match left → right.
    matchR = {}  # A' -> A
    def try_dfs(A, visited):
        for Ap in edges_per_A[A]:
            if Ap in visited: continue
            visited.add(Ap)
            if Ap not in matchR or try_dfs(matchR[Ap], visited):
                matchR[Ap] = A
                return True
        return False
    matched = 0
    for A in edges_per_A:
        visited = set()
        if try_dfs(A, visited):
            matched += 1
    return matched, matchR


def check_hall_directly(edges_per_A, Xk):
    """For small |X_k|, check Hall's condition by brute force over subsets."""
    if len(Xk) > 20:
        return None, "too large for brute force"
    failures = []
    for r in range(1, len(Xk)+1):
        for S_tup in combinations(Xk, r):
            S = list(S_tup)
            N_S = set()
            for A in S:
                N_S.update(edges_per_A.get(A, []))
            if len(N_S) < len(S):
                failures.append((tuple(sorted(map(sorted, S))), sorted(map(sorted, N_S)), len(S), len(N_S)))
                if len(failures) >= 5:
                    return failures, f"{len(failures)} Hall failures (truncated)"
    return failures, f"no Hall failures over {2**len(Xk)} subsets" if not failures else f"{len(failures)} Hall failures"


def check_one(N, label, k):
    print(f"\n--- {label}: n={N.n}, rank={N.rank}, k={k} ---")
    Xk = X_k_set(N, k)
    Xkp1 = X_k_set(N, k+1)
    print(f"  |X_k| = {len(Xk)}, |X_{{k+1}}| = {len(Xkp1)}")
    if not Xk:
        print(f"  X_k is empty — vacuous")
        return
    edges_per_A, edges_per_Ap = bipartite_edges(N, Xk, Xkp1)
    degrees = [len(edges_per_A[A]) for A in Xk]
    print(f"  Degrees: min={min(degrees)}, max={max(degrees)}, avg={sum(degrees)/len(degrees):.2f}")
    if min(degrees) == 0:
        zeros = [A for A in Xk if not edges_per_A[A]]
        print(f"    *** {len(zeros)} elements have degree 0 — Hall FAILS ***")
        return
    msize, _ = matching_size(edges_per_A)
    print(f"  Max matching size: {msize}  (|X_k|={len(Xk)})  {'covers X_k ✓' if msize == len(Xk) else 'PARTIAL'}")
    if msize == len(Xk):
        print(f"  ⇒ Hall's condition holds (perfect matching from X_k exists)")
    if len(Xk) <= 16:
        failures, msg = check_hall_directly(edges_per_A, Xk)
        print(f"  Hall (brute force): {msg}")


if __name__ == "__main__":
    # The failing simple matroids
    M = M_Kn(6)
    N1 = make_NC_U(M, frozenset(), frozenset(range(8)))
    check_one(N1, "N1 = M(K_6)|_{0..7}", 3)

    N2 = make_NC_U(M, frozenset(), frozenset(list(range(7)) + [9]))
    check_one(N2, "N2 = M(K_6)|_{0..6,9}", 3)

    # Some smaller / clearer cases
    check_one(M_Kn(5), "M(K_5)", 2)
    check_one(M_Kn(4), "M(K_4)", 1)

    # Uniforms
    check_one(Matroid.uniform(4, 6), "U_{4,6}", 2)
    check_one(Matroid.uniform(5, 8), "U_{5,8}", 3)
    check_one(Matroid.uniform(5, 8), "U_{5,8}", 4)

    # Failing M(K_6) orbit (rank-deficient case)
    failing_C = frozenset({0})
    failing_U = frozenset({0, 1, 2, 3, 4, 5, 6})
    N_fail = make_NC_U(M, failing_C, failing_U)
    print(f"\n*** Failing orbit M(K_6) m=3 d=2 C={{0}} U={{0,...,6}} ***")
    print(f"   N: n={N_fail.n}, rank={N_fail.rank}, f={N_fail.f}")
    check_one(N_fail, "N(failing orbit)", 2)

    # Vamos
    check_one(Vamos(), "Vamos V_8", 2)
    check_one(Vamos(), "Vamos V_8", 3)
