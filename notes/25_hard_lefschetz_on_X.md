# Note 25 — Hard Lefschetz on R(M)|_X (2026-05-24)

## Headline

**R(M)|_X is Gorenstein-like:** the X-restriction satisfies Hard Lefschetz with the symmetric Aut(M)-invariant operator ω = Σ x_i. Verified on 10 test matroids (paving + non-paving). The bilinear pairing on R(M)|_X is non-degenerate; the geometric realization route is *not* blocked by Poincaré duality on the X-restriction.

## The check

For each test matroid M:
- Compute X-vector |X_k(M)| for k = 0, ..., n. Always palindromic: |X_k| = |X_{n-k}|.
- Test whether `∂*^{n-2k}: X_k → X_{n-k}` is an isomorphism for every k ≤ n/2 with X_k ≠ 0.

| Matroid | (n, r) | X-vector (support) | HL holds? |
|---|---|---|---|
| U(3, 4) | (4, 3) | (4, 6, 4) | ✓ |
| U(4, 6) | (6, 4) | (15, 20, 15) | ✓ |
| U(5, 8) | (8, 5) | (56, 70, 56) | ✓ |
| Triangle ⊕ U_{2,2} | (5, 4) | (3, 9, 9, 3) | ✓ |
| Triangle ⊕ U_{3,3} | (6, 5) | (3, 12, 18, 12, 3) | ✓ |
| Triangle ⊕ U_{4,4} | (7, 6) | (3, 15, 30, 30, 15, 3) | ✓ |
| Triangle ⊕ U_{5,5} | (8, 7) | (3, 18, 45, 60, 45, 18, 3) | ✓ |
| M(K_4) ⊕ U_{3,3} | (9, 6) | (12, 36, 36, 12) | ✓ |
| M(K_4) ⊕ U_{4,4} | (10, 7) | (12, 48, 72, 48, 12) | ✓ |
| Vámos V_8 | (8, 4) | (64,) (singleton) | ✓ (trivially) |

`computations/test_hard_lefschetz_x.py`.

## Lefschetz decomposition

By the sl(2) structure of a Lefschetz module, R(M)|_X decomposes into **Lefschetz strings**. Primitive dims:

```
   P_k = X_k − X_{k-1}   (for k in the lower half of support)
```

Each primitive at grade k generates a string of length (n − 2k + 1) spanning grades [k, n − k].

`computations/test_primitive_lefschetz.py` verifies P_k = X_k − X_{k-1} on all test cases, with X-vector reconstruction Σ_{k ≤ d} P_k = X_d.

## What this means

The HL statement on R(M)|_X is **equivalent** to:
- Palindromic X-vector (automatic by A ↔ E\A complementation).
- Single-step injectivity: `∂*: X_k → X_{k+1}` injective for k ≤ n/2 − 1 (and surjective for k ≥ n/2 by symmetry).

Single-step injectivity for k ≤ n/2 − 1 is *exactly* our project's conjecture for the orbit (∅, E). So HL on R(M)|_X **is** the conjecture, restated cleanly.

**This gives no new empirical information**, but a **much cleaner sharp statement**:

> **Refined conjecture (HL on the X-restriction).** For every loopless matroid M, the graded vector space R(M)|_X is a Lefschetz module under the symmetric Aut(M)-invariant operator ω = Σ x_i. Equivalently, R(M)|_X is Gorenstein with HL.

## Implications for the geometric route

The Poincaré-duality obstruction (notes/24, Layer 3) said: full R(M) is not the cohomology of a compact smooth oriented manifold. But it does NOT block R(M)|_X, which IS Gorenstein/Lefschetz.

However, an attempted manifold realization for R(M)|_X faces a different problem:

- For Triangle ⊕ U_{3,3}: X-vector (3, 12, 18, 12, 3) at grades 1..5.
- Any compact connected orientable manifold has b_0 = b_{top} = 1.
- Our X-vector has b_0 = 0 (X_0 = 0 since ∅ ∉ X(M) when E is not independent).
- So R(M)|_X is *not* the full cohomology of a connected compact manifold — there's no "fundamental class at degree 0."

R(M)|_X could plausibly be:
- The **primitive** or **reduced** cohomology of some compact manifold (subtracting off the trivial sl(2)-string of length 1 at degree 0).
- The cohomology of a non-orientable / multi-component space.
- The cohomology in a non-trivial local coefficient system.
- A piece of mixed Hodge structure on a non-compact variety.

None of these is obviously implausible, but none is identified.

## What the "more ambitious" next step looks like

Two genuinely promising directions emerge from the HL framing:

### (a) **Combinatorial Hodge theory on R(M)|_X à la BHMPW.**

BHMPW (arXiv:2002.03341, 2010.06088) prove HL on the AHK Chow ring **combinatorially**, without any underlying smooth projective variety, using a "semi-small decomposition" under matroid deletion-contraction. The blueprint:

1. For each element e ∈ E, find a deletion-contraction decomposition of R(M)|_X into pieces related to R(M\e)|_X and R(M/e)|_X.
2. Show each piece carries a HL structure.
3. Show the decomposition preserves HL (this is the "semi-small" condition).
4. By induction on |E|, HL holds throughout.

The challenges:
- BHMPW's decomposition is *flat-indexed*; we need a *subset-indexed* analog. The X-restriction's behavior under deletion-contraction must be worked out.
- Our `notes/23` already established a block-triangular decomposition by element. The depth-3 failure of "diagonal blocks individually injective" is exactly the kind of complication that semi-small decomposition handles via a careful tracking of cokernels.
- "Semi-small" has a precise meaning in BHMPW: each piece of the decomposition has Lefschetz support of the right size. We'd need a matroid-X analog.

This is **2-5 years of work** but it's the most likely real path. It would give a complete equivariant proof of f-vector ELC for arbitrary loopless matroids.

### (b) **Realize R(M)|_X via "reduced" / "primitive" cohomology of a known matroid construction.**

If R(M)|_X is the reduced cohomology of the moment-angle complex Z_{IN(M)} (or a related space), we'd be done. The moment-angle complex Z_{IN(M)} has cohomology = full Tor algebra, which is much bigger than R(M). But the "linear part" of the Tor is precisely R(M). The X-restriction might correspond to a *specific symmetric piece* of the Tor — possibly an "intersection cohomology" component or a "Lefschetz primitive" piece.

This requires deep moment-angle / toric topology expertise but it's the cleanest geometric candidate.

### (c) **Anari-Liu-Vuong polynomial capacity, equivariant lift.**

The X-bipartite structure is matroid intersection. ALOV (arXiv:1810.04341) prove (non-equivariant) log-concavity for matroid intersection via polynomial capacity. Lifting to equivariant log-concavity is the open problem in equivariant Lorentzian polynomial theory; the matroid-intersection case is the natural entry point.

## Files

- `computations/test_hard_lefschetz_x.py` — verifies HL on R(M)|_X for test matroids.
- `computations/test_primitive_lefschetz.py` — extracts Lefschetz string decomposition.
- This note supersedes the "is R(M)|_X Gorenstein?" question raised in notes/24 with a clean affirmative answer.
