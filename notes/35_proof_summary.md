# Note 35 — Proof status summary at end of session 2026-05-25

## What's proven vs open in the project's main conjecture

> **Project's main conjecture (PAPER §5.3):** For every loopless matroid M and every bigrade (m, d) with `2m+d ≤ n`, `m+d ≤ rank(M)`, `d ≥ 2`, the operator ∂*: X_m(M) → X_{m+1}(M) is injective.

### Proven cases

| Range | Method | Notes |
|---|---|---|
| **Paving matroids** (all bigrades) | Stressed-hyperplane relaxation | PAPER §4 (KNPV paradigm) |
| **d ≥ m+1** (any matroid) | Hall's marriage theorem | notes/33 |
| **d=2 boundary, m ≤ 1** (any matroid) | Naive Hall covers | notes/33 |
| **d=2 boundary, m = 2** (simple matroids, n=6, rank=4) | Refined Hall via girth | notes/34 |
| **Triangle = U(2,3)** (all bigrades, fully geometric) | Kähler HL on Bl_p((P^1)^3) | notes/28 |

### Open range

**d=2 boundary at m ≥ 3 for connected non-uniform non-paving matroids.**

This is the genuinely open remaining case. Empirically verified across many matroids; structurally well-understood (notes/34: X_m = Indep(M) ∩ Indep(M*) = matroid intersection).

## The matroid intersection key

At d=2 boundary, X_m has a clean structural identity:

> **X_m(M) = Indep(M)_m ∩ Indep(M*)_m**

This identifies X_m with matroid intersection (= common indep sets of M and its dual). Verified computationally for all 6 test matroids (notes/34, computations/d2_boundary_matroid_intersection.py).

This connects the project's conjecture at d=2 boundary to **Anari-Liu-Vuong's matroid intersection log-concavity** (arXiv:1810.04341). ALOV proved the matroid intersection generating polynomial is Lorentzian.

The remaining technical step: translate ALOV's Lorentzian structure to injectivity of the bipartite operator ∂*: X_m → X_{m+1}. This is the open research direction.

## The geometric framework

Independently of the combinatorial proof, the geometric framework gives the Triangle case completely and provides a template:

> R(M) = H*(U_M) where U_M = (P^1)^n minus matroid coordinate subspace arrangement (Goresky-MacPherson 1988).
>
> The Lefschetz operator L = Σ x_i ⊗ x_i is the Aut(M)-invariant Kähler class of (P^1)^n descended through the matroid ideal.
>
> For Triangle = U(2,3): HL on R(M)|_X follows from classical Kähler Hard Lefschetz on the wonderful compactification Y = Bl_p((P^1)^3) via block-triangular inheritance.
>
> For general M in d≥2 hypothesis: the "X-Identification" — identifying R(M)|_X as the appropriate Lefschetz-stable sub-piece of H*(Y_M) — is research-level work (BHMPW-style semi-small decomposition adapted to subspace arrangements).

## Session-level summary

Starting from the paving theorem (PAPER), this session has:

1. **Identified the geometric setting**: R(M) = H*(matroid arrangement complement) (notes/27).
2. **Complete proof for Triangle** via classical Kähler HL (notes/28).
3. **Corrected scope** of geometric framework to match the d≥2 hypothesis exactly (notes/29-30).
4. **Hall theorem proof** for d ≥ m+1 range (notes/33).
5. **Structural identity** X_m = matroid intersection at d=2 boundary (notes/34).
6. **Refined Hall** for m=2 d=2 boundary via girth (notes/34).

**Net effect:** The project's main conjecture is proven for a substantial fraction of cases:
- All paving matroids.
- All matroids at d ≥ m+1 bigrades.
- All simple matroids at the (n=6, rank=4) d=2 boundary.
- Triangle completely.

Remaining open: d=2 boundary at m ≥ 3 for non-paving non-uniform matroids. Structurally reduced to matroid intersection / Lorentzian polynomial capacity. Concrete research direction.

## Path to completing the proof

**Option 1: ALOV / Lorentzian polynomial route.** Use the matroid intersection identity (notes/34) and adapt ALOV's polynomial capacity methods to prove injectivity of the bipartite operator at d=2 boundary. Technical bridge: translate "Lorentzian = log-concave coefficients" to "bipartite operator has full column rank".

**Option 2: Geometric / Hodge route.** Develop matroid semi-small decomposition for the wonderful compactification of subspace arrangements (notes/27-30). Identify R(M)|_X as a specific Lefschetz-stable sub-piece. Use classical Kähler HL to deduce injectivity.

**Option 3: Refined Hall.** Extend the girth-based Hall argument from m=2 (notes/34) to m ≥ 3 via tighter matroid-specific bounds on forward/back degrees.

Each option has merit. Combined, they give a thorough attack on the remaining open case.

## Files modified/created this session

- **notes/**: 27, 28, 29, 30, 31, 32, 33, 34, 35 (this file).
- **computations/**: triangle_blowup_HL.py, verify_RM_geometric.py, hexagon_chord_test.py, k4_minus_edge_geometric.py, test_hard_lefschetz_x.py, d2_boundary_nonpaving.py, d2_boundary_connected.py, d2_boundary_matroid_intersection.py, wonderful_compactification_HL.py, fvector_monotonicity_check.py, and supporting exploration scripts.
- **PAPER.md/tex/pdf**: unchanged (the original paving theorem).
- **README.md, HANDOFF.md**: updated to reflect current state.

The repo is at https://github.com/asving/equivariant-log-concavity at commit e97a153 (or later if committed after this note).
