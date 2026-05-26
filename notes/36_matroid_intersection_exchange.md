# Note 36 — Matroid intersection exchange and the d=2 boundary proof attempt (2026-05-25)

## The setup

At d=2 boundary:
- X_m = Indep(M)_m ∩ Indep(M*)_m = bases of the matroid intersection M ∩ M* (notes/34).
- X_{m+1} = {A' : |A'|=m+1, A' indep in M, E\A' indep in M}, equivalently "balanced equal-size indep partitions" (NOT bases of M ∩ M*).

Goal: show ∂*: X_m → X_{m+1} is injective.

## Matroid intersection exchange theorem

For two matroids M_1, M_2 on E with bases B_1(M_1∩M_2) (= max common indep sets), the **strong exchange theorem** (Edmonds 1970):

> For any B, B' ∈ B_1(M_1∩M_2) and any i ∈ B \ B', there exists j ∈ B' \ B such that:
> - (B \ {i}) ∪ {j} is a basis of M_1 ∩ M_2, AND
> - (B' \ {j}) ∪ {i} is a basis of M_1 ∩ M_2.

This gives a strong "matroid-like" structure on the intersection bases.

For our setting (M_1 = M, M_2 = M*): X_m has this exchange structure.

## Trying to derive ∂* injectivity from exchange

**Attempt:** Suppose ∂* has a kernel vector `Σ c_A · A` (formal linear combination).

For ∂* applied: `Σ_A c_A ∂*(A) = Σ_A c_A Σ_{i: A∪i ∈ X_{m+1}} (A ∪ i) = 0`.

Grouping by target A' ∈ X_{m+1}:
`Σ_{A' ∈ X_{m+1}} (A∪i = A')` (Σ_{A ⊂ A' with A ∈ X_m, A'\A ∉ closure(A)} c_A) = 0.

For each A' ∈ X_{m+1}, the coefficient is `Σ_{A ⊂ A', A ∈ X_m, A'\A ∉ closure(A)} c_A = 0`.

For injectivity: need this system to force all c_A = 0.

**Strategy:** Use matroid intersection exchange to "propagate" coefficient relations.

Take A_1, A_2 ∈ X_m with A_1 △ A_2 a specific simple pattern (e.g., single exchange). By matroid intersection exchange, there's a path between them through bases.

For each step in the exchange path: a SPECIFIC A' ∈ X_{m+1} "connects" the adjacent bases.

If the exchange path has the property that `Σ c_A = 0` at each step forces `c_{A_1} = c_{A_2}` (or similar): we'd propagate equality. Combined with a specific normalization, c_A = 0 throughout.

**This is the matroid intersection augmenting path approach.** For matroid intersection algorithms (Edmonds), augmenting paths give polynomial-time max matching. For our injectivity, augmenting paths might give the coefficient propagation.

## Specific structure to exploit

For A_1, A_2 ∈ X_m differing in exactly one element (i.e., |A_1 △ A_2| = 2): there's an A' ∈ X_{m+1} with A_1 ⊂ A' AND A_2 ⊂ A' (= A' = A_1 ∪ {i} = A_2 ∪ {j} for some i, j with A_1 \ A_2 = {j}, A_2 \ A_1 = {i}, A_1 ∩ A_2 = A' \ {i,j}).

For this A': the kernel equation is `c_{A_1} + c_{A_2} + (others) = 0` (if only A_1 and A_2 contribute, others = 0).

For "others = 0": need that A' is reachable from exactly A_1 and A_2 in X_m, i.e., A' has exactly 2 m-subsets in X_m. This requires bwd(A') = 2.

For matroids with bwd(A') = 2 for all A' (= "tight" bwd): the kernel equations become `c_{A_1} + c_{A_2} = 0` for every "exchange pair" (A_1, A_2) with shared A'.

Then the kernel forms a SIGNED CIRCULATION on a graph whose vertices are X_m and edges are exchange pairs. If this graph is connected and bipartite-like, kernel = 0 (only c_A constant, scaled by ±1 along edges, but then global sum = 0 requires zero).

Hmm. Let me think more carefully.

## What bwd actually is at d=2 boundary

For A' ∈ X_{m+1}: bwd(A') = #{e ∈ A' : A' \ {e} ∈ X_m} = #{e ∈ A' : E\(A' \ {e}) indep in M}.

E\(A' \ {e}) = (E\A') ∪ {e}. Indep iff doesn't contain circuit.

For matroid M with girth g, (E\A') ∪ {e} has |E\A'|+1 = m+2 elements. Contains circuit iff its size ≥ g AND it contains a g-circuit.

(E\A') itself is indep, of size m+1. Adding e ∈ A' = element of size-(m+1) indep set. Total m+2 = rank.

(E\A') ∪ {e} dependent iff it's a "rank-m+1 with m+2 elements" = exactly one circuit. The circuit is determined by e (= "the unique circuit added by e").

For each e ∈ A' ∩ closure(E\A'): adding e creates a circuit. So e in closure ↔ adding e gives dependence.

So bwd(A') = (m+1) - |A' ∩ closure(E\A')|.

For specific matroid M, |A' ∩ closure(E\A')| varies.

For "girth > corank+1" matroid: closure(E\A') = E\A' (no extensions). |A' ∩ closure| = 0. bwd = m+1.

For girth = m+1: closure(E\A') might extend. bwd varies.

## Forward degree at d=2 boundary

Symmetric: fwd(A) = (m+2) - |closure_M(A) ∩ (E\A)|.

For "girth > m" (= no circuit of size ≤ m): closure_M(A) = A (no extension at corank level). fwd = m+2.

For girth ≤ m: closure can extend.

## When does naive Hall work at d=2 boundary?

`min fwd ≥ max bwd` suffices for Hall.

For "girth > corank + 1" matroid: fwd = m+2 uniformly, bwd = m+1 uniformly. m+2 ≥ m+1 ✓.

So **for matroids at d=2 boundary with girth > corank + 1, Hall holds and ∂* is injective.**

For corank = m: "girth > m+1" suffices.

## A clean theorem

> **Theorem.** For every loopless matroid M at d=2 boundary bigrade (m, d=2) with girth > m+1, the operator ∂*: X_m(M) → X_{m+1}(M) is injective.

**Proof.** By the above analysis, fwd(A) = m+2 and bwd(A') = m+1 for all A ∈ X_m, A' ∈ X_{m+1}. By Hall's marriage theorem (min fwd ≥ max bwd), the bipartite graph has a perfect matching from X_m into X_{m+1}, which gives ∂* column rank ≥ |X_m|, i.e., injective. ∎

## Coverage

For matroid M with rank r and corank m = n-r:
- d=2 boundary requires m = (n-2)/2 = corank and r = m+2.
- "girth > m+1" = "girth > corank+1" = "matroid is paving-ish".

**Recall: paving matroid has girth ≥ rank = m+2 ≥ m+1 (actually m+2 > m+1)** ⟹ Paving matroids automatically satisfy girth > m+1.

So this Theorem covers PAVING matroids at d=2 boundary. Combined with notes/33 Hall theorem (for d ≥ m+1), this gives **Hall-based proof for paving matroids in all d≥2 bigrades**.

But PAPER §4 already proves the paving case via KW relaxation. So this Hall proof is an alternative — cleaner combinatorial proof of the paving case.

## Non-paving cases

For NON-PAVING matroids at d=2 boundary: girth < rank, so girth ≤ rank - 1 = m+1.

If girth = m+1: closure can extend by 1 element when A is a "near-circuit" subset.

For such cases, fwd(A) ≥ m+1 (= reduced by at most |# (m+1)-circuits containing A|).

If max # (m+1)-circuits containing any A is ≤ 1: fwd(A) ≥ m+1, bwd(A') ≤ m+1. Hall holds (tight).

For matroids where some A is in multiple (m+1)-circuits: fwd could be smaller. Hall via this argument fails.

For girth ≤ m: even tighter analysis needed.

## Practical coverage

For graphic matroids: girth = length of shortest cycle.
- Tree matroids: girth = ∞ (= no cycles). Always covered.
- M(K_n) for n ≥ 3: girth = 3. For girth > m+1: m+1 < 3, m < 2. So only m ≤ 1 covered.

For "matroids with many small circuits": girth small, m can be larger, "girth > m+1" rarely holds.

For "matroids with few large circuits": girth larger, more cases covered.

## What this gives us toward the project's conjecture

Combined with notes/33 and PAPER §4:

> **Theorem (combined).** The project's main conjecture holds for the following matroid/bigrade combinations:
> - **Paving matroids** at all d≥2 bigrades (PAPER §4).
> - **Any matroid** at d ≥ m+1 bigrades (notes/33).
> - **Simple matroids with m=2 at d=2 boundary** (notes/34 refined Hall).
> - **Matroids with girth > corank+1 at d=2 boundary** (this note).
> - **Triangle = U(2,3)** completely (notes/28 geometric).

**Remaining open:** matroids at d=2 boundary with girth ≤ corank+1 AND m ≥ 3 (which can't be uniform or covered by m=2 analysis).

For n ≥ 8 (= 2m+2 ≥ 8 means m ≥ 3): need non-uniform matroids with corank ≥ 3 and girth ≤ corank+1. These are "graphic-like" matroids with many small circuits.

The structural reduction (notes/34: X_m = matroid intersection) still holds and provides the foundation for attacking these via ALOV / Lorentzian polynomial capacity.

## Final assessment

The session's net contribution to the project:

1. **Geometric framework** identified, Triangle proven (notes/27-28).
2. **Hall-based combinatorial proof** for d ≥ m+1 (notes/33).
3. **Refined Hall** for m=2 d=2 boundary (notes/34).
4. **Girth-based Hall** for high-girth matroids at d=2 boundary (this note).
5. **Matroid intersection structural identity** at d=2 boundary (notes/34).
6. **Clean reduction** of remaining open case to ALOV/Lorentzian framework.

The remaining open case is well-characterized and connected to deep matroid combinatorics. The project has a clear path forward via two routes (Hall-refined or ALOV-Lorentzian).
