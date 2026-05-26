# Note 33 — Structural proof attempt: Hall + matroid structure (2026-05-25)

## Goal

Prove the project's conjecture (PAPER §5.3) directly:

> For every loopless matroid M and every bigrade (m, d) with `2m+d ≤ n`, `m+d ≤ rank(M)`, `d ≥ 2`, the operator `∂*: ℝ^{X_m(M)} → ℝ^{X_{m+1}(M)}` is injective.

via a structural combinatorial argument (Hall's marriage theorem + matroid properties), without explicit cohomology computation.

## Setup

For matroid M of rank r on n elements with X(M) = balanced indep bipartitions, the bipartite graph G_M(m) has:
- Parts: X_m(M), X_{m+1}(M).
- Edges: (A, A∪i) for A ∈ X_m, A∪i ∈ X_{m+1}.

For ∂* to be column-injective: equivalent (König/Hall) to existence of a perfect matching from X_m into X_{m+1}, i.e., Hall's marriage condition `|N(S)| ≥ |S|` for all `S ⊆ X_m`.

## Forward and back degrees

**Forward degree** of A ∈ X_m: `fwd(A) = #{i : A∪i ∈ X_{m+1}}`.

For A ∈ X_m: A indep, E\A indep. `A∪i ∈ X_{m+1}` requires A∪i indep AND E\(A∪i) indep. The second is automatic (subset of indep E\A is indep). So `fwd(A) = #{i ∈ E\A : i ∉ closure(A)} = (n-m) - |closure(A)\A|`.

**Lower bound on fwd:** Since A is indep of size m and `rank(M) ≥ m+d ≥ m+2`, A can be extended to a basis using at least `d` further elements. So `fwd(A) ≥ d ≥ 2`. More generally, `fwd(A) ≥ rank(M) - m`.

**Back degree** of A' ∈ X_{m+1}: `bwd(A') = #{e ∈ A' : A'\{e} ∈ X_m}`.

For A' ∈ X_{m+1}: A'\{e} ∈ X_m requires A'\{e} indep (automatic) AND E\(A'\{e}) = (E\A')∪{e} indep. The latter requires `e ∉ closure(E\A')`.

So `bwd(A') = (m+1) - |A' ∩ closure(E\A')|`.

**Lower bound on bwd:** Since E\A' is indep with `rank(E\A') = m+d-1 < m+d ≤ rank(M)`, the closure `closure(E\A')` has rank `m+d-1 < rank(M)`. So `closure(E\A') ⊊ E`. Since A' adds rank to E\A' (because A'∪(E\A') = E and `rank(E) = rank(M) > rank(E\A')`), at least one element of A' lies outside `closure(E\A')`. So **`bwd(A') ≥ 1`** for every A' ∈ X_{m+1}.

**Upper bound on bwd:** `bwd(A') ≤ m+1`.

## Hall via min-fwd / max-bwd

By double counting edges:

`Σ_{A ∈ S} fwd(A) = |edges from S| ≤ |N(S)| · max_bwd`

`|S| · min_fwd ≤ Σ_{A ∈ S} fwd(A)`

Combining: `|N(S)|/|S| ≥ min_fwd / max_bwd`.

For Hall (`|N(S)| ≥ |S|`): need `min_fwd ≥ max_bwd`.

With our bounds: `min_fwd ≥ rank - m`, `max_bwd ≤ m+1`. So Hall holds whenever:

> **`rank(M) ≥ 2m + 1`.**

For d≥2 hypothesis: `rank ≥ m+d`. So we need `m+d ≥ 2m+1`, i.e., **`d ≥ m+1`**.

**Hall covers exactly the bigrades with d ≥ m+1.**

## Status of bigrades

For d≥2 hypothesis bigrade (m, d) with `2m+d = n`:

- **Hall covers**: `d ≥ m+1`, i.e., `n-2m ≥ m+1`, i.e., `m ≤ (n-1)/3`.
- **Hall doesn't cover**: `m > (n-1)/3` but `m ≤ (n-2)/2`.

For small n, the gap is empty or one bigrade:
- n ≤ 4: Hall covers all hypothesis bigrades.
- n = 5: Hall covers m ≤ 1; hypothesis allows m ≤ 1.5. So only m=1, covered.
- n = 6: Hall covers m ≤ 1.67; hypothesis allows m ≤ 2. **Gap at m=2.**
- n = 7: Hall covers m ≤ 2; hypothesis m ≤ 2.5. Only m ∈ {1,2}, covered.
- n = 8: Hall covers m ≤ 2.33; hypothesis m ≤ 3. **Gap at m=3.**
- n = 9: Hall covers m ≤ 2.67; hypothesis m ≤ 3.5. **Gap at m=3.**
- n = 10: Hall covers m ≤ 3; hypothesis m ≤ 4. **Gap at m=4.**

So Hall handles all but a **single boundary bigrade** per even n.

## The boundary bigrade

The "gap" bigrade for even n is approximately `(m, d) ≈ (n/2 - 1, 2)`. Specifically `m = (n-2)/2, d = 2`. This is the "tightest" bigrade — same as the d=2 case in the project's main conjecture.

For this boundary: `rank ≥ m+2 = n/2`, exactly half the ground set.

**This boundary case is exactly the d=2 "critical" case** in the project's main conjecture (PAPER §5.3 was already restricted to d≥2; this is the smallest d=2 case).

For the boundary case Hall via min-fwd / max-bwd fails. But Hall's condition might still hold via a stronger argument:

### Refined Hall analysis (incomplete)

For Hall: |N(S)| ≥ |S| for every S ⊆ X_m. We don't need uniform `min_fwd ≥ max_bwd`; we need set-dependent inequality.

Specifically: for each S, `Σ_{A ∈ S} fwd(A) ≤ |N(S)| · max_bwd_in_N(S)`. If we can show `max_bwd` over N(S) is small or `Σ fwd` is large for "bad" S, Hall might still hold.

This is matroid-specific. For matroids in the d=2 hypothesis with rank = n/2 + 1 (the boundary): the matroid is "thick at the middle" — many indep sets of size m+1.

### Two specific approaches for the boundary

**Approach A: matroid-specific upper bound on bwd.**
For A' ∈ X_{m+1} at the boundary: `bwd(A') = (m+1) - |A' ∩ closure(E\A')|`. The intersection `A' ∩ closure(E\A')` depends on the matroid. For "spread out" matroids (= flats are small): the intersection is small, so bwd is large. For "concentrated" matroids: bwd is small. Empirically, the matroids where Hall would fail (= bwd ≈ m+1) have a specific concentrated structure that doesn't arise within the d≥2 hypothesis.

**Approach B: direct kernel analysis.**
At the boundary d=2: ∂* takes |X_m| → |X_{m+1}|. If |X_m| = |X_{m+1}| (palindromic), ∂* is a square matrix. Its determinant has a specific form related to matroid combinatorics. For matroids in d≥2 hypothesis, the determinant should be non-zero (empirically verified).

For paving matroids: the boundary case is the d=2 case in the proven theorem (PAPER §4). The proof uses stressed-hyperplane relaxation directly, not Hall.

## What we've actually shown

> **Partial Theorem.** For every loopless matroid M and every bigrade (m, d) with `2m+d ≤ n`, `m+d ≤ rank(M)`, `d ≥ m+1`, the operator `∂*: X_m(M) → X_{m+1}(M)` is injective.

The proof: Hall's marriage condition holds in this range by the min-fwd / max-bwd argument. A perfect matching gives an injection X_m → X_{m+1}, hence column-injectivity.

**This covers a substantial portion of the d≥2 hypothesis** — specifically, the "interior" cases away from the boundary.

## What remains open

The **boundary bigrade** `(m, d) = ((n-2)/2, 2)` for even n (and similar near-boundary cases) is not covered by the naive Hall argument. For these:

1. The PAVING case is handled by PAPER §4 (KW relaxation).
2. The non-paving case at the boundary is the GENUINELY OPEN part.

Concrete remaining task: prove `∂*` injective at the d=2 boundary for non-paving matroids.

## Connection to geometric framework

The geometric framework (notes/27-32) handles the boundary case in PRINCIPLE via Hard Lefschetz on the wonderful compactification Y_M. The structural argument here (Hall) gives an INDEPENDENT proof for the d ≥ m+1 range, validating that part of the conjecture combinatorially.

For the boundary case d=2: both approaches stall at the same point:
- Hall: needs better bounds on bwd for specific matroid types.
- Geometric: needs the X-Identification (= R(M)|_X is the Lefschetz-stable sub-piece of H*(Y_M)).

Both routes converge on the same combinatorial difficulty: understanding the bipartite incidence structure of X_m vs X_{m+1} at d=2.

## Status

- **Proven (this note):** Project conjecture for `d ≥ m+1` bigrades via Hall.
- **Proven (PAPER):** Project conjecture for paving matroids (all bigrades).
- **Proven (notes/28):** Geometric proof for Triangle (= U(2,3)).
- **Open:** Project conjecture for non-paving matroids at d=2 boundary bigrades.

The session's net mathematical progress: a Hall-theorem-based proof of the project's conjecture for a substantial sub-range of the bigrade hypothesis (d ≥ m+1). This is complementary to the geometric framework — both reduce the open problem to the same d=2 boundary cases.

## Next steps if continuing

1. Push harder on Hall at the d=2 boundary: find matroid-specific upper bounds on `bwd(A')` for matroids in the hypothesis.
2. Combine Hall (for d ≥ m+1) with geometric framework (which handles Triangle / paving) to nail down the boundary case.
3. Investigate if the d=2 boundary is **provably** the only remaining obstacle, or if there are deeper structural issues.
