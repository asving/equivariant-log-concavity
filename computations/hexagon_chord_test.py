"""Test HL on R(M)|_X for M = M(hexagon + chord).

G = hexagon 0-1-2-3-4-5-0 with chord (0,3).
Edges: e_0=(0,1), e_1=(1,2), e_2=(2,3), e_3=(3,4), e_4=(4,5), e_5=(5,0), e_6=(0,3).

M(G): rank 5 (= 6 vertices - 1), n = 7 edges.
Circuits: 2 four-cycles + 1 hexagon (3 circuits total).

Matroid M is:
  - CONNECTED (G is 2-edge-connected).
  - NON-UNIFORM (has circuits of size 4 < 5 = rank).
  - IN BIGRADE HYPOTHESIS: rank 5 > (n+2)/2 = 4.5. The bigrade (m=2, d=3) is valid.

This is the simplest matroid satisfying all three properties.

Goal: verify ∂*: X_2 → X_3 is INJECTIVE (= project's conjecture for this matroid).
      And verify HL on R(M)|_X via ∂*^3: X_2 → X_5 iso.
"""

from __future__ import annotations
import sys
from itertools import combinations
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid
from test_hard_lefschetz_x import x_sets, bipartite_matrix, rank_modp, L_power


def build_hexagon_chord():
    """Build M(hexagon + chord {0,3}).
    Edges: 0=(0,1), 1=(1,2), 2=(2,3), 3=(3,4), 4=(4,5), 5=(5,0), 6=(0,3).
    """
    edges = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (0,3)]
    n_edges = 7
    n_verts = 6

    def is_forest(edge_indices):
        parent = list(range(n_verts))
        def find(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v
        for i in edge_indices:
            u, v = edges[i]
            ru, rv = find(u), find(v)
            if ru == rv:
                return False
            parent[ru] = rv
        return True

    indep = []
    for k in range(n_edges + 1):
        for S in combinations(range(n_edges), k):
            if is_forest(S):
                indep.append(frozenset(S))
    return Matroid(n_edges, indep)


def main():
    M = build_hexagon_chord()
    print(f"M(hexagon + chord): n={M.n}, rank={M.rank}")
    print(f"  f-vector: {M.f}")
    xv = [len(x_sets(M, k)) for k in range(M.n + 1)]
    print(f"  X-vector: {xv}")

    # Bigrade hypothesis: 2m+d ≤ n, m+d ≤ rank, d ≥ 2.
    print(f"\n  Bigrade hypothesis checks (2m+d ≤ n={M.n}, m+d ≤ {M.rank}, d ≥ 2):")
    for m in range(M.n + 1):
        for d in range(2, M.n + 1):
            if 2*m + d <= M.n and m + d <= M.rank:
                print(f"    (m={m}, d={d}) valid;  X_m = {xv[m] if m < len(xv) else 0}, X_{{m+1}} = {xv[m+1] if m+1 < len(xv) else 0}")

    # Test ∂*: X_k → X_{k+1} for each k in X-support
    print(f"\n  Single-step injectivity tests:")
    for k in range(M.n + 1):
        Xk = x_sets(M, k)
        if not Xk:
            continue
        Xk1 = x_sets(M, k + 1)
        if not Xk1:
            continue
        mat = bipartite_matrix(M, k)
        rk = rank_modp(mat)
        flag = "INJ" if rk == len(Xk) else f"ker={len(Xk)-rk}"
        print(f"    ∂*: X_{k}({len(Xk)}) → X_{k+1}({len(Xk1)}): rank={rk}  [{flag}]")

    # HL test: ∂*^{n-2k}: X_k → X_{n-k} iso
    print(f"\n  HL tests (∂*^{{n-2k}}: X_k → X_{{n-k}}):")
    n = M.n
    for k in range(n + 1):
        target = n - k
        if target <= k:
            continue
        Xk_size = xv[k] if k < len(xv) else 0
        Xtgt_size = xv[target] if target < len(xv) else 0
        if Xk_size == 0:
            continue
        if Xk_size != Xtgt_size:
            print(f"    k={k}→{target}: |X_k|={Xk_size} ≠ |X_{{n-k}}|={Xtgt_size}")
            continue
        power = target - k
        mat = L_power(M, k, power)
        rk = rank_modp(mat)
        flag = "ISO ✓" if rk == Xk_size else f"NOT ISO (rank {rk}/{Xk_size})"
        print(f"    ∂*^{power}: X_{k}({Xk_size}) → X_{target}({Xtgt_size}): rank={rk}  [{flag}]")


if __name__ == "__main__":
    main()
