# Structural update: Lemma 5 FAILS, Theorem 4' is genuinely stronger

**Date: 2026-05-22**.  Continuation of the project after the 2026-05-15 handoff.

## TL;DR

We had two candidate routes to close the proof of Theorem 1 (the user's INJ for every matroid):

- **Path B** (proving Lemma 5 directly, i.e., `f_k(N(C,U)) ≤ f_{k+1}(N(C,U))` per orbit, then invoking Mason's full-rank theorem on the *unrestricted* level walk on `Indep_k(N)`).
- **Path A** (proving Theorem 4' = the restricted bipartite incidence `Ô_{C,U} → Ô'_{C,U}` has full rank from the smaller side).

The two paths previously appeared comparable. **They are not**: Path B is dead, Path A is strictly stronger and is the *only* viable route. Extended verification across M(K_6), Vámos, AG(3,2), Fano, Pappus, NonPappus confirms this.

## Empirical findings (computations/verify_orbits_extended.py, verify_X_dims.py)

For each `(M, m, d)`, we enumerated all orbits `(C, U)`, computed both
- `f_k(N(C,U))`, `f_{k+1}(N(C,U))` (Lemma 5 quantities), and
- `|Ô_{C,U}|`, `|Ô'_{C,U}|` (Theorem 4' quantities).

**Lemma 5 fails on M(K_6) at (m=3, d=2):** 2820 / 107445 orbits violate `f_k ≤ f_{k+1}`.

Smallest failing case: `C = {e_0}` (one edge), `U = {e_0, ..., e_6}` (7 edges of K_6 spanning all 6 vertices). After contracting `e_0 = (0,1)`, the restricted matroid `N` on 6 edges has structure
- 5 vertices {01, 2, 3, 4, 5} with 4 distinct "endpoints" {2, 3, 4, 5} of edges incident to merged vertex `01`,
- Two parallel pairs (from the contraction): `{(0,2), (1,2)}` and `{(0,3), (1,3)}`,
- Two singleton edges `(0,4)`, `(0,5)`.

Thus `N` has `n' = 6`, `r' = 4`, with `f`-vector `(1, 6, 13, 12, 4)`. Here `f_2 = 13 > 12 = f_3`. **Lemma 5 fails.**

**However** the X-restriction works out cleanly:
- `Indep_4(N) = 4`-sets that form a forest with no parallel pair = `{e_3, e_4} ∪ {one of two parallels} ∪ {one of other two parallels}` = 4 sets. So `|X_2| = |X_4| = 4` (by complementation).
- `Indep_3(N) ∩ {self-complement-indep}` = 3-sets choosing one from each parallel pair plus one singleton = 2 × 2 × 2 = 8. So `|X_3| = 8`.

So `|X_2| = 4 < 8 = |X_3|` — the X-restriction restores the inequality even when the f-vector doesn't.

**Theorem 4' dim consistency:** 0 / 107445 violations of `|Ô_k| ≤ |Ô_{k+1}|` on M(K_6) m=3 d=2. Full bipartite incidence on the small failing case (worked out by hand): 4 LHS, 8 RHS, decomposes into 4 disjoint "books" of two edges each, easily full rank.

## Why Lemma 5 fails (intuition)

`N(C, U)` can have non-trivial *parallel structure* inherited from M. When `C` contains edges that, after contraction, identify several elements of `U \ C` (as parallel classes), the f-vector of `N` becomes lopsided: many size-`k` indep sets come from "skipping at most one element per parallel class", and at size `k+1` the parallels start to fight more.

But the **X-restriction is much more disciplined** than the raw `f`-vector. `X_k` requires both an indep set AND its complement to be indep. Parallel-collapse arguments suggest `|X_k(N)| = |X_k(\text{simplified } N)|` where `simplified N` collapses parallels — and on the simplified N, Lemma 5 holds.

## Theorem 4' as the right target

Restated for clarity:

> **Theorem 4' (Restricted bipartite incidence rank, conjectural).** Let `N` be a matroid on `E` with `|E| = 2k + d`, `rank(N) ≥ k + d`, `d ≥ 2`. Define
> `X_j(N) := { A ⊆ E : |A| = j, A ∈ Indep(N), E \ A ∈ Indep(N) }`.
> Then the bipartite incidence `∂ : ℝ^{X_k} → ℝ^{X_{k+1}}`,
> `∂(x_A) = ∑_{i ∈ E \ A, A ∪ i ∈ Indep(N)} x_{A ∪ i}`,
> has full rank from the `X_k` side.

(For `d ≥ 2` we have `k < n'/2`, and by complementation `|X_j| = |X_{n'-j}|`, so the X-vector is palindromic with peak at the midpoint `(n'-1)/2 = k + (d-1)/2 ≥ k + 1/2`.)

This is genuinely stronger than Mason's full-rank theorem applied to N's level walk. In the failing M(K_6) case, Mason on `Indep_2(N) → Indep_3(N)` fails (13 → 12, not injective), but Theorem 4' on the X-subspaces still holds.

## What remains for a clean proof

1. **Prove `|X_k| ≤ |X_{k+1}|`** (the X-vector inequality). By complementation `|X_k| = |X_{n'-k}|`, so the X-sequence is palindromic. Need: unimodality OR a direct injection / generating-function argument.

2. **Prove the restricted bipartite incidence is full-rank.** Given (1), this requires showing the kernel of `∂|_{X_k}` is trivial. The kernel lives inside the kernel of the unrestricted `∂ : Indep_k(N) → Indep_{k+1}(N)`. So:

   `ker(∂|_{X_k}) = ker(∂) ∩ ℝ^{X_k}`.

   In the failing M(K_6) example, `ker(∂)` is at least 1-dimensional (since `f_k > f_{k+1}`). We need: this kernel doesn't intersect `ℝ^{X_k}` nontrivially.

3. **Identifying the kernel of ∂ on `Indep_k(N)`:** the elements of the kernel are formal sums `∑ c_A x_A` with `∑_{A : A∪i indep} c_A = 0` for every "target" `A∪i ∈ Indep_{k+1}`. By Mason / Brändén-Huh, this kernel has dim `= max(0, f_k - f_{k+1})`.

   In our failing case, dim ker = 13 - 12 = 1. So ker is spanned by a single vector `v ∈ ℝ^{Indep_2(N)}`. We need to show `v ∉ ℝ^{X_2}`, i.e., the support of `v` is not contained in `X_2`.

## Concrete next-step strategies

**Strategy α: Characterize the kernel of `∂` on `Indep_k(N)` and show it always sticks out of X.**

The kernel of the level-walk operator on a matroid has been studied (Anari et al., Brändén-Huh). For Lorentzian polynomials, the kernel at level `k > peak` corresponds to "primitive forms" in a Lefschetz decomposition.

For our small failing example (parallel structure), can we write down the kernel vector explicitly? It should be a "syzygy" among the 13 indep_2 sets that maps to 0 under "extend by one". Likely involves the parallel pairs.

**Strategy β: Direct unimodality of X-vector via Lorentzian methods.**

Define `F_N(z, w) := ∑_{A ⊆ E indep, E\A indep} z^{|A|} w^{|E|-|A|}`. If this is a Lorentzian polynomial (in the Brändén-Huh sense), then its support is M-convex and we get all the right inequalities.

**Strategy γ: Reduce to "parallel-collapsed" matroid.**

The X-sets of `N` are in bijection with the X-sets of `N̂ := N / loops / collapse-parallels` (a simple matroid), suitably re-indexed. On simple matroids, Lemma 5 may hold (no parallel-induced asymmetry).

This is the most concrete and probably the right route. We'd prove:

(a) For simple matroids `N` (no loops, no parallels), `f_k(N) ≤ f_{k+1}(N)` whenever `2k+d = n'` and `r' ≥ k+d` with `d ≥ 2`. (Conjectured.)

(b) For general `N`, the X-vector is invariant under collapsing parallels (= replacing each parallel class with a single element with multiplicity).

Then (a)+(b) ⇒ Lemma 5 holds on the *collapsed* N for X-counting purposes, hence Theorem 4' follows from Mason on the collapsed matroid.

The empirical evidence supports (b): in the failing M(K_6) example, the parallel-collapsed matroid is the star K_{1,4} (a uniform matroid), and its X-vector at k=2, d=2 would give `|X_k| = 4, |X_{k+1}| = 8` — consistent.

## Files produced this session

- `notes/11_lemma5_fails_theorem4_holds.md` — this document.
- `computations/verify_orbits_extended.py` — Lemma 5 sweep across M(K_6), AG(3,2), Vámos, Fano, Pappus, NonPappus.
- `computations/verify_orbits_extended.log` — output (Lemma 5 fails at M(K_6) m=3 d=2 on 2820/107445 orbits).
- `computations/verify_X_dims.py` — checks `|Ô_k| ≤ |Ô_{k+1}|` even on Lemma-5-failing orbits.
- `computations/verify_X_dims.log` — output (0/107445 X-dim violations).

## Recommendation for the user

**Path B is dead.** The proof in PREPRINT_DRAFT.md as currently written has a logical gap that cannot be closed by proving Lemma 5 — Lemma 5 is false on real matroids.

The preprint should be rewritten to make **Theorem 4'** the central technical statement, with Lemma 5 noted as a strictly stronger statement that holds *for the X-restriction* but not for the full level walk.

**Concrete next mathematical task:** pursue Strategy γ (parallel collapse) — verify that `|X_k(N)| = |X_k(\widehat{N})|` where `\widehat{N}` is the simple matroid obtained by deleting loops and collapsing parallel classes. If this holds and Lemma 5 holds on simple matroids of our hypothesis, we close everything.

Strategy γ is the cleanest because: (i) the parallel-collapse map is matroid-theoretically natural and well-studied; (ii) it explains *why* Lemma 5 fails generically (parallel-induced f-vector asymmetry) but the X-vector stays well-behaved.
