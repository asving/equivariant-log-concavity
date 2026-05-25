"""Deep-dive on N1 = M(K_6)|_{0..7} to understand what makes Hall hold even
when double-counting fails.

Specifically, examine which A in X_3(N1) has low degree (3) vs high degree (5),
and which A' in X_4(N1) has high back-degree (4) — and check if there's a
"tight Hall subset" that's structurally constrained.
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from collections import defaultdict, Counter
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


def analyze(N, k):
    Xk = X_k_set(N, k)
    Xkp1 = X_k_set(N, k+1)
    Xkp1_set = set(Xkp1)

    # Forward degrees
    adj = {}
    for A in Xk:
        adj[A] = []
        for i in range(N.n):
            if i in A: continue
            Ap = A | frozenset([i])
            if Ap in Xkp1_set:
                adj[A].append(Ap)
    fwd_deg = {A: len(adj[A]) for A in Xk}

    # Back degrees
    back_deg = defaultdict(int)
    for A, neighbors in adj.items():
        for Ap in neighbors:
            back_deg[Ap] += 1

    print(f"\nForward degree distribution: {dict(Counter(fwd_deg.values()))}")
    print(f"Back degree distribution:    {dict(Counter(back_deg.values()))}")

    # Sort A's by forward degree
    Xk_by_deg = sorted(Xk, key=lambda A: fwd_deg[A])
    print(f"\nA ∈ X_k with smallest forward-degree:")
    for A in Xk_by_deg[:6]:
        print(f"  A = {sorted(A)}, deg = {fwd_deg[A]}, extensions = {sorted([sorted(Ap) for Ap in adj[A]])}")

    # Find A' with high back-degree
    Xkp1_by_bdeg = sorted(Xkp1, key=lambda Ap: -back_deg.get(Ap, 0))
    print(f"\nA' ∈ X_{{k+1}} with HIGHEST back-degree (≥3):")
    for Ap in Xkp1_by_bdeg[:8]:
        if back_deg.get(Ap, 0) < 3: break
        # Find predecessors of Ap in X_k
        preds = [A for A in Xk if Ap in adj[A]]
        print(f"  A' = {sorted(Ap)}, back-deg = {back_deg[Ap]}, preds = {sorted([sorted(A) for A in preds])}")

    # CRUCIAL: examine if there's a "tight" subset
    # Specifically: take all A's with min forward-degree, check their joint neighborhood
    min_deg = min(fwd_deg.values())
    low_deg_A = [A for A in Xk if fwd_deg[A] == min_deg]
    if low_deg_A:
        nbhd = set()
        for A in low_deg_A:
            nbhd.update(adj[A])
        print(f"\nA's with min forward-degree ({min_deg}): count = {len(low_deg_A)}")
        print(f"  Their joint neighborhood: {len(nbhd)}  {'(Hall would fail if < |low_deg_A|)' if len(nbhd) < len(low_deg_A) else ''}")
        if len(nbhd) >= len(low_deg_A):
            print(f"  ✓ Hall holds at this 'tight-looking' subset (|N|={len(nbhd)} ≥ |S|={len(low_deg_A)})")

    # Check: does any 'isotypic-like' subset violate Hall?
    # Try all S of size up to ~6, brute force on Xk.
    if len(Xk) <= 25:
        print(f"\nBrute-force Hall check on subsets of size up to 6:")
        worst_ratio = float('inf')
        worst_subset = None
        for r in range(1, min(7, len(Xk)+1)):
            for S_tup in combinations(Xk, r):
                S = set(S_tup)
                nbhd = set()
                for A in S:
                    nbhd.update(adj[A])
                ratio = len(nbhd) / len(S) if S else 0
                if ratio < worst_ratio:
                    worst_ratio = ratio
                    worst_subset = (S, nbhd)
        S, nbhd = worst_subset
        print(f"  Tightest subset: |S|={len(S)}, |N(S)|={len(nbhd)}, ratio={len(nbhd)/len(S):.3f}")
        if len(nbhd) >= len(S):
            print(f"  ✓ Hall holds with margin {len(nbhd) - len(S)}")


if __name__ == "__main__":
    M = M_Kn(6)
    N1 = make_NC_U(M, frozenset(), frozenset(range(8)))
    print(f"=== N1 = M(K_6)|_{{0..7}}: n=8, rank=5, f={N1.f} ===")
    print(f"Underlying graph edges: edges 0-7 of K_6 in lex order")
    edges = list(combinations(range(6), 2))
    for i in range(8):
        print(f"  edge {i} = {edges[i]}")
    analyze(N1, 3)
