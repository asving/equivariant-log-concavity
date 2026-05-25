# Project History — condensed journey through ideas tried

This document compresses notes 10–17 (and indirectly 01–09 in `archive/`) into a single chronological summary of the ideas explored, what worked, and what failed. The full historical notes are preserved in `archive/` (notes 01–09) and as separate files (10–18) for anyone who wants the raw record.

For the current state and the proven theorem, see `../PAPER.md` and `../README.md`. For the inductive proof itself, see `18_kw_proof_sparse_paving.md`.

---

## 2026-05-14 to 2026-05-15: Setup and exploration of the tensor Lefschetz

(See `archive/01_setup_and_inj_implies_ELC.md` through `archive/09_strategic_summary.md`.)

- Defined the matroid algebra `R(M)`, dual `R^∨(M)`, tensor space `S(M) = R(M) ⊗ R^∨(M)`, and the Lefschetz operator `L = Σ x_i ⊗ x_i`.
- Established: **ELC for the f-vector ⟺ injectivity of `L` on each bigrade `(m, -d)` for `d ≥ 2`** (Aut(M)-equivariant cokernel argument).
- Computationally verified `L` injective for U_{r,n} up to rank 10, M(K_n) for `n ≤ 6`, Fano, Vámos, Pappus, NonPappus, AG(3,2).
- Found the orbit decomposition: `L` preserves orbits indexed by `(C, U) = (S ∩ T, S ∪ T)`, with each orbit identified as a bipartite incidence on the contracted-restricted minor `N(C, U)`.
- Discovered the stronger CONJ-A (full hard Lefschetz `L^d : S_{-d} → S_d` iso) is **FALSE**: first counterexample at `M(K_5)`, `d = 2`, deficit 180.

## 2026-05-22 morning: The X-restriction and the Lemma 5 collapse

(See `10_alogv_approach.md`, `11_lemma5_fails_theorem4_holds.md`.)

- Identified `X_k(N) := { A ⊆ E(N) : |A|=k, A indep, E\A indep }` as the correct subspace where the bipartite incidence acts.
- Initial proof attempt assumed "Lemma 5": `f_k(N) ≤ f_{k+1}(N)` per orbit, which, combined with Mason's full-rank theorem on the unrestricted Indep_k → Indep_{k+1}, would close everything.
- **Lemma 5 turns out FALSE**: 2820 / 107445 orbits in `M(K_6)` at `(m, d) = (3, 2)` violate it. (The failing orbits have parallel-pair structure in `N(C, U)` from contracting an edge of K_6.) But Theorem 4'-II (the X-bipartite incidence injectivity) still holds — verified empirically on the failing orbits.

## 2026-05-22 mid-morning: Mason's "full-rank theorem" was not a theorem

(See `12_mason_fails_X_restores.md`.)

- We had been assuming a "matroid level-walk full-rank theorem" (= rank(∂*) on Indep_k → Indep_{k+1} = min(f_k, f_{k+1})). **This is not a theorem of matroids in general.** Counterexample: simple graphic matroid `N_1 = M(K_6)|_{\{0,...,7\}}` has rank deficit 4.
- Yet the X-restriction `∂*|_{X_k}` still has full rank on `N_1`. So the X-restriction does *genuine* structural work, not just inheriting from Mason.
- This made Theorem 4'-II (X-bipartite injectivity) a *new* matroid-theoretic statement, not a consequence of any classical result.

## 2026-05-22 mid-day: The X-ULC conjecture is already proven (dim half)

(See `13_X_ULC_conjecture.md`.)

- Identified the "X-ULC conjecture": `|X_d(M)|/C(n, d)` is ultra-log-concave in `d` for every matroid `M`. Empirically verified on 510+ matroids.
- **Found this is already proven** (Jan 2026): Corollary 1.7 of Ardila-Mantilla et al. (arXiv:2601.02547) — their `N_M(a, b)` is our `|X_a(M)|`. Also Theorem 3.2 of Cao-Chen-Li-Wu (arXiv:2601.03809).
- This handles the **dim half** of Theorem 4'-II (= `|X_k| ≤ |X_{k+1}|`). The remaining work is the **rank half** (= bipartite incidence injective).

## 2026-05-22 afternoon: Hall reduction — partial, with a subtle gap

(See `14_hall_reduction.md`, `16_hall_reduction_correction.md`.)

- Reformulated Theorem 4'-II as **Hall's condition on the X-bipartite graph**: for every `S ⊆ X_k`, `|N(S)| ≥ |S|`. Verified empirically across 6239 orbits.
- **Proved Hall for `d > k`** via simple double-counting: forward-degree ≥ `d`, back-degree ≤ `k+1`, ratio ≥ 1 when `d ≥ k+1`. This is a clean partial theorem.
- For `d ≤ k`: empirical only.
- **A subtle gap surfaced**: a matching covering `X_k` does NOT in general imply full column rank for a 0/1 bipartite incidence matrix. Counterexample: `K_{3,3}` at `(k=4, d=1)` (outside our hypothesis) has matching 72 but rank 68. The "Hall ⇒ rank" reduction works empirically for `d ≥ 2` but isn't itself proven.

## 2026-05-22 late afternoon: Aut-orbit Hall + concrete proof attempts

(See `15_concrete_proof_test.md`.)

- Discovered: the tightest Hall subsets are always Aut(M)-orbits. This is forced by Aut-equivariance of `∂*`.
- **Aut-orbit Hall** is the cleanest "equivariant" reformulation, directly mirroring the rep-theoretic structure of ELC.
- Verified `Aut(M(K_{2,3})) = 48` (Whitney twists give 8× more than graph Aut = 12). Single Aut-orbit of size 12 on `X_2`, neighborhood = all of `X_3`. One-paragraph proof of Theorem 4'-II for `K_{2,3}` and `K_{2,4}`.

## 2026-05-22 evening: Lorentzian path eliminated

(See `17_lorentzian_negative_result.md`.)

- Tested whether the natural multivariate lift `G̃_M(z_1,...,z_n;w_1,...,w_n) := Σ z^A w^{E\A}` (over indep partitions) is Lorentzian in 2n variables.
- **It is NOT.** Counterexample at `U_{2, 3}` (the simplest non-boolean matroid): the (n-2)-fold partial derivative gives a quadratic with 4 monomials whose Hessian has Lorentzian-incompatible signature.
- Specifically, the failure is the "matroid bipartition Plücker relation" `c_AA · c_BB = c_AB · c_BA`, which is NOT a theorem of matroids.
- **Lorentzian methods cap out at giving the dim half** (which Ardila et al. already proved). They cannot give the rank half on G̃_M. **Lorentzian path is dead.**

## 2026-05-22 night: KW relaxation works for paving — THE BREAKTHROUGH

(See `18_kw_proof_sparse_paving.md`.)

- Pivoted to Karn–Nasr–Proudfoot–Vecchi style stressed-hyperplane relaxation.
- Key insight: starting from uniform `U_{r,n}` (where Theorem 4'-II is trivially true by boolean Lefschetz), and adding circuit-hyperplanes (one or several at a time, depending on whether matroid axioms force multiple together), at the relevant bigrade `(k, d)`:
  - `X_{k+1}` is unchanged (since `r ≥ k+d ≥ k+2 > k+1`, neither `A'` nor `E\A'` can equal any `F` of size `r`).
  - `|X_k|` decreases by exactly the number of new CHs whose complements were in X_k (= 0 unless boundary case r = k+d).
  - Bipartite incidence becomes a submatrix of the original; submatrix-rank argument propagates full column rank because any subset of linearly independent columns is itself LI.
- **First PROVED Theorem 6 (ELC of f-vector) for sparse paving matroids.** Later in the same session, realized the argument extends straightforwardly to **all paving matroids** (= circuits of size ≥ rank, not just = rank). Verified computationally on a non-sparse-paving example (`U_{5,8}` with 6 CHs = all 5-subsets of `{0,...,5}`).
- Final theorem in `../PAPER.md`: ELC of f-vector for every paving matroid.

## What remains open

- Non-paving matroids (= matroids with circuits of size strictly less than rank): the relaxation operation isn't directly defined for smaller circuits, and a Schur-complement-type modification or fundamentally different methodology is needed.
- Find a geometric / cohomological framework (Eur–Huh–Larson stellahedral, augmented Chow ring) that realizes the X-bipartite incidence as a Lefschetz morphism on the cohomology of some variety — a path that could potentially give the full conjecture.

## Files relevant to the proven result

- `../PAPER.md` — the formal short paper write-up of the sparse paving theorem.
- `18_kw_proof_sparse_paving.md` — detailed proof + empirical verification table.
- `../computations/test_kw_relaxation.py` — empirical verification of the inductive step on various uniforms with CHs added.
- `../computations/test_g_tilde_lorentzian.py` — supporting negative result (G̃_M not Lorentzian).
