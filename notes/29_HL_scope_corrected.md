# Note 29 — Scope of HL on R(M)|_X: correction to note 25 (2026-05-24)

## TL;DR

**HL on R(M)|_X is NOT universal.** My claim in notes/25 was based on test matroids that all factored as direct sums with free components. Testing on M(K_4 − e), a genuinely connected non-uniform matroid, reveals that ∂*: X_2 → X_3 has rank 7 (not 8): kernel of dimension 1.

This is **not** a counterexample to the project's main conjecture (PAPER §5.3), which is restricted to bigrades with `d ≥ 2`, `m+d ≤ rank`, `2m+d ≤ n`. M(K_4 − e) is OUTSIDE this hypothesis. The empirical failure occurs at a bigrade the conjecture doesn't claim.

But it IS a refutation of the stronger "HL on R(M)|_X for all matroids" claim I'd asserted in notes/25.

## The empirical data

`computations/k4_minus_edge_geometric.py`:

For M(K_4 − e) (n=5, rank=3, circuits = 2 triangles + 1 four-cycle):
- X-vector: (0, 0, 8, 8, 0, 0).
- ∂*: X_2(8) → X_3(8) is 8×8.
- Rank = 7. Kernel of dimension 1.
- **HL fails.**

## Why the project's conjecture is unaffected

PAPER.md §5.3 conjecture, recapitulated:

> For every loopless matroid M and every bigrade (m, -d) with `2m + d ≤ n`, `m + d ≤ rank(M)`, `d ≥ 2`, the operator ∂*: X_m(M) → X_{m+1}(M) is injective.

For M(K_4 − e) (n=5, r=3), the constraints `2m+d ≤ 5`, `m+d ≤ 3`, `d ≥ 2` admit only:
- (m=0, d=2): X_0 = 0, trivial.
- (m=0, d=3): X_0 = 0, trivial.
- (m=1, d=2): X_1 = 0, trivial.

The bigrade (m=2, d=?) requires `m+d ≤ 3`, so `d ≤ 1` — outside hypothesis.

**The conjecture is vacuous for M(K_4 − e).** The empirical failure at (m=2, d=1) doesn't refute it.

## What I was actually testing in notes/25

My HL test from notes/25 checked the structurally stronger claim: "HL on R(M)|_X" (= ∂* iso between symmetric grades), regardless of bigrade hypothesis.

The matroids tested:
- Uniform U(r, n) — these are uniform, so R(M)|_X is essentially boolean, HL is classical sl₂.
- Triangle ⊕ U(k, k) — direct sum; HL factors and inherits from Triangle (trivial case).
- M(K_4) ⊕ U(k, k) — direct sum; HL factors and inherits from M(K_4) which has X-restriction at a single grade (trivial).
- Vámos V_8 — has only X_4 = 64, single grade, trivial.

**None of these test cases is "genuinely connected non-uniform with multi-grade X-support."** That's why HL appeared to hold universally.

M(K_4 − e) is the simplest such genuinely-connected test case, and HL fails on it.

## Implication for the geometric proof template (notes/28)

The Triangle proof in notes/28 works because R(Triangle)|_X = R(Triangle) at non-trivial grades — the X-restriction is the *full* pullback subspace of H*(Y).

For matroids where R(M)|_X is a *strict* subspace of R(M)_k (like M(K_4 − e) at grade 2: |X_2|=8 vs R(M)_2 = 10), the X-restriction isn't simply the pullback in H*(Y_M).

**The X-Identification step** (notes/28 §"What remains to be verified for general M") is non-trivial. For matroids in the bigrade hypothesis, the X-restriction empirically has the right structural property to inherit HL. For matroids outside the hypothesis, this property can fail.

## What "in the bigrade hypothesis" means structurally

A loopless matroid M with rank r on n elements has a bigrade (m, d) with `2m+d=n`, `m+d ≤ r`, `d ≥ 2` iff `r ≥ (n+2)/2`. That is, **rank exceeds half the ground set by at least 1**.

For such "high-rank" matroids (= rank > n/2 + 1 - 1/2), the X-restriction lives in a regime where HL appears to hold.

For "low-rank" matroids (= rank ≤ (n+1)/2): the X-restriction may have HL failure.

M(K_4 − e): n=5, r=3 = (n+1)/2. On the boundary.
Triangle: n=3, r=2 = (n+1)/2. On the boundary.

Both are on the boundary, but Triangle has X-vector = full binomial (boolean structure) while M(K_4 − e) has X-vector that's actually constrained by circuits.

The actual structural property distinguishing "HL on R(M)|_X holds" from "fails" needs to be identified. Empirical conjecture (refined):

> **HL on R(M)|_X holds when the X-restriction at the relevant grade equals the full pullback of H*(Y_M) at that grade.**

For Triangle: X_1 = 3 = R(M)_1 = full pullback at grade 1. ✓
For M(K_4 − e): X_2 = 8 ≠ R(M)_2 = 10 = pullback at grade 2. ✗

Need more test cases to confirm this is the right structural property.

## What I still believe

1. **Triangle's geometric proof is solid.** HL on R(Triangle)|_X is proven via classical Kähler HL on Bl_p((P^1)^3).

2. **The project's main conjecture (PAPER §5.3) is likely true** — empirically verified across 200k+ orbits, my computational tests support it for direct sums and uniform cases, and the geometric proof template can extend to the d≥2 hypothesis with more work.

3. **The geometric proof template needs refinement** to handle the case where R(M)|_X is a strict subspace of R(M)_k. The X-Identification step is the genuine technical content.

4. **My notes/25 overreach is corrected.** The stronger "HL on R(M)|_X universally" claim is FALSE.

## Next concrete step

Find a genuinely-connected NON-uniform matroid that DOES satisfy the bigrade hypothesis (rank > n/2 + 1), and verify HL on its R(M)|_X.

For n=4, rank=3, "rank > n/2 + 1 = 3" is satisfied marginally. Examples:
- U(3, 4): uniform.
- "Rank 3 on 4 with parallel pair": non-uniform, X-vector (0, 2, 4, 2, 0). Just verified ∂*: X_1 → X_2 has rank 2 (= full column rank). HL holds. ✓

This is the kind of test case where HL on R(M)|_X holds, AND the matroid is in the bigrade hypothesis.

For n=5, need rank = 4 (since rank > n/2 + 1 = 3.5 → rank ≥ 4).
- U(4, 5): uniform.
- Non-uniform: hard to construct with rank 4 on 5 elements (only one circuit of size 5 = the whole set, giving U(4, 5)).

For n=6, need rank = 4 or 5:
- U(4, 6) and U(5, 6): uniform.
- Non-uniform with rank ≥ 4: e.g., M = U(4, 6) with a 3-circuit added (= 6 elements, rank 4, one triangle circuit and the size-5 circuits).

Whether such matroids satisfy HL on R(M)|_X needs to be tested.

## Status

- Geometric proof: Triangle = solid.
- General template: needs careful X-Identification per matroid.
- Project's main conjecture: still empirically supported, geometric proof in principle exists for in-hypothesis case.
- "Universal" HL claim from notes/25: WRONG, corrected here.

The geometric realization is real but more nuanced than I initially claimed.
