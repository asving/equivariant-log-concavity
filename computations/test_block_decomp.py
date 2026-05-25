"""Test the deletion-contraction block-triangular decomposition of ∂*.

Setup:
  For matroid N on E, the X-bipartite operator ∂* : ℝ^{X_k(N)} → ℝ^{X_{k+1}(N)}
  sends A ↦ Σ_{i ∈ E\A : A∪i ∈ X_{k+1}} (A∪i).

  Fix e ∈ E. Split:
    X_k = X_k^{no e}  ⊔  X_k^{has e}
  Under this splitting, ∂* is block lower-triangular:
    ∂*(A ∈ X_k^{no e}) = (sum over i ≠ e in X_{k+1}^{no e}) + (add e if ∈ X_{k+1}^{has e})
    ∂*(A ∈ X_k^{has e}) = (sum over i ≠ e in X_{k+1}^{has e})   [adding e to a set already containing e is impossible]

  So the matrix has the block form
    [ ∂*_{no e}           0          ]
    [ +e off-diag       ∂*_{has e}   ]
  and column injectivity reduces to: both diagonal blocks have full column rank.

  The diagonal blocks are X-bipartite operators on PAIRED matroids:
    ∂*_{no e}:  X-bipartite on the pair (N\e, N/e), grade k
    ∂*_{has e}: X-bipartite on the pair (N/e, N\e), grade k-1
  where "X-bipartite on (P, Q)" = bipartite incidence on
     {A ⊆ E_common : A indep in P, complement indep in Q}.

Goal of test:
  (a) Verify the block-triangular shape (no e → has e off-diag must vanish above).
  (b) Verify both diagonal blocks are individually injective for every e.
  (c) If yes for non-paving matroids, this is the empirical evidence we need
      to attempt a Schur-complement-style inductive proof.

We test on small non-paving matroids: free-extended graphic matroids,
where M(K_n) is direct-summed with U_{r,r} to lift rank above |E|/2.
"""

from __future__ import annotations
import sys
from itertools import combinations
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid, M_Kn
from sparse_rank import sparse_rank_modp

P = 10007


# --------- Matroid X-set and bipartite construction ---------

def x_sets(M, k):
    """X_k(M) = {A indep, |A|=k, E\\A indep}."""
    E = frozenset(range(M.n))
    return [A for A in M.by_size.get(k, []) if (E - A) in M.indep]


def bipartite_entries(Xk, Xkp1, n):
    row_idx = {A: i for i, A in enumerate(Xkp1)}
    rows, cols, vals = [], [], []
    for j, A in enumerate(Xk):
        for i in range(n):
            if i in A: continue
            Ap = A | frozenset([i])
            if Ap in row_idx:
                rows.append(row_idx[Ap])
                cols.append(j)
                vals.append(1)
    return rows, cols, vals


def rank_of(rows, cols, vals, m, n):
    if n == 0 or m == 0 or not rows:
        return 0
    return sparse_rank_modp(rows, cols, vals, m, n, P, verbose=False)


# --------- Matroid constructions ---------

def free_sum(M, k):
    """M ⊕ U_{k,k} — add k free (= always-independent) elements."""
    extra_elts = list(range(M.n, M.n + k))
    new_indep = []
    for A in M.indep:
        for s in range(k + 1):
            for free_subset in combinations(extra_elts, s):
                new_indep.append(A | frozenset(free_subset))
    return Matroid(M.n + k, new_indep)


def single_triangle(extra_free):
    """Matroid on (3 + extra_free) elements: triangle circuit on {0,1,2},
    plus extra_free free elements. Rank = 2 + extra_free."""
    n = 3 + extra_free
    indep = []
    for k in range(n + 1):
        for S in combinations(range(n), k):
            S = frozenset(S)
            # Independent iff S does not contain the triangle {0,1,2}.
            if {0, 1, 2}.issubset(S):
                continue
            indep.append(S)
    return Matroid(n, indep)


# --------- Block decomposition ---------

def block_decompose(M, k, e):
    """Decompose X_k, X_{k+1} by e-content; build the three sub-matrices.
       Returns: (sizes, full_rank, diag_no_rank, diag_has_rank).
    """
    Xk = x_sets(M, k)
    Xk1 = x_sets(M, k + 1)
    Xk_no = [A for A in Xk if e not in A]
    Xk_has = [A for A in Xk if e in A]
    Xk1_no = [A for A in Xk1 if e not in A]
    Xk1_has = [A for A in Xk1 if e in A]

    n = M.n

    # Full ∂*
    rows, cols, vals = bipartite_entries(Xk, Xk1, n)
    full_rank = rank_of(rows, cols, vals, len(Xk1), len(Xk))

    # ∂*_{no e}: X_k^{no e} → X_{k+1}^{no e} (no operation touches e)
    row_idx_no = {A: i for i, A in enumerate(Xk1_no)}
    rows, cols, vals = [], [], []
    for j, A in enumerate(Xk_no):
        for i in range(n):
            if i == e or i in A: continue
            Ap = A | frozenset([i])
            if Ap in row_idx_no:
                rows.append(row_idx_no[Ap]); cols.append(j); vals.append(1)
    r_no = rank_of(rows, cols, vals, len(Xk1_no), len(Xk_no))

    # ∂*_{has e}: X_k^{has e} → X_{k+1}^{has e}
    row_idx_has = {A: i for i, A in enumerate(Xk1_has)}
    rows, cols, vals = [], [], []
    for j, A in enumerate(Xk_has):
        for i in range(n):
            if i == e or i in A: continue
            Ap = A | frozenset([i])
            if Ap in row_idx_has:
                rows.append(row_idx_has[Ap]); cols.append(j); vals.append(1)
    r_has = rank_of(rows, cols, vals, len(Xk1_has), len(Xk_has))

    # Verify the upper-right block (no e → has e via adding ≠ e) is identically zero.
    # If A ∈ X_k^{no e} and we add i ≠ e, the result has e ∉ A∪i, so lands in X_{k+1}^{no e}.
    # If we add e, lands in X_{k+1}^{has e}. So upper-right block (Xk_no → Xk1_no via +e) is just +e operation,
    # but if we restrict to "add ≠ e", upper-right is zero.

    sizes = dict(Xk=len(Xk), Xk1=len(Xk1),
                 Xk_no=len(Xk_no), Xk_has=len(Xk_has),
                 Xk1_no=len(Xk1_no), Xk1_has=len(Xk1_has))
    return sizes, full_rank, r_no, r_has


def report(M, label):
    print(f"\n{'='*70}")
    print(f"  {label}: n={M.n}, rank={M.rank}, f={M.f}")
    print(f"{'='*70}")

    # Find all (k, d) bigrades satisfying our hypothesis: 2k+d = n, rank ≥ k+d, d ≥ 2.
    n = M.n
    candidates = []
    for k in range(n + 1):
        d = n - 2 * k
        if d < 2: continue
        if M.rank < k + d: continue
        if k + 1 > M.rank: continue
        candidates.append((k, d))

    if not candidates:
        print("  No bigrade matches hypothesis (need 2k+d=n, rank≥k+d, d≥2). Skipping.")
        return

    for k, d in candidates:
        Xk = x_sets(M, k)
        Xk1 = x_sets(M, k + 1)
        if not Xk:
            continue
        rows, cols, vals = bipartite_entries(Xk, Xk1, M.n)
        full_rank = rank_of(rows, cols, vals, len(Xk1), len(Xk))
        inj = (full_rank == len(Xk))
        print(f"\n  Bigrade k={k}, d={d}: |X_k|={len(Xk)}, |X_{{k+1}}|={len(Xk1)}, "
              f"∂* rank={full_rank}  [{'INJ' if inj else 'ker='+str(len(Xk)-full_rank)}]")
        if not inj:
            print(f"  *** ∂* NOT INJECTIVE — empirical conjecture fails here, skip decomp.")
            continue

        print(f"  Block decomposition by element e ∈ E:")
        all_ok = True
        for e in range(M.n):
            sizes, full_r, r_no, r_has = block_decompose(M, k, e)
            ok_no = (r_no == sizes['Xk_no'])
            ok_has = (r_has == sizes['Xk_has'])
            ok = ok_no and ok_has
            all_ok = all_ok and ok
            flag_no = 'INJ' if ok_no else f'ker={sizes["Xk_no"]-r_no}'
            flag_has = 'INJ' if ok_has else f'ker={sizes["Xk_has"]-r_has}'
            print(f"    e={e}: |Xk_no|={sizes['Xk_no']:3d} |Xk_has|={sizes['Xk_has']:3d} | "
                  f"∂*_no:{r_no}/{sizes['Xk_no']} [{flag_no}] | "
                  f"∂*_has:{r_has}/{sizes['Xk_has']} [{flag_has}]")
        verdict = 'YES — both diagonal blocks injective for every e' if all_ok \
            else 'NO — some block fails to be injective'
        print(f"  Decomposition works for every e? {verdict}")


def main():
    tests = []

    # --- Tests: small non-paving matroids ---

    # Single triangle on 3 elements + free padding to lift rank above |E|/2.
    # n=5: 3 triangle + 2 free, rank=4, |E|=5. Bigrade 2k+d=5 → (k=1,d=3): rank≥4 ✓.
    tests.append((single_triangle(2), 'Triangle ⊕ U_{2,2}: 5 elements'))

    # n=6: rank=5. Bigrade 2k+d=6 → (k=2,d=2) rank≥4 ✓; (k=1,d=4) rank≥5 ✓.
    tests.append((single_triangle(3), 'Triangle ⊕ U_{3,3}: 6 elements'))

    # n=7: rank=6. Bigrades (k=1,d=5), (k=2,d=3) (k+d≤6).
    tests.append((single_triangle(4), 'Triangle ⊕ U_{4,4}: 7 elements'))

    # n=8: rank=7. Multiple bigrades.
    tests.append((single_triangle(5), 'Triangle ⊕ U_{5,5}: 8 elements'))

    # M(K_4) ⊕ U_{3,3}: 9 elements, rank 6, multiple triangle circuits.
    tests.append((free_sum(M_Kn(4), 3), 'M(K_4) ⊕ U_{3,3}: 9 elements'))

    # M(K_4) ⊕ U_{4,4}: 10 elements, rank 7.
    tests.append((free_sum(M_Kn(4), 4), 'M(K_4) ⊕ U_{4,4}: 10 elements'))

    for M, label in tests:
        try:
            report(M, label)
        except Exception as ex:
            print(f"\nERROR on {label}: {ex}")
            import traceback; traceback.print_exc()


if __name__ == '__main__':
    main()
