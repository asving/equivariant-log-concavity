# Note 26 — Hunt for hyperkähler twistor matches for R(M)|_X (2026-05-24)

## TL;DR

**The most natural hyperkähler / twistor cohomology candidates do not realize R(M)|_X.** Total dimensions match by coincidence for 3 of 11 small representable matroids (U(2,3), U(3,5), U(3,6)), but the **graded sl(2)-module structures are incompatible** even in those cases. For 8 of 11 matroids, even total dimensions disagree.

This rules out the simplest geometric story but does NOT rule out more exotic realizations. The negative finding is structurally informative: R(M)|_X has a Lefschetz decomposition with **many thin strings** (small irrep dimensions, high multiplicity), unlike standard hyperkähler twistor cohomology, which has **fewer wide strings**.

## Setup

For a representable matroid M of rank r on n elements:
- **Hausel-Sturmfels** (arXiv:math/0203096): the toric hyperkähler X^HK_M has complex dim 2r and `H*(X^HK_M; ℚ) = ℚ[IN(M)]/Θ`, with graded dim = **h-vector** of IN(M).
- **Twistor space** Z(X^HK) = X^HK × S² (set-theoretic) with twisted complex structure, complex dim 2r+1. Cohomology by Leray (toric hyperkähler case, Leray collapses): `H*(Z) ≅ H*(S²) ⊗ H*(X^HK)`, total dim = 2 × |h-vector|.

Candidates checked:
- (a) `R(M)|_X = H*(X^HK_M)`: total dim |X| = |h-vec|.
- (b) `R(M)|_X = H*(Z(X^HK_M))`: total dim |X| = 2 |h-vec|.
- (c) `R(M)|_X = H*(X^HK_M × X^HK_M)`: total dim |X| = |h-vec|².
- (d) Künneth `H*(X^HK)^⊗2` graded match.

## Empirical results (`computations/test_twistor_matching.py`)

| Matroid | X-vector total | h-vector total | Best match? |
|---|---|---|---|
| **U(2,3)** "Triangle" | 6 | 3 | (b) twistor: 2·3 = 6 ✓ |
| U(3,4) | 14 | 4 | None |
| **U(3,5)** | 20 | 10 | (b) twistor: 2·10 = 20 ✓ |
| **U(3,6)** | 20 | 20 | (a) X^HK: 20 = 20 ✓ |
| U(4,5) | 30 | 5 | None |
| U(4,6) | 50 | 15 | None |
| U(5,8) | 182 | 56 | None |
| M(K_4) | 12 | 16 | None |
| U(2,3) ⊕ U(2,2) | 24 | 3 | None |
| U(2,3) ⊕ U(3,3) | 48 | 3 | None |
| M(K_4) ⊕ U(3,3) | 96 | 16 | None |

**3 out of 11 have a total-dim match.**

## Why even the matches fail at the structural level

For U(2,3): both R(M)|_X and H*(twistor Z) have dim 6, but the **sl(2)-module decompositions** are different:

| Object | sl(2)-strings |
|---|---|
| R(U(2,3))\|_X | 3 strings of length 2 (= 3 copies of V₁) |
| H*(twistor Z) | 1 string of length 4 + 1 of length 2 (= V₃ + V₁) |

Total dim 6 in both cases (3·2 vs 4+2), but the irreducible decompositions differ. As sl(2)-modules these are NOT isomorphic.

Similarly for U(3,5): R(M)|_X has 10 strings of length 2 (= 10·V₁), while H*(twistor) has a multi-string decomposition coming from (1+t²)(1+2t²+3t⁴+4t⁶) — totally different irrep multiplicities.

## What the negative result tells us

The R(M)|_X Lefschetz structure has a very specific signature: **primitives P_k = X_k − X_{k-1}**, all concentrated at the "bottom" of the X-support window, generating short strings. Standard hyperkähler / twistor cohomology has primitives **at multiple grades** (one per h-vector consecutive difference), generating strings of varying lengths.

For R(M)|_X to be cohomology of a smooth manifold (Kähler or otherwise), that manifold's Lefschetz decomposition must match: many primitives at one grade, generating many short strings. This is the signature of a manifold whose cohomology is concentrated in two consecutive degrees with the same dim (= "very degenerate" Hodge structure).

The negative eigenvalues (from notes/25) further confirm: the Lefschetz operator on R(M)|_X is **non-Kähler**. Any geometric realization must use:
- An indefinite Hodge structure (pseudo-Kähler), OR
- A non-Kähler complex manifold with Lefschetz property (Kodaira-Thurston-type), OR
- A purely combinatorial Lefschetz structure with no geometric counterpart (BHMPW-style).

The Hausel-Sturmfels toric hyperkähler twistor is too "structured" (its Lefschetz decomposition is determined by the h-vector consecutive-differences pattern). R(M)|_X is too "degenerate" (one primitive grade only) to match.

## Where to look instead

1. **Modified hyperkähler quotients:** non-toric, or with different moment map level, might give different cohomology with right primitive structure.
2. **Subvarieties of X^HK or Z:** restricting to a smaller piece might isolate the X-restriction's structure.
3. **Cohomology with twisted coefficients:** local systems on X^HK or Z with combinatorial structure.
4. **Direct combinatorial Hodge theory (BHMPW-style):** the genuine path. The combinatorial Lefschetz with negative-eigenvalue spectrum is the new structural content; develop it without geometric scaffolding.

## Bottom line

The naive twistor matching doesn't work. R(M)|_X has its own characteristic Lefschetz signature — short strings with many primitives at a single bottom grade and non-Kähler spectrum — that no off-the-shelf hyperkähler construction produces. The honest research direction is combinatorial Hodge theory on this specific structure, not the search for a pre-existing geometric realization.

## Files

- `computations/test_twistor_matching.py` — Hilbert-series matching test.
- `computations/test_x_factorization.py` — eigenvalue and direct-sum factorization analysis.
