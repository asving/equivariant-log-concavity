"""Set up the geometric proof template for M = M(K_4 - e), the cycle matroid of K_4
with one edge removed.

This is the simplest connected non-uniform matroid with multi-grade X-support
(no direct-sum factorization to fall back on).

M(K_4 - e) data:
  n = 5 edges. Label them 0,1,2,3,4 representing edges 02, 03, 12, 13, 23 of K_4-{0,1}.
  rank r = 3.
  Circuits (3 of them):
    C_1 = {0, 1, 4} = edges {02, 03, 23} = triangle on vertices {0,2,3}.
    C_2 = {2, 3, 4} = edges {12, 13, 23} = triangle on vertices {1,2,3}.
    C_3 = {0, 1, 2, 3} = edges {02, 03, 12, 13} = the 4-cycle.
  f-vector: (1, 5, 10, 8, 0).
  X-vector at grades 0..5: (0, 0, 8, 8, 0, 0). Support [2, 3].

The X-restriction R(M)|_X has dims (8, 8). The Lefschetz ∂*: X_2 → X_3 is an 8x8 matrix.

GEOMETRIC SETUP:
  In (P^1)^5, coordinate subspaces are:
    Z_1 = {z_0 = z_1 = z_4 = 0}    codim 3
    Z_2 = {z_2 = z_3 = z_4 = 0}    codim 3
    Z_3 = {z_0 = z_1 = z_2 = z_3 = 0}    codim 4
  All three subspaces contain the origin {z_0=...=z_4=0}.

  Intersection lattice:
    Pairwise intersections all = origin (codim 5).
    Triple intersection = origin.

  Wonderful compactification Y:
    Step 1: Blow up origin (codim 5) → Y_0. Adds exceptional E_0 ≅ P^4, contributing
            4 new classes at degrees 2, 4, 6, 8.
    Step 2: Strict transforms of Z_1, Z_2, Z_3 in Y_0 are disjoint codim-3, codim-3, codim-4
            subvarieties. Blow up each. Adds exceptional E_1, E_2 (each P^2-bundle, contributing
            2 new classes per fiber) and E_3 (P^3-bundle, 3 new classes).

  Resulting Y is smooth projective 5-fold. By general theory of wonderful compactifications,
  Y has a natural Kähler class.

CLAIM (X-Identification for M(K_4-e)):
  The bipartite operator ∂*: X_2 → X_3 on R(M)|_X equals the matrix of mult ω̃ restricted
  to the pullback-of-R(M)|_X block at H^4(Y) → H^6(Y).

  By the block-triangular structure of mult ω̃ on H*(Y) wrt the (pullback / exceptional)
  decomposition, and HL on Y (= compact projective Kähler ⟹ HL classical),
  the diagonal pullback block is invertible. Hence ∂* is invertible.

VERIFICATION:
  Step 1: Verify ∂* is empirically invertible on M(K_4-e).
  Step 2: Sketch the block-triangular argument.
"""

from __future__ import annotations
import sys
from itertools import combinations
import numpy as np
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid
from test_hard_lefschetz_x import x_sets, bipartite_matrix, rank_modp


def build_K4_minus_e():
    """Build M = M(K_4 - {0,1}) explicitly.
    Edges labeled 0..4 = {02, 03, 12, 13, 23}.
    Edge i connects vertices: edges[i] below.
    """
    edges = [(0,2), (0,3), (1,2), (1,3), (2,3)]  # 5 edges of K_4 - {0,1}
    n = 5

    def is_forest(edge_indices):
        """Check if the given edge indices form a forest in K_4-e."""
        parent = list(range(4))
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
    for k in range(n + 1):
        for S in combinations(range(n), k):
            if is_forest(S):
                indep.append(frozenset(S))
    return Matroid(n, indep)


def main():
    M = build_K4_minus_e()
    print(f"M(K_4 - edge): n={M.n}, rank={M.rank}")
    print(f"  f-vector: {M.f}")
    xv = [len(x_sets(M, k)) for k in range(M.n + 1)]
    print(f"  X-vector: {xv}  (support [n-r, r] = [{M.n-M.rank}, {M.rank}])")

    # Verify ∂*: X_2 → X_3 is invertible
    mat = bipartite_matrix(M, 2)
    print(f"\n  Bipartite ∂*: X_2({len(x_sets(M,2))}) → X_3({len(x_sets(M,3))})")
    print(f"  Matrix shape: {mat.shape}")
    rk = rank_modp(mat)
    print(f"  Rank mod p (with p=10007): {rk}")
    inj = (rk == len(x_sets(M, 2)))
    print(f"  Verdict: {'∂* INJECTIVE (rank = |X_2|)  →  HL holds on R(M)|_X' if inj else 'NOT INJECTIVE'}")

    # Print the matrix for inspection
    print(f"\n  Matrix (rows = X_3, cols = X_2):")
    Xk = x_sets(M, 2)
    Xk1 = x_sets(M, 3)
    print(f"    cols (X_2, |X_2|={len(Xk)}):")
    for j, S in enumerate(Xk):
        print(f"      col {j}: {{{','.join(str(e) for e in sorted(S))}}}")
    print(f"    rows (X_3, |X_3|={len(Xk1)}):")
    for i, S in enumerate(Xk1):
        print(f"      row {i}: {{{','.join(str(e) for e in sorted(S))}}}")
    print(f"    Matrix entries:")
    for i in range(mat.shape[0]):
        print(f"      {list(mat[i])}")

    print("""
GEOMETRIC INTERPRETATION:

For M = M(K_4 - e) (connected non-uniform matroid with multi-grade X-support):

  Y = wonderful compactification of (P^1)^5 minus the 3 matroid coord subspaces.
  Y is smooth projective Kähler of complex dim 5, with Aut(M)-invariant Kähler class
  ω̃ = (Σ x_i) - ε · (linear combination of exceptional divisors).

  By classical Kähler Hard Lefschetz on Y:
    mult ω̃: H^{2k}(Y) → H^{2(k+1)}(Y) is iso for appropriate k.

  H*(Y) decomposes via filtration by exceptional ideals:
    H*(Y) ⊃ (exceptional ideal) ⊃ (deeper exceptional ideal) ⊃ ...

  Quotient by the top exceptional ideal: R(M) = H*(Y) / (exceptional).

  R(M) restricted to X-grades (= [2,3] in our case) is the PALINDROMIC sub-piece of R(M).
  This is the Lefschetz module on which HL inherits from HL on Y.

  Specifically: the 8x8 bipartite matrix above IS the pullback-block of mult ω̃ on Y
  at H^4 → H^6, restricted to the R(M)|_X subspace.

  By the block-triangular structure: HL on Y ⟹ each diagonal block is invertible
  ⟹ the R(M)|_X block (= our ∂*) is invertible
  ⟹ HL on R(M)|_X.

ABSTRACT PROOF (template):
  1. Y_M = wonderful compactification of (P^1)^n minus matroid coord subspace arrangement.
     Smooth projective Kähler (de Concini-Procesi).
  2. Hard Lefschetz on Y_M with ω̃ = (Σx_i) - ε·(exceptional corrections).
  3. R(M) = H*(Y_M) / (exceptional ideal).
  4. R(M)|_X is the palindromic Lefschetz-stable sub-piece of R(M).
  5. HL on Y_M restricts to HL on R(M)|_X via the block-triangular decomposition.

  The remaining technical work: identify R(M)|_X concretely as the "palindromic piece"
  inside H*(Y_M). For Triangle this was manifest. For M(K_4-e), it requires explicit
  intersection theory but the structure is clear from the wonderful compactification's
  Feichtner-Yuzvinsky-style description.
""")


if __name__ == "__main__":
    main()
