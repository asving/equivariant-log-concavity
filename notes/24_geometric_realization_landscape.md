# Note 24 — Geometric realization of R(M): landscape & decisive obstruction (2026-05-23)

## The headline finding

**The "obvious" geometric program is provably impossible.**

For any non-uniform-or-rank-1 matroid M, the independence complex IN(M) is **not a simplicial sphere**. Therefore R(M) (the squares-zero exterior face ring of IN(M)) **lacks Poincaré duality**. Any smooth compact orientable manifold Y_M (in particular any smooth projective variety) has H*(Y_M) Poincaré-dual to itself. So:

> **No smooth projective variety Y_M can have H*(Y_M) ≅ R(M) for general M.**

This is the cleanest negative observation in the geometric direction. It rules out the naive "find a Y_M and apply Hard Lefschetz" program entirely. None of the previous notes (21–23) had recorded this obstruction.

## Re-framing: what CAN we still hope for?

R(M) ⊗ R^∨(M) is more symmetric (it's the tensor product of a graded vector space with its dual), but it's also not Poincaré-duality unless R(M) is itself Gorenstein. **The X-restriction is doing real structural work**: empirically it cuts R(M) down to a subspace where the bilinear form `(a, b) ↦ a ⋅ b` IS symmetric and non-degenerate. So the modified geometric dream is:

> Realize **R(M)|_X** (the X-restricted bigrading, on which we conjecture L is injective) as a subspace/subquotient of the cohomology of a smooth projective variety where Σ x_i ⊗ x_i acts as an ample class.

This is unexplored territory. None of the matroid-Hodge-theory papers (AHK / BHMPW / EHL / BEST / Pagaria-Pezzoli / Binder) realize a ring with the f-vector as Hilbert series. **They all realize Whitney / Tutte / characteristic / augmented-Whitney style invariants, indexed by flats, not by independent sets.**

## What actually realizes R(M) geometrically (and is non-compact)

For Δ = IN(M):
- The **complement of the coordinate subspace arrangement** U_Δ ⊂ C^n satisfies H*(U_Δ; k) = R(Δ) (Goresky-MacPherson; De Longueville Math. Z. 1999).
- The **moment-angle complex** Z_Δ deformation-retracts equivariantly onto U_Δ and has H*(Z_Δ) = R(Δ) as a subring of the full Tor algebra (Buchstaber-Panov, arXiv:math/9912199).
- These are smooth but **not compact**. Z_Δ is in general **not Kähler** (Bosio-Meersseman; Panov-Ustinovsky arXiv:1008.4764), so no Kähler ample class exists.

Hodge-theoretic Lefschetz for mixed-Hodge-structure on a non-compact U is subtle and has never been pushed to give an ELC-type statement.

## The only known geometric realization with the right Hilbert series (f-vector)

**Hausel-Sturmfels toric hyperkähler** (arXiv:math/0203096):
- For a **representable** matroid M (linear over Q), they construct a non-compact hyperkähler manifold X^HK_M.
- H*(X^HK_M; Q) = k[IN(M)] / Θ, the Stanley-Reisner ring of IN(M) modulo a generic linear system of parameters.
- Graded dimensions = **f-vector of M**. This matches our R(M) bigrade structure exactly (after the squares-zero quotient — needs verification).
- This is Swartz's "generic-WLP" geometric source (arXiv:math/0210376).
- **Limitations:** representable only; non-compact (so no Kähler Lefschetz a priori, but hyperkähler structures give richer triples); generic Θ — *not* the symmetric Σ x_i; no published Aut(M)-equivariant statement.

This is the **closest existing geometric model to R(M) with the correct Hilbert series**, and it has not been pushed equivariantly.

## Survey of matroid varieties (what they actually realize)

| Construction | Variety | Ring realized | Hilbert series | f-vector? |
|---|---|---|---|---|
| AHK (Chow ring) arXiv:1511.02888 | Bergman toric X_M | A(M) | Whitney 2nd kind | ✗ |
| BHMPW augmented arXiv:2002.03341, 2010.06088 | Augmented X_M | CH(M) | augmented Whitney | ✗ |
| Eur-Huh-Larson stellahedral arXiv:2207.10605 | Stellahedral toric | K(M) valuative | Tutte data | ✗ |
| BEST arXiv:2103.08021 | Permutohedral + bundles | 4-variable Tutte ring | Tutte | ✗ |
| Pagaria-Pezzoli arXiv:2105.04214 | Polymatroid Leray model | building-set Chow | building-set Poincaré | ✗ |
| Binder arXiv:2412.05732 (2024) | Quasi-projective toric | Singular cohomology ring | Möbius-controlled | ✗ |
| Hausel-Sturmfels arXiv:math/0203096 | Toric hyperkähler (open) | k[IN(M)]/Θ | **f-vector ✓** | ✓ (representable, generic Θ, non-compact) |

## Three avenues, ranked

### Avenue 1 — **RULED OUT** by dimension check (2026-05-24).

`computations/test_chow_hilbert_vs_x.py` computes |X_k(M)| against dim A(M)_k (AHK Chow ring) for 12 small matroids. **Result: 11 of 12 fail |X_k| ≤ dim A(M)_k at multiple k.** Examples:

| Matroid | Bigrade violation |
|---|---|
| U(2,4) | k=2: |X_2|=6 but A has no degree 2 |
| U(3,5) | k=2: |X_2|=10 vs dim A_2=6 |
| M(K_4) | k=3: |X_3|=12 but A has no degree 3 |
| Vámos V_8 | k=4: |X_4|=64 but A has no degree 4 |
| Triangle ⊕ U_{3,3} | k=2: |X_2|=12 vs dim A_2=9; k=3,4,5 also fail |
| M(K_4) ⊕ U_{3,3} | k=4: |X_4|=36 vs dim A_4=23; k=5,6 also fail |

**Structural reason:** A(M) has top degree r-1 and is graded by **flat-based / rank** combinatorics. X-vector is supported up to degree n with peak near n/2 and is graded by **subset size**. For n > 2r (= virtually every non-uniform matroid), the X-vector's peak lies entirely outside the support of A(M).

**Generalizes to all flat-indexed varieties.** Augmented Chow CH(M) extends to top degree r (one more), but is still flat-indexed; same scaling argument kills it. Same for Pagaria-Pezzoli (polymatroid Leray model, flag-length-graded), EHL stellahedral, BEST permutohedral, Binder singular. **Every matroid variety in the post-AHK literature is flat-indexed and therefore dimensionally cannot contain R(M)|_X.**

This is a clean conclusive refutation. Avenue 1 is dead at the dimensional level — no embedding R(M)|_X ↪ (any flat-indexed Chow-style ring) can exist.

### Avenue 2 — addresses the wrong question.

**Correction (2026-05-24):** the prior agent report incorrectly claimed H*(X^HK_M) has f-vector dimensions. It does not — the cohomology is k[IN(M)]/Θ for **generic linear Θ**, whose Hilbert function is the **h-vector** of IN(M), not the f-vector (Stanley's standard formula).

So even if symmetric ω is Lefschetz on H*(X^HK_M), this gives h-vector log-concavity, not f-vector log-concavity. The implication "h-vector log-concave ⟹ f-vector log-concave" exists for matroids non-equivariantly (Stanley's chain of inequalities), but the **equivariant lift of this implication is non-trivial** and as far as I can tell has not been done.

**Status:** Avenue 2 is *not* a direct path to our f-vector ELC. It could still be a useful side project, but it answers a related but different question.

### Avenue 3 (research program, 1–3 years): Build a new compactification of U_M = X(IN(M)).

- **Idea:** find a smooth projective Y_M ⊃ U_M whose cohomology recovers R(M)|_X (necessarily not all of R(M) by the Poincaré-duality obstruction). One candidate: closure of U_M inside the Eur-Huh-Larson stellahedral variety as a quotient by boundary divisors.
- **Cost:** very high. Full thesis-scale project unless implicit in existing literature.
- **Risk:** may not exist. The Poincaré-duality obstruction says compactifications must alter cohomology in some way; finding one whose alteration restricts cleanly to R(M)|_X is non-obvious.

## Updated verdict (2026-05-24, post-Hilbert-check)

The geometric realization route, as standardly conceived, is **substantially blocked**:

1. **Poincaré-duality obstruction**: R(M) is not Gorenstein for general M, so no smooth projective Y_M with H*(Y_M) ≅ R(M) exists.
2. **Dimensional obstruction** (new): the X-vector is graded by subset size, peaking at k ≈ n/2 ≫ r. Every flat-indexed matroid variety (top degree r or r-1) is too short to contain X-vector data. The Hilbert series simply doesn't fit.
3. **Avenue 2 misidentification**: Hausel-Sturmfels realizes h-vector dims, not f-vector dims.

**What's left:**
- **Subset-indexed cohomology rings.** Only the coordinate subspace arrangement complement / moment-angle complex has the right dimensions (= R(M) itself). But these are non-compact / non-Kähler, so Hard Lefschetz doesn't apply directly.
- **Non-Kähler Lefschetz theory.** L²-cohomology of complete-but-non-compact spaces (Hausel-Sturmfels-style hyperkähler), mixed Hodge structure on open varieties, or symplectic / LCK Lefschetz theorems on moment-angle manifolds could provide a substitute. None of these has been applied to matroid face rings as far as I can tell.
- **A fundamentally different combinatorial-geometric construction.** Possibly the variety has nothing to do with the lattice of flats and instead uses the simplicial complex IN(M) directly (e.g., as a real analog of an algebraic torus quotient).

**Practical recommendation:** the geometric route, as the prior agent surveyed, is essentially closed for the f-vector / equivariant log-concavity question in the form we want. Spending more research time hoping for a flat-indexed embedding is unlikely to pay off. The honest options going forward are:

(i) **Pursue the Schur-complement KNPV-style proof** despite the depth-3 difficulty (notes/23). This is in the combinatorial / linear-algebraic regime, which is where all existing successful proofs (paving case, ALOV polynomial capacity) live.

(ii) **Investigate non-Kähler Lefschetz theory** on the moment-angle manifold Z_{IN(M)} or the coordinate-subspace-arrangement complement U_{IN(M)}. This is research-program-scale and high-uncertainty.

(iii) **Treat the paving theorem as the publishable result** (already proven) and let the non-paving case remain a stated open question for the community.

## Key arXiv references (consolidated)

- AHK: arXiv:1511.02888 — Hodge theory for combinatorial geometries.
- BHMPW: arXiv:2002.03341 (semi-small decomposition), arXiv:2010.06088 (singular Hodge theory).
- ANR 2023: arXiv:2309.14312 — equivariant HL on AHK Chow ring.
- Eur-Huh-Larson 2022: arXiv:2207.10605 — stellahedral geometry of matroids.
- BEST 2021: arXiv:2103.08021 — tautological classes of matroids.
- Pagaria-Pezzoli 2021: arXiv:2105.04214 — Hodge theory for polymatroids.
- Binder 2024: arXiv:2412.05732 — singular cohomology ring of a matroid.
- Hausel-Sturmfels: arXiv:math/0203096 — toric hyperkähler varieties.
- Buchstaber-Panov: arXiv:math/9912199 — torus actions and moment-angle complexes.
- Panov-Ustinovsky: arXiv:1008.4764 — complex structures on moment-angle manifolds.
- Swartz 2002: arXiv:math/0210376 — g-elements of matroid complexes (generic WLP).
- De Longueville Math. Z. 1999 — ring structure on coordinate subspace arrangement cohomology.

## Pointer

This note supersedes the geometric portions of `notes/21` and parts of `notes/22`. It is the canonical entry point for any future "geometric realization" work on this project.
