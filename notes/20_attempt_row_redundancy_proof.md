# Attempt: prove rank-drop = column-drop for the one-circuit case

**Date: 2026-05-22 (extension session, continued).**

The empirical pattern from `notes/19`: when going from `U_{r, n}` to `M = U_{r, n} + 1 small circuit F`, the bipartite-incidence rank drops by exactly `|X_k| drop`, *not* the larger `|X_k| drop + |X_{k+1}| drop`.

We attempt to understand why structurally.

## Setting (concrete: n=8, r=5, k=3, F a 3-circuit)

`U = U_{5,8}` has bipartite incidence matrix `M_U` of size `70 × 56`, full column rank 56.

`M = U + F as 3-circuit` has bipartite incidence `M_M`. Empirically, `M_M` is the submatrix of `M_U` obtained by removing:
- 11 columns: `F` itself (now dep in `M`) and the 10 3-subsets `A ⊆ E \ F` (whose complement contains `F`).
- 10 rows: `F ∪ {x}` for `x ∈ E \ F` (5 rows, now dep in `M`) and 4-subsets `A' ⊆ E \ F` (5 rows, complement contains `F`).

After this removal: `M_M` is `60 × 45` with rank 45 = `|X_3(M)|`.

## What we need

`rank(M_M) = 45` is equivalent to: the 45 remaining columns are linearly independent when restricted to the 60 remaining rows.

The full 56 columns of `M_U` are LI in `ℝ^{70}` (= row space of `M_U`). Restricting to 60 rows (= projecting onto a 60-dim subspace of `ℝ^{70}`): the columns may or may not stay LI.

For the 45 specific columns (= `X_3(M)`): they stay LI in `ℝ^{60}`.

**Question: what's the structural reason?**

## Attempt: characterize the left null-space and check which rows lie in it

The left null-space of `M_U` has dimension `C(8, 4) - C(8, 3) = 70 - 56 = 14`. A vector `v ∈ ℝ^{70}` (indexed by 4-subsets) is in the left null-space iff for every 3-subset `A`:
`Σ_{x ∈ E \ A} v_{A ∪ {x}} = 0`.

There are `C(8, 3) = 56` such equations, with rank 56 (= full column rank means equations are independent).

The 14-dim left null-space corresponds to "syzygies" of the boolean simplicial coboundary.

**Goal:** Show that the 10 removed rows lie in some specific 11-dim subspace of the row space, allowing 11 columns to be "covered" by the remaining 45.

Hmm — this didn't quite work in my analysis attempt. Let me try a different angle.

## A more promising frame: SVD / linear-algebra restriction

The 56 columns of `M_U` are LI in `ℝ^{70}`. They span a 56-dim subspace `V ⊆ ℝ^{70}`.

Restricting to 60 specific rows: the columns project to `ℝ^{60}`. The kernel of the projection map is `ℝ^{10}` (the 10 removed rows).

For columns to stay LI in `ℝ^{60}`: need `V ∩ ker(projection) = 0`, i.e., no element of `V` is supported entirely on the 10 removed rows.

We *don't* need this for all 56 columns — only for the specific 45 columns of `X_3(M)`.

**Refined question:** is `\text{span}(X_3(M)\text{-columns}) ∩ \text{ker(projection)} = 0`?

For the 45 cols of `X_3(M)`, viewed as elements of `ℝ^{70}`: each col `A` has support on its 5 4-supersets `A ∪ {x}` for `x ∈ E \ A`.

For `A ∈ X_3(M)`: A's 5 supersets are split between X_4(M) (= remaining rows) and X_4(U) \ X_4(M) (= removed rows). Specifically:
- A 4-superset `A ∪ {x}` is in X_4(M) iff it's not in the 10 removed rows.
- A 4-superset is in the removed 10 iff `A ∪ {x} \supseteq F` or `A ∪ {x} \subseteq E \ F`.

For `A ∈ X_3(M)` (so `A ≠ F` and `A \not\subseteq E \ F` i.e., `A` intersects `F`):
- `A ∪ {x} \supseteq F` requires `F \subseteq A \cup \{x\}`, i.e., `F \setminus A \subseteq \{x\}`. Since `A` intersects F and `|A| = 3, |F| = 3`, `|F \setminus A| = |F| - |A \cap F|`. For F \ A to be `\{x\}`: need `|F \setminus A| = 1`, i.e., `|A \cap F| = 2`.

So `A ∪ {x} \supseteq F` iff `|A \cap F| = 2` AND `x = F \setminus A`. In this case `A \cup \{x\} = F \cup (A \setminus F)`. With `|A \cap F| = 2`, `|A \setminus F| = 1`, so `A \cup \{x\} = F \cup \{A \setminus F\}`.

- `A ∪ {x} \subseteq E \ F` requires `A \subseteq E \ F` AND `x \in E \ F`. But we assumed `A ∈ X_3(M)` so `A \cap F \neq \emptyset` (else `E \setminus A \supseteq F` and `A \notin X_3(M)`). So `A \not\subseteq E \setminus F`, hence this case doesn't occur for `A ∈ X_3(M)`.

So **for `A ∈ X_3(M)`, the only "removed" 4-supersets are of the form `F \cup \{y\}`**, occurring exactly when `|A \cap F| = 2` (in which case there's exactly one such removed superset). For `|A \cap F| = 1` or `|A \cap F| = 3` (= A = F, but A ∈ X_3(M) excludes this), no removed supersets.

Counting:
- `|A \cap F| = 1`: number of such A = `C(3, 1) · C(5, 2) = 3 · 10 = 30`. All 5 4-supersets are in X_4(M); no removed supersets.
- `|A \cap F| = 2`: number of such A = `C(3, 2) · C(5, 1) = 3 · 5 = 15`. Of the 5 4-supersets, 1 is removed (`F \cup \{A \setminus F\}`) and 4 are in X_4(M).

Total `A ∈ X_3(M)`: 30 + 15 = 45 ✓.

## The key observation

For columns indexed by `A ∈ X_3(M)`:
- 30 columns (with `|A \cap F| = 1`): 5 nonzero entries, all in `X_4(M)` (kept rows).
- 15 columns (with `|A \cap F| = 2`): 5 nonzero entries, 4 in `X_4(M)` and 1 in the removed 5 rows of form `F ∪ \{y\}` (where `y = A \setminus F`).

So among the 10 removed rows:
- 5 rows of form `F ∪ \{y\}`: each has nonzero entries from the 15 "|A ∩ F| = 2" columns (specifically, 3 of them have `A \setminus F = \{y\}`, all with `|A ∩ F| = 2`).
- 5 rows of form `A' \subseteq E \setminus F`: NONE of the X_3(M) columns map here (we showed above).

**So 5 of the 10 removed rows are trivially "uninvolved" for X_3(M)-columns** — those columns have zero entries in these rows. Removing these 5 rows doesn't affect the column rank.

For the OTHER 5 removed rows (= `F ∪ \{y\}`): these have nonzero entries from 3 specific X_3(M)-columns (= the 3 columns A with `A ∩ F = \{F \setminus \{y\}\}`... wait let me redo).

For each row `F \cup \{y\}` (y ∈ E \ F): its sub-3-sets are `F \cup \{y\} \setminus \{z\}` for `z ∈ F \cup \{y\}`. For `z = y`: sub = `F` (= circuit, NOT in X_3(M)). For `z \in F`: sub = `F \setminus \{z\} \cup \{y\}` (= 3-set with |∩ F| = 2). So 3 sub-cols in X_3(M) of size-2 intersection type.

So row `F \cup \{y\}` has nonzero entries in 3 specific X_3(M)-columns (= those with |A∩F|=2 and A \ F = {y}).

For these 5 "informative" removed rows: do they constrain rank of X_3(M)-columns?

If we DON'T remove these rows (= keep them in the matrix): X_3(M)-columns have specific entries in these rows. Some linear combinations of cols could "use" these rows.

If we DO remove these rows: those entries are erased; some col-combinations might become zero.

For full col rank to be preserved: no nontrivial col-combination has support entirely in these 5 removed rows.

To check: does there exist a nontrivial linear combination `Σ c_A x_A` (with `A ∈ X_3(M)`) such that the result is supported only on the 5 removed rows `F ∪ \{y\}`?

Equivalently: for every row `A' ∈ X_4(M)`, `Σ_{A ⊂ A', A ∈ X_3(M)} c_A = 0`.

This is exactly the equation for `c` to be in the kernel of `M_M` (= M's bipartite incidence). Empirically `ker(M_M) = 0`. So no such non-trivial combination. So the 45 cols are LI on the 60 remaining rows. ✓

So the empirical full-rank IS equivalent to ker(M_M) = 0. That's just restating Theorem 4'-II.

## Stepping back: this doesn't give a proof, but clarifies the structure

The "rank-drop = column-drop" empirical pattern doesn't have a clean structural reason beyond `ker(M_M) = 0` itself (= Theorem 4'-II for M).

So the question is back to: prove ker(M_M) = 0 for non-paving M.

## A different structural angle

For non-paving M, the kernel of `∂*` on Indep_k(M) is non-trivial (since `f_k(M) > f_{k+1}(M)` sometimes). But the kernel intersects ℝ^{X_k(M)} trivially.

We could try to characterize ker(∂*) ⊆ ℝ^{Indep_k(M)} explicitly and show it has trivial X-projection.

For our test case (U + 1 triangle): ker(∂*) on Indep_k(M) has dim = `f_3(M) - rank(∂*)`. We have `f_3(M) = 55` (= U has 56, minus 1 for F). `rank(∂*: Indep_3(M) → Indep_4(M))` =? Need to check empirically.

If full rank ≤ min(f_3, f_4) = min(55, 65) = 55: then no kernel, and `∂*|_{Indep_3(M)}` is injective. Then `∂*|_{X_3(M)}` (= restriction) is automatic injective. Theorem 4'-II holds trivially.

If full rank = 45 (= equal to |X_3(M)|): then kernel has dim 10. We'd need to check if kernel intersects X_3(M) trivially.

For sparse paving M = U + 1 CH F: ∂* on Indep_k is "almost full rank" (= rank = f_k - 1, perhaps). For non-paving M with smaller circuit F: ∂*'s rank could be lower.

I don't have an empirical check of `rank(∂*: Indep_3(M) → Indep_4(M))` vs `|X_3(M)|` for the non-paving case. Let me suggest this as the next concrete test.

## Conclusion

The empirical "rank-drop = col-drop" pattern is restating Theorem 4'-II for non-paving M. It doesn't simplify the proof.

A genuine proof of the non-paving case requires understanding the kernel structure of `∂*` on `Indep_k(M)` and showing the X-projection is injective.

This is the same problem we faced before. Progress requires either:
- (i) New combinatorial / structural understanding of matroid kernel of ∂*.
- (ii) A different framework (= not the relaxation chain) that handles non-paving directly.

For the proof to extend cleanly à la sparse / paving, we'd need the **stressed-flat relaxation operation for non-CH stressed flats** to behave in a way that preserves the "submatrix-rank propagation" structure. This is what KNPV develop in detail for KL polynomials; adapting to the f-vector remains open.
