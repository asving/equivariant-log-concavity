"""Test KW-style relaxation proof of Theorem 4'-II for sparse paving matroids.

Strategy:
  1. Start from U_{r, n}. Theorem 4'-II holds (boolean Lefschetz).
  2. Repeatedly add circuit-hyperplanes (= size-r subsets that become dependent).
  3. At each step, verify Theorem 4'-II for the new matroid.
  4. If Theorem 4'-II always holds: we have a proof template for sparse paving matroids.

Key technical claim:
  Under CH-relaxation M -> M' (add F as CH), at bigrade (k, k+1) with r >= k+d, d >= 2:
    - X_{k+1}(M') = X_{k+1}(M) [since r > k+1, so A' ≠ F, and corank-1 < n-k-1 so E\\A' ≠ F]
    - X_k(M'): possibly shrinks by 1 (= removes E\\F if E\\F was in X_k(M), happens at boundary r = k+d)
    - Bipartite incidence: matrix with possibly 1 column removed.
    - rank decreases by exactly 1 (since original was full rank). Preserved.
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from sparse_rank import sparse_rank_modp
from gpu_rank import Matroid


def make_uniform_minus_chs(r, n, chs):
    """Construct U_{r,n} with specified r-subsets `chs` declared as CHs.
    chs: list of frozenset of size r."""
    indep = []
    for k in range(r+1):
        for S in combinations(range(n), k):
            S = frozenset(S)
            if k == r and S in chs:
                continue  # F is dependent
            indep.append(S)
    return Matroid(n, indep)


def X_k_set(N, k):
    E = frozenset(range(N.n))
    out = []
    for A in combinations(range(N.n), k):
        A = frozenset(A)
        if A not in N.indep: continue
        if (E - A) not in N.indep: continue
        out.append(A)
    return out


def bipartite_rank(N, k, P=10007):
    Xk = X_k_set(N, k)
    Xkp1 = X_k_set(N, k+1)
    Xkp1_idx = {A: i for i, A in enumerate(Xkp1)}
    rows, cols, vals = [], [], []
    for j, A in enumerate(Xk):
        for i in range(N.n):
            if i in A: continue
            Ap = A | frozenset([i])
            if Ap in Xkp1_idx:
                rows.append(Xkp1_idx[Ap]); cols.append(j); vals.append(1)
    if not rows: return 0, len(Xk), len(Xkp1)
    r = sparse_rank_modp(rows, cols, vals, len(Xkp1), len(Xk), P, verbose=False)
    return r, len(Xk), len(Xkp1)


def test_kw_step(r, n, ch_list, ks_to_test):
    print(f"\n=== U_{{{r},{n}}} with CHs = {[sorted(c) for c in ch_list]} ===")
    N = make_uniform_minus_chs(r, n, ch_list)
    print(f"  f-vector: {N.f}")
    for k in ks_to_test:
        d = n - 2*k
        if d < 2: continue
        if r < k + d: continue
        rk, sd, td = bipartite_rank(N, k)
        ok = rk == sd
        print(f"  k={k}, d={d}: |X_k|={sd}, |X_{{k+1}}|={td}, rank={rk}  {'✓' if ok else '✗'}")


def main():
    print("KW-style relaxation: incrementally add CHs to uniforms")
    print("="*60)

    # U_{3, 4}: rank 3, 4 elts. (k, d) candidates: 2k+d=4, k+d <= 3, d>=2.
    # (k=1, d=2): k+d=3 ✓. So test k=1.
    print("\n--- U_{3,4} family ---")
    test_kw_step(3, 4, [], [1])  # uniform
    test_kw_step(3, 4, [frozenset({0,1,2})], [1])  # 1 CH
    test_kw_step(3, 4, [frozenset({0,1,2}), frozenset({0,1,3})], [1])  # 2 CHs

    # U_{4, 6}: 2k+d=6, k+d<=4. (k=1,d=4), (k=2,d=2).
    print("\n--- U_{4,6} family ---")
    test_kw_step(4, 6, [], [1, 2])
    test_kw_step(4, 6, [frozenset({0,1,2,3})], [1, 2])
    test_kw_step(4, 6, [frozenset({0,1,2,3}), frozenset({0,1,2,4})], [1, 2])

    # U_{4, 7}: 2k+d=7, k+d<=4. (k=1,d=5)??? Let's just say (k=2,d=3).
    print("\n--- U_{4,7} family ---")
    test_kw_step(4, 7, [], [2])
    test_kw_step(4, 7, [frozenset({0,1,2,3})], [2])

    # U_{5, 8}: (k=2, d=4), (k=3, d=2)
    print("\n--- U_{5,8} family ---")
    test_kw_step(5, 8, [], [2, 3])
    test_kw_step(5, 8, [frozenset({0,1,2,3,4})], [2, 3])
    test_kw_step(5, 8, [frozenset({0,1,2,3,4}), frozenset({0,1,2,3,5})], [2, 3])

    # U_{5, 8} with MANY CHs
    chs = [frozenset(c) for c in [{0,1,2,3,4}, {0,1,2,3,5}, {0,1,2,4,5},
                                    {0,1,3,4,5}, {0,2,3,4,5}]]
    print("\n--- U_{5,8} with 5 CHs (sparse paving with many CHs) ---")
    test_kw_step(5, 8, chs, [2, 3])


if __name__ == "__main__":
    main()
