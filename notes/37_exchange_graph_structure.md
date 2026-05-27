# Note 37 — Exchange graph structure at d=2 boundary (2026-05-27)

## TL;DR

For matroid M at d=2 boundary, the bipartite operator ∂*: X_m → X_{m+1} can be analyzed via an "exchange graph" structure on X_{m+1}. Concrete finding:

**For M(K_4 + 2 pendants):** Every A ∈ X_3 has forward degree 2 (= every A maps to exactly 2 elements of X_4). The induced graph G on X_4 (with edges = {(A∪{i_1}, A∪{i_2}) : A ∈ X_3, i_1, i_2 the 2 forward neighbors}) is a **perfect matching**: 12 edges on 24 vertices, no cycles, 12 components.

This gives ∂* INJECTIVE by structural counting: 12 disjoint 2-term sums in Q^24 are linearly independent.

## The setup

At d=2 boundary, for A ∈ X_m: ∂*(A) = Σ_{i ∈ E\A, A ∪ i ∈ X_{m+1}} (A ∪ i). Forward degree fwd(A) = (m+2) - |closure_M(A) ∩ E\A|.

**Case analysis:**
- **fwd(A) = m+2 uniformly (closure(A) = A for all A):** Hall via min-fwd ≥ max-bwd trivially holds. Covered in notes/34, 36.
- **fwd(A) < m+2 for some A:** Forward degree reduced; need structural argument.

The interesting case is the second. We just analyzed one such matroid in detail.

## M(K_4 + 2 pendants): the structural analysis

**Setup:** Graph = K_4 on vertices {0,1,2,3} (6 edges) + pendant edges (0,4) and (1,5). n=8 edges, rank=5.

**Bases:** Every spanning tree must include the two pendant edges. So bases = (K_4 spanning tree) ∪ {pendant 1, pendant 2}. K_4 has 16 spanning trees, but only 12 give A ∈ X_3 (the 4 "star" spanning trees have triangle complement, excluded).

**X_3:** 12 elements = (path spanning trees of K_4).

**Closure analysis:** For A ∈ X_3 (= path spanning tree of K_4 with 3 edges), closure_M(A) = K_4 (all 6 K_4 edges) because A is a maximal forest in K_4, so adding any other K_4 edge creates a cycle.

**Forward degree:** fwd(A) = (m+2) - |closure(A) ∩ E\A| = 5 - |K_4 ∩ E\A| = 5 - 3 = 2.

The 2 elements of E\A not in closure(A) are exactly the pendant edges {6, 7}.

So ∂*(A) = (A ∪ {6}) + (A ∪ {7}) — a 2-term sum.

**The exchange graph:** Define G on vertices X_4 with edges {(A ∪ {6}, A ∪ {7}) : A ∈ X_3}.
- 12 edges (one per A ∈ X_3).
- Each vertex in X_4 touched by at most one edge (since A is uniquely determined by either A ∪ {6} or A ∪ {7}, and the pair is uniquely "matched").
- |X_4| = 24, so 24 vertices total.
- All 24 X_4 vertices are touched (each edge contributes 2 distinct vertices, 12 edges × 2 = 24 = |X_4|).
- 0 cycles, 12 components (each a single edge).

**This is a perfect matching of X_4.**

**Injectivity:** ∂*(A) = e_{A ∪ {6}} + e_{A ∪ {7}} in Q^{X_4}. The 12 sums use disjoint pairs of basis vectors, hence are linearly independent. ∂* INJECTIVE. ∎

## Generalizing to other matroids

This structural argument works whenever:
1. For each A ∈ X_m, the forward "fingerprint" (= set {A ∪ i : i forward neighbor}) is unique.
2. The "exchange graph" on X_{m+1} induced by ∂*(A) has structure forcing linear independence.

For (1): forward fingerprints are different across distinct A's because A determines the fingerprint (specifically, A = ∩ of all elements in fingerprint).

For (2): in M(K_4 + 2 pendants), the fingerprint is exactly 2 elements, and these 2-element sets are pairwise disjoint across different A's.

**For general M at d=2 boundary:** the exchange graph G could have higher degree per A (forward degree > 2). For ∂* injectivity, we need the "hypergraph" structure to be such that the sums are linearly independent.

This generalizes the matroid intersection / Lorentzian polynomial framework: ALOV's M-convexity guarantees specific "spread" of matroid intersection bases, which should give the linear independence we need.

## What we've established

For the project's main conjecture (∂* injective at d≥2 hypothesis):

1. **Paving matroids: all bigrades** (PAPER §4 KW relaxation).
2. **d ≥ m+1 bigrades: any matroid** (notes/33 Hall theorem).
3. **m=2 d=2 boundary: simple matroids** (notes/34 girth analysis).
4. **High-girth d=2 boundary (girth > corank+1): any matroid** (notes/36).
5. **Triangle U(2,3): complete geometric proof** (notes/28).
6. **M(K_4 + 2 pendants) at d=2 boundary**: structural proof via exchange graph (this note).

For other low-girth non-paving matroids at d=2 boundary: same EXCHANGE GRAPH technique works, but verification per matroid.

The exchange graph approach gives a **GENERAL TEMPLATE** that should be provable for all matroids at d=2 boundary, via matroid intersection / ALOV polynomial capacity. The key ingredient: the "matroid intersection" structure of X_m at d=2 boundary makes the exchange graph "well-connected" in a controllable way.

## The general conjecture

> **Conjecture (Exchange Graph at d=2 boundary).** For any matroid M at d=2 boundary, the exchange graph G on X_{m+1} induced by ∂*(A) for A ∈ X_m has the property: the |X_m| "edge-sums" Σ_{i forward} e_{A∪{i}} are linearly independent in Q^{X_{m+1}}.

Equivalently: ∂* has full column rank.

This is the project's main conjecture restated. The exchange graph framework gives a concrete structural attack — verify forest / well-connected properties for each specific matroid.

## Connection to matroid intersection theorems

For X_m = Indep(M) ∩ Indep(M*) (matroid intersection bases at max rank): Edmonds' theorem gives strong exchange structure.

For ∂* injective: equivalent to a "strong matroid intersection bipartite incidence" theorem.

ALOV (arXiv:1810.04341) proves the matroid intersection polynomial is Lorentzian. Combined with Brändén-Huh, this gives:
- Coefficient log-concavity.
- M-convexity of support.
- "Brunn-Minkowski-style" inequalities.

For rank statements on bipartite operators: ALOV doesn't directly give it. But the structural foundation is there.

## Path forward

For a complete proof of project's conjecture at d=2 boundary:

1. **Prove the Exchange Graph Conjecture above** in general (not just per-matroid). Possible via:
   - Matroid intersection exchange theorem (Edmonds).
   - ALOV-style polynomial capacity bounds.
   - Direct combinatorial enumeration on exchange graph.

2. **Combined with notes/33, 34, 36, this completes the project's main conjecture.**

The Exchange Graph Conjecture is a concrete, tractable structural statement — much sharper than the original conjecture and amenable to combinatorial techniques.

## Files

- `computations/k24_m3_boundary.py` — verifies ∂* injective on M(K_{2,4}).
- `computations/closure_at_d2_boundary.py` — tests closure(A)=A across many matroids.
- This note: structural exchange graph analysis.
