# Mason's level-walk full-rank fails; the X-restriction restores it

**Date: 2026-05-22 (session continuation).**

## The previous misunderstanding

PREPRINT_DRAFT.md (and the strategy in HANDOFF.md §16) leaned on the following (mistakenly stated as) classical fact:

> "Mason / Edmonds level-walk full-rank theorem": for any matroid `N` on `n'` elements of rank `r'`, the bipartite incidence operator `∂*: ℝ^{Indep_k(N)} → ℝ^{Indep_{k+1}(N)}` has `rank(∂*) = min(f_k, f_{k+1})`.

**This is not a theorem.** Empirical disproof on two simple graphic matroids derived from M(K_6):

| Matroid                          | n' | r' | k | f_k | f_{k+1} | rank(∂*) | min  | Deficit |
|----------------------------------|----|----|---|-----|---------|----------|------|---------|
| **N₁ = M(K_6) \| {edges 0..7}**  | 8  | 5  | 3 | 53  | 52      | **48**   | 52   | **4**   |
| **N₂ = M(K_6) \| {0..6, 9}**     | 8  | 5  | 3 | 52  | 47      | **46**   | 47   | **1**   |
| Same N₁                          | 8  | 5  | 4 | 52  | 20      | 20       | 20   | 0       |
| All tested uniforms U_{r',n'}    | —  | —  | — | —   | —       | —        | —    | 0       |
| All tested M(K_n) (whole)        | —  | —  | — | —   | —       | —        | —    | 0       |

The deficit appears precisely on submatroids where Lemma 5 (`f_k ≤ f_{k+1}`) also fails — the parallel-rich or "almost-bipartite-graph" matroids that arise as `N(C, U)` in M(K_6) at high (m, d).

Mason's actually-true statement (proven by Adiprasito–Huh–Katz / Brändén–Huh) is that the **f-vector is log-concave**: `f_k^2 ≥ f_{k-1} f_{k+1}`. That's an inequality between integer values, **not** a rank claim about the bipartite incidence matrix. The bipartite-incidence full-rank statement I attributed to "Edmonds; Stanley; Brändén–Huh / ALOGV" was conflated from several different theorems.

## What's actually true

(a) **For uniform matroids:** the bipartite incidence is the simplicial boundary, which is full rank by classical sl₂-Lefschetz on the boolean lattice.

(b) **For matroids satisfying f_k ≤ f_{k+1}:** Mason's log-concavity gives unimodality which guarantees that f is rising at level k. But this is consistent with `rank(∂*) < f_k`, as N₁ k=3 shows.

(c) **For our X-restriction:** computationally, `rank(∂*|_{X_k}) = |X_k|` always. The X-restriction is doing genuine work that the unrestricted operator cannot.

## Why the X-restriction restores rank

For N₁ at k=3:
- `ker(∂*)` on Indep_3 has dim 5 (= 53 − 48).
- 2 of the 5 kernel basis vectors live entirely in `ℝ^{Indep_3 \ X_3}` (X-trivial).
- 3 have nontrivial X_3 components.
- The 3 X-touching vectors' projections onto `ℝ^{X_3}` are linearly **independent** in `ℝ^{20}`.

Consequently `ker(∂*) ∩ ℝ^{X_3} = 0` — no linear combination of the kernel basis vectors lies entirely on X_3 coordinates.

This is the **mechanism** of Theorem 4': the X-restriction filters out the kernel directions that have all-X support, leaving a full-rank operator on `ℝ^{X_k} → ℝ^{X_{k+1}}`.

## Revised proof strategy for Theorem 4'

The proof has to engage directly with the X-restriction, not via Mason's theorem.

**Strategy I (Kernel-injects-into-X⊥):** Show that the projection `π: ker(∂*) → ℝ^{X_k}` is **injective**. Equivalently, no nontrivial kernel vector is supported only on `Indep_k \ X_k`.

This is **false** — the empirical data shows 2 kernel vectors of N₁ are supported on `Indep_3 \ X_3` only. So Strategy I doesn't work as stated.

**Strategy II (Kernel projects injectively in a different sense):** Show that the X-projections of kernel basis vectors, ignoring the X-trivial kernel vectors, are linearly independent. Equivalently: `ker(∂*) ∩ ℝ^{X_k} = 0`.

This is equivalent to Theorem 4' and what needs proving.

A possible angle: characterize `ker(∂*)` as a "syzygy module" with a free direct summand from `Indep_k \ X_k` (the "X-trivial part") and a "boundary" part with X-injective projection. The dimensions match: ker dim = (X-trivial dim) + (X-injective dim), and `|X-trivial| = f_k - f_{k+1} + (X-injective dim count)`.

For N₁: ker dim = 5, X-trivial = 2, X-injective = 3. Note `|X_k| - |X_{k+1}| + |Indep_{k+1}| - |Indep_k| =` ... hmm, let me compute. f_k - f_{k+1} = 53 - 52 = 1. The dim of ker(∂) over the integers is 5, way more than 1. So Mason's claim was off by 4.

Hmm — the actual rank deficit of N₁'s ∂* is exactly `f_k - rank(∂)` = 53 - 48 = 5? No wait, deficit = `min(f_k, f_{k+1}) - rank(∂)` = 52 - 48 = 4.

Let me parse more carefully.
- ∂* : ℝ^{Indep_k} → ℝ^{Indep_{k+1}}, dims 53 → 52.
- rank(∂*) = 48.
- ker(∂*) = ℝ^{Indep_k} kernel of dim 5.
- coker(∂*) = ℝ^{Indep_{k+1}} mod image, dim 52 - 48 = 4.

So both ker and coker are nontrivial, dims 5 and 4. Mason's claim "rank = min = 52" would give ker dim 1 and coker dim 0, which is wrong.

**Strategy III (Strict-Lorentzian on X-vector):** The polynomial `G_N(z, w) = Σ_d |X_d(N)| z^d w^{n'-d}` may be Lorentzian (in two variables), giving log-concavity / unimodality of the X-vector.

By complementation symmetry, the X-vector is palindromic: `|X_d| = |X_{n'-d}|`. So `G_N` is "self-reciprocal" in `(z, w)`. If Lorentzian, log-concavity ⇒ unimodality ⇒ peak at `n'/2`, hence `|X_k| ≤ |X_{k+1}|` for `k < n'/2` (which is our case for `d ≥ 2`). This handles the **dim** part of Theorem 4'.

The **rank** part still requires more.

**Strategy IV (Matroid intersection):** `X_k(N)` is the set of common indep sets in N and a "complement-indep" structure. By matroid duality, "E\A indep in N" ⟺ "A spans N*" ⟺ "A contains a basis of N*". For `|A| = k`, this is "A indep in N AND A indep in N* (if `k ≤ corank(N)`)" or "A indep in N AND A spans N* (if `k > corank(N)`)".

Edmonds 1970 matroid intersection theorem covers the structure of common indep sets in two matroids. For our case (intersection of N and N*), the structure might be amenable to known full-rank theorems.

## What's confirmed empirically (across more than 200k orbits)

- `|X_k| ≤ |X_{k+1}|` for `k < n'/2` (X-vector unimodality): **0 violations**.
- `rank(∂*|_{X_k}) = |X_k|` (Theorem 4'): **0 violations** (= consistent with the user's INJ being verified directly).
- `rank(∂*|_{Indep_k}) = min(f_k, f_{k+1})` (the misstated "Mason"): **FAILS** on N₁ k=3 (deficit 4), N₂ k=3 (deficit 1), and likely many other "parallel-rich-or-low-rank" submatroids of M(K_6).

## What this means for the preprint

PREPRINT_DRAFT.md v0.2 incorrectly stated Theorem 4 as a known classical result. This needs to be retracted. **Theorem 4' is the ACTUAL theorem to prove**, and it is *not* a corollary of any known matroid full-rank theorem.

The proof strategies above (especially Strategies III and IV) are concrete and worth pursuing. The X-vector palindromicity (from complementation) is suggestive of a deep structural property — perhaps a "doubled-matroid Lefschetz" or a matroid-intersection-Lefschetz framework.

## Empirical data summary (this session)

Code: `computations/sanity_check_partial.py`, `kernel_disjoint_X.py`, `simple_lemma5.py`.

| Phenomenon                                  | Status                      |
|---------------------------------------------|-----------------------------|
| User's INJ (`L: S_{-d}→S_{-d+2}` injective) | Verified on M(K_n) up to n=6, AG(3,2), Vámos, Fano, Pappus, NonPappus, all uniforms tested |
| Theorem 4' (X-bipartite full-rank)          | Verified on every orbit checked (more than 200k orbits) |
| Lemma 5 (f_k ≤ f_{k+1} per orbit)            | **FALSE** (2820/107445 orbits in M(K_6) m=3 d=2) |
| Simple-Lemma-5 (Lemma 5 restricted to simple N) | **FALSE** (N₁, N₂ above) |
| "Mason's level-walk full-rank"               | **NOT A THEOREM** (deficits 4 and 1 on N₁, N₂)  |
| X-vector palindromicity `\|X_d\| = \|X_{n'-d}\|` | Always holds (by complementation) |
| `\|X_k\| ≤ \|X_{k+1}\|` for `k < n'/2`      | Empirically always holds |
