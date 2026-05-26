"""Test d=2 boundary on GENUINELY CONNECTED non-uniform matroids.

Previous test had errors — "rank-r on 2r-2 with triangle" gives rank > r
when the matroid axioms don't force rank reduction.

Genuinely connected non-uniform matroid at d=2 boundary (n=2r-2 with rank=r):
   M(5-cycle + chord): n=6, rank=4. Has triangle + 4-cycle + 5-cycle circuits.

   M(theta graph): two vertices joined by 3 internally-disjoint paths.

For each: verify ∂* injective at d=2 boundary AND look at structural
properties (eigenvalues, kernel structure) for proof hints.
"""
from __future__ import annotations
import sys
from itertools import combinations
import numpy as np
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid
from test_hard_lefschetz_x import x_sets, bipartite_matrix, rank_modp


def build_graphic_matroid(edges, n_verts):
    """Build M(G) for a graph G with given edges (list of (u, v) tuples)."""
    n = len(edges)
    def is_forest(idxs):
        parent = list(range(n_verts))
        def find(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v
        for i in idxs:
            u, v = edges[i]
            ru, rv = find(u), find(v)
            if ru == rv:
                return False
            parent[ru] = rv
        return True
    indep = []
    for k in range(n + 1):
        for S in combinations(range(n), k):
            if is_forest(S):
                indep.append(frozenset(S))
    return Matroid(n, indep)


def matroid_is_connected(M):
    """Check matroid connectivity: no proper S with rank(S) + rank(E\\S) = rank(M)."""
    n = M.n
    r = M.rank
    def rk(A):
        return max((len(B) for B in M.indep if B.issubset(A)), default=0)
    for k in range(1, n):
        for S in combinations(range(n), k):
            S = frozenset(S)
            comp = frozenset(range(n)) - S
            if rk(S) + rk(comp) == r:
                return False, S
    return True, None


def analyze_d2(M, label):
    """Analyze d=2 boundary case in detail."""
    print(f"\n{'='*70}")
    print(f"  {label}: n={M.n}, rank={M.rank}")
    print(f"{'='*70}")
    print(f"  f-vector: {M.f}")
    n, r = M.n, M.rank
    xv = [len(x_sets(M, k)) for k in range(n + 1)]
    while xv and xv[-1] == 0: xv.pop()
    print(f"  X-vector: {xv}")

    is_conn, sep = matroid_is_connected(M)
    print(f"  Connected as matroid: {is_conn}" + (f" (separator: {sorted(sep)})" if not is_conn else ""))

    # Check d=2 boundary
    d = 2
    m = (n - d) // 2
    if 2*m + d == n and m + d == r:
        print(f"  d=2 boundary bigrade: m={m}, d={d}")
        if m < len(xv) and m+1 < len(xv):
            mat = bipartite_matrix(M, m)
            rk = rank_modp(mat)
            inj = (rk == xv[m])
            print(f"  ∂*: X_{m}({xv[m]}) → X_{m+1}({xv[m+1]}): rank={rk}  [{'INJ ✓' if inj else 'NOT INJ ✗'}]")

            # Eigenvalues of L^{n-2m}: X_m → X_{n-m} (HL)
            if xv[m] == xv[n-m] if n-m < len(xv) else False:
                from test_hard_lefschetz_x import L_power
                power = n - 2*m
                if power > 0 and n - m < len(xv):
                    L_mat = L_power(M, m, power)
                    eigs = sorted(np.linalg.eigvals(L_mat.astype(float)).real.round(4).tolist())
                    print(f"  Eigenvalues of L^{power}: X_{m} → X_{n-m}:")
                    if len(eigs) <= 12:
                        print(f"    {eigs}")
                    else:
                        print(f"    span [{min(eigs):.2f}, {max(eigs):.2f}], {len(set(eigs))} distinct")
            return inj
    else:
        print(f"  NOT at d=2 boundary (m+d={m+d}, rank={r})")
    return None


def main():
    # M(5-cycle + chord): genuinely connected non-uniform at d=2 boundary
    edges_5c_chord = [(0,1), (1,2), (2,3), (3,4), (4,0), (0,2)]
    M1 = build_graphic_matroid(edges_5c_chord, 5)
    analyze_d2(M1, "M(5-cycle + chord {0,2})")

    # M(theta graph): 2 vertices with 3 paths of lengths 2, 2, 2
    # Vertices: 0, 1, 2, 3, 4. Paths: 0-2-1, 0-3-1, 0-4-1.
    edges_theta = [(0,2), (2,1), (0,3), (3,1), (0,4), (4,1)]
    M2 = build_graphic_matroid(edges_theta, 5)
    analyze_d2(M2, "M(theta graph)")

    # M(K_4) minus 0 edges = K_4 itself: rank 3, n=6, d=2 boundary?
    # n=6, rank=3, m+d ≤ 3 so m=1 d=2 (not boundary since rank=3 ≠ m+2=3, actually IS boundary)
    edges_k4 = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
    M3 = build_graphic_matroid(edges_k4, 4)
    print(f"\n  Note: M(K_4) has n=6, rank=3. d=2 boundary requires rank=(n+2)/2=4. So NOT at d=2 boundary.")
    print(f"  f-vector: {M3.f}, X-vector: {[len(x_sets(M3, k)) for k in range(M3.n+1)]}")

    # M(prism graph): K_3,3 minus matching? Or other connected non-uniform
    # K_4 + 1 edge attached: 5 vertices, 7 edges. Too many.

    # M(K_{2,3}): bipartite 5 vertices, 6 edges, rank 4
    edges_K23 = [(0,2), (0,3), (0,4), (1,2), (1,3), (1,4)]
    M4 = build_graphic_matroid(edges_K23, 5)
    analyze_d2(M4, "M(K_{2,3})")


if __name__ == "__main__":
    main()
