# Non-paving extension: key structural pattern observed

**Date: 2026-05-22 (extension session).**

## What we tested

Starting from `U_{5, 8}` and adding **valid** stressed flats (= small circuits + any forced consequences from matroid axioms), we tested whether the bipartite-incidence rank equals `|X_k|` at bigrade `(k, d) = (3, 2)`.

`computations/test_smaller_circuit_v2.py` verifies matroid validity (via the augmentation axiom) before testing each case. Invalid "matroids" (= sets of declared circuits violating circuit elimination) are flagged and skipped.

## What we found

**Every valid non-paving matroid tested has rank = |X_k|.** Furthermore, the rank decrease from the uniform `U_{r,n}` baseline equals the `|X_k|` decrease exactly:

| Matroid | f-vector | \|X_3\| | \|X_4\| | rank | \|X_4\| drop | \|X_3\| drop | rank drop |
|---|---|---|---|---|---|---|---|
| U_{5,8} | (1,8,28,56,70,56) | 56 | 70 | 56 | — | — | — |
| U + 1 triangle | (1,8,28,55,65,46) | 45 | 60 | 45 | 10 | 11 | 11 |
| U + 2 disjoint triangles | (1,8,28,54,60,36) | 36 | 54 | 36 | 16 | 20 | 20 |
| U + 2 sharing 1 + forced 4-circ | (1,8,28,54,59,34) | 32 | 48 | 32 | 22 | 24 | 24 |
| U + 1 4-circuit | (1,8,28,56,69,52) | 52 | 68 | 52 | 2 | 4 | 4 |
| U + 4-circuit + disjoint 3-circuit | (1,8,28,55,64,42) | 42 | 60 | 42 | 10 | 14 | 14 |

## The key structural observation

When going from `U_{r,n}` to a valid non-paving matroid `M` by adding stressed flats:

- Both `|X_k|` and `|X_{k+1}|` decrease (= some elements are no longer in X_k or X_{k+1} due to new dependencies).
- The bipartite-incidence matrix becomes a submatrix with both rows AND columns removed.
- **The rank decrease equals the `|X_k|` decrease (= column decrease) exactly.** The row decreases don't cause additional rank loss.

This is the key structural fact that **could power the proof for non-paving matroids**.

## What this implies, if proven

**Conjectured Theorem (extension).** For every valid matroid `M` reachable from `U_{r', n'}` by adding stressed flats (= every loopless matroid in our hypothesis), the bipartite incidence on `X_k(M) → X_{k+1}(M)` has rank `|X_k(M)|`. Hence ELC of the f-vector holds for every loopless matroid.

The key technical lemma needed is:

> **Lemma (Row-redundancy under stressed-flat addition).** In the bipartite-incidence matrix of `U_{r', n'}` at bigrade `(k, k+1)`, the rows corresponding to `X_{k+1}(U) \ X_{k+1}(M)` (= 4-subsets removed when adding stressed flats to obtain `M`) lie in the row-span of the rows corresponding to `X_{k+1}(M)` (= rows that remain).

If this lemma holds, the submatrix-rank argument from the paving proof goes through:
- Rank of `M`'s bipartite incidence = rank of corresponding submatrix of `U`'s incidence.
- Submatrix rank = full rank - col loss (by row-redundancy).
- Full rank - col loss = `|X_k(U)| - (|X_k(U)| - |X_k(M)|) = |X_k(M)|`.

## Why the lemma might be true (structural intuition)

For the bipartite incidence of `U_{r', n'}` at level `k → k+1`, the row span is the column space of the matrix, which has dimension `|X_k(U)|` (= the matrix has full column rank).

The kernel of the row-map (= rows in left-null-space) has dimension `|X_{k+1}(U)| - |X_k(U)| = C(n, k+1) - C(n, k)`.

For our hypothesis `n = 2k + d` with `d ≥ 2`: this difference is `C(n, k+1) - C(n, k)` which equals `\binom{n}{k} \cdot \frac{d-1}{k+1} \cdot \frac{1}{?}` ... let me compute: it's the standard difference between consecutive binomials.

For n = 8, k = 3: `C(8,4) - C(8,3) = 70 - 56 = 14`. So 14-dim row null-space.

When we add a stressed flat (= some small circuit), we remove rows from `X_{k+1}`. For the proof to work, these removed rows must lie in a specific 14-dim subspace of the row null-space.

This is a SPECIFIC combinatorial structure of the boolean simplicial coboundary — the row null-space corresponds to "syzygies" indexed by combinatorial objects (probably 5-subsets of [8] in our setup).

**Conjecture:** the rows corresponding to "F-stressed" 4-subsets (= 4-subsets containing F or disjoint from F, where F is a small circuit) all lie in the row null-space.

If we can prove this for a single stressed flat addition (the inductive step), the rest follows by induction.

## Concrete next steps

1. **Prove the row-redundancy lemma for single-stressed-flat addition.** This is the technical heart of the extension.

2. **Test on N₁ = M(K_6)|_{0..7}** which has triangles AND 4-cycles. If N₁ is reachable from `U_{5,8}` by adding stressed flats (probably yes via deletion-contraction sequences), the empirical full-rank verification gives evidence that the lemma holds at scale.

3. **Generalize the proof in PAPER.md** to include non-paving matroids, with the row-redundancy lemma as the new technical step.

## Files

- `computations/test_smaller_circuit_v2.py` — validity-checked test on 6 matroids.
- `computations/test_smaller_circuit_v2.log` — output.

## Honest assessment

This is a genuine empirical extension. We have:
- **Empirical pattern:** verified across all tested valid non-paving matroids.
- **Specific structural observation:** rank decrease matches `|X_k|` decrease exactly.
- **No proof yet.**

In `notes/20_attempt_row_redundancy_proof.md`, I attempted to prove this via a "row-redundancy" argument and found that the direct interpretation doesn't go through: the "rank-drop = col-drop" pattern is *equivalent to* Theorem 4'-II itself, not a simpler consequence. The 10 removed rows in the U → M_1 transition are NOT linearly dependent on the remaining rows in `M_U`; they're linearly independent. The empirical pattern emerges from a subtler structural fact involving both row and column removals together.

**What we can conclude:** the proof technique for non-paving cases requires more than a direct generalization of the submatrix-rank argument. It requires understanding the structure of `ker(∂*: Indep_k(M) → Indep_{k+1}(M))` for non-paving M, and proving that its X-projection is trivial.

## What's actually proven this session (honestly)

- For SPARSE PAVING and PAVING matroids: rigorous proof (PAPER.md).
- For valid non-paving matroids: empirically all tested cases satisfy Theorem 4'-II, with the specific structural pattern that rank drop = `|X_k|` drop. But this is equivalent to Theorem 4'-II rather than a clean stepping stone toward proving it.

The proof for non-paving matroids genuinely remains open and requires a new conceptual ingredient.
