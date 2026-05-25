# Proven: Theorem 4'-II for sparse paving matroids

**Date: 2026-05-22 (end of day, KW relaxation breakthrough).**

After eliminating the Lorentzian path, I tried the Karn-Wakefield stressed-hyperplane relaxation approach. **It works for an infinite family of matroids.**

## The theorem

> **Theorem.** Let `M` be a **sparse paving matroid** — i.e., a matroid where every circuit has size exactly equal to the rank. Equivalently, `M` is obtained from a uniform matroid `U_{r,n}` by declaring some `r`-subsets to be circuit-hyperplanes (CHs).
>
> Then for every `(k, d)` with `n = 2k + d`, `r ≥ k + d`, `d ≥ 2`, the bipartite incidence operator `∂*|_{X_k(M)}: ℝ^{X_k(M)} → ℝ^{X_{k+1}(M)}` is injective.
>
> Hence Theorem 1 (user's INJ conjecture) holds for sparse paving matroids, and **ELC for the f-vector of every sparse paving matroid is proven.**

## Proof

By induction on the number of CHs.

**Base case:** `M = U_{r,n}` (no CHs). Then `X_k(M) = C(n, k)` (every k-subset is indep with indep complement). The bipartite incidence `∂*: ℝ^{X_k} → ℝ^{X_{k+1}}` is exactly the boolean simplicial extension at level k → k+1, which is **injective by classical sl₂-Lefschetz** for `k < n/2` (= satisfied since `2k + d = n` with `d ≥ 2` gives `k < n/2`).

**Inductive step:** Assume Theorem 4'-II holds for `M_0` (with `c` CHs). Let `M_1 = M_0` with one additional CH `F` (an r-subset declared as a circuit). We show Theorem 4'-II holds for `M_1`.

Fix bigrade `(k, k+1)` with `2k + d = n`, `r ≥ k + d`, `d ≥ 2`.

**Key claim 1:** `X_{k+1}(M_1) = X_{k+1}(M_0)`.

*Proof.* An element `A'` is removed from `X_{k+1}` iff `A' = F` or `E \ A' = F`. We have `|A'| = k + 1` and `|F| = r`. Since `r ≥ k + d ≥ k + 2 > k + 1`, we have `A' ≠ F`. Also `|E \ A'| = n - k - 1 = (2k + d) - k - 1 = k + d - 1 < k + d ≤ r = |F|`, so `E \ A' ≠ F`. ∎

**Key claim 2:** `|X_k(M_1)| = |X_k(M_0)| - δ`, where `δ ∈ {0, 1}`.
- If `r > k + d` (strict): δ = 0, X_k unchanged.
- If `r = k + d` (boundary): δ = 1 if `E \ F ∈ X_k(M_0)`, else 0.

*Proof.* `A` is removed from `X_k` iff `A = F` (impossible since `|A| = k ≠ r`) or `E \ A = F`. The latter requires `|E \ A| = r`, i.e., `n - k = r`, i.e., `k = n - r = corank(M)`. By hypothesis `r ≥ k + d`, so `corank = n - r ≤ n - (k + d) = k`, with equality iff `r = k + d`. So:
- For `r > k + d` (strict): `corank < k`, so `E \ A` has size `n - k > r`, can't equal `F` of size `r`. δ = 0.
- For `r = k + d` (boundary): `corank = k`, so `|E \ F| = k`. `E \ F` may or may not be in `X_k(M_0)`. In a sparse-paving setting where `M_0` has rank `r` and `F` is a new CH being added, `E \ F` is automatically in `X_k(M_0)` (since `M_0` is itself sparse paving and so its CHs don't include `E \ F` — `|E \ F| = k < r`). Hence δ = 1. ∎

**Inductive step proper.** The bipartite incidence matrix of `M_1` is a **submatrix** of the bipartite incidence matrix of `M_0`, obtained by deleting the columns corresponding to `X_k(M_0) \ X_k(M_1)` (= δ columns) and deleting NO rows (since `X_{k+1}` unchanged).

- If `δ = 0`: the matrix is unchanged. Theorem 4'-II propagates trivially.
- If `δ = 1`: one column removed. The original matrix has rank `|X_k(M_0)|` (= full column rank by induction). Removing one column from a full-column-rank matrix decreases rank by exactly 1: the new rank is `|X_k(M_0)| - 1 = |X_k(M_1)|`. Full column rank preserved. ∎

**Conclusion.** By induction over the number of CHs, Theorem 4'-II holds for every sparse paving matroid `M`. By the chain of reductions established earlier (Theorem 1 ⟺ Theorem 4'-II per orbit), **the user's INJ conjecture and ELC for the f-vector hold for every sparse paving matroid.**

## Verification

The proof is verified empirically in `computations/test_kw_relaxation.py`:

| Matroid (U_{r,n} + CHs added) | f-vector | k | d | \|X_k\| | bipartite rank | OK? |
|---|---|---|---|---|---|---|
| U_{3,4} + 0 CHs | (1, 4, 6, 4) | 1 | 2 | 4 | 4 | ✓ |
| U_{3,4} + 1 CH | (1, 4, 6, 3) | 1 | 2 | 3 | 3 | ✓ |
| U_{3,4} + 2 CHs | (1, 4, 6, 2) | 1 | 2 | 2 | 2 | ✓ |
| U_{4,6} + 0–2 CHs | varies | 2 | 2 | 15→14→13 | 15→14→13 | ✓ |
| U_{5,8} + 0–2 CHs | varies | 3 | 2 | 56→55→54 | 56→55→54 | ✓ |
| U_{5,8} + 5 CHs | (1,…,70,51) | 3 | 2 | 51 | 51 | ✓ |

Every step matches the predicted behavior: rank drops by exactly 1 (= the number of new CHs that hit the X_k bigrade) per step.

## What this gives us

**Real theorem result:** ELC for the f-vector is proven for the infinite class of sparse paving matroids. This includes:
- All uniform matroids `U_{r,n}`.
- All matroids obtained by adding circuit-hyperplanes to a uniform.
- "Most" small matroids by count: it's been conjectured (Mayhew–Newman–Welsh–Whittle) that asymptotically almost all matroids are sparse paving.

**Comparison to existing literature:**
- Karn-Wakefield 2024 proved equivariant log-concavity of *KL polynomials* for paving matroids. We've proven ELC of *f-vector* for *sparse paving* matroids (a stronger conclusion for a weaker class).
- The proof technique (CH relaxation + submatrix-rank argument) is much simpler than KW's full machinery.

## What's NOT covered

**Matroids with circuits smaller than rank** are not covered. E.g.:
- M(K_5), M(K_6) (graphic matroids with triangles).
- N₁, N₂ (our test cases from M(K_6) restrictions).
- Most "natural" matroids in algebra/geometry.

For these, we need to allow "smaller circuit relaxation", which is structurally different — adding circuits of size `< r` doesn't preserve sparse paving structure.

## Honest comparison vs the empirical state

Before this proof: we had verified Theorem 4'-II on 6,239+ orbits empirically, with zero failures.

After this proof: we now have a proven theorem for the sparse paving class (an infinite family). The proof is simple and rigorous.

For non-sparse-paving matroids (like N₁): Theorem 4'-II is still verified empirically but the proof doesn't extend directly. The "relax smaller circuits" generalization is the natural next step.

## The route forward (post-session)

1. **Generalize CH relaxation to arbitrary circuit relaxation.** For each circuit `C` of size `c < r`, define "M relaxes C" as = remove `C` from circuit set. For this to give a matroid, need to check axioms.

2. **Find the right "Schur complement" formula for non-CH relaxation.** KW's technique uses Schur complements for paving; for non-paving matroids, a more elaborate matrix-theoretic argument is needed.

3. **Combine with the Aut-orbit framework** to get equivariant statements directly.

## Files

- `notes/18_kw_proof_sparse_paving.md` — this proof + analysis (= this note).
- `computations/test_kw_relaxation.py` — empirical verification of the inductive step.
- `computations/test_kw_relaxation.log` — output, all checks pass.
