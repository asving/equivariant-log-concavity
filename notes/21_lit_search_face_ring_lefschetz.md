# Literature search: face-ring Lefschetz and the position of our conjecture

**Date: 2026-05-23.**

Comprehensive search for high-powered machinery (= Hodge theory, Lefschetz, equivariant g-theorem) that could give the structural ingredient missing for the non-paving case. Two parallel searches: (a) survey papers and post-Swartz extensions; (b) equivariant / specific-linear-form Lefschetz follow-ups. Findings consolidated here.

## Reframing: our conjecture in face-ring language

Our `R(M) = k[x_1, ..., x_n] / (x_C : C ∈ Circ(M); x_i^2)` is the **exterior face ring of the matroid independence complex `IN(M)`**. The Lefschetz operator `L = Σ x_i ⊗ x_i` corresponds, after orbit decomposition, to **multiplication by the symmetric Aut(M)-invariant linear form `ω = Σ x_i`** on `R(M)`.

So our conjecture rephrases as:

> **Equivariant X-restricted WLP for the matroid face ring.** For every loopless matroid `M`, multiplication by `ω = Σ x_i` is injective from `R(M)_k|_X` to `R(M)_{k+1}|_X` for every `k < r/2` in our bigrade hypothesis, where `R(M)_k|_X` denotes the subspace spanned by `{x_A : A ∈ X_k(M)}`.

This is the f-vector analog of the matroid g-theorem, restricted to balanced bipartitions.

## The three asymmetries we found

### Asymmetry 1: Chow ring side is solved equivariantly, face ring side isn't

- **Chow ring `A(M)` (AHK Chow ring)**: Aut(M)-equivariant hard Lefschetz with G-invariant ample class proven by Angarone–Nathanson–Reiner [ANR, arXiv:2309.14312, JLMS 2025, Cor. 2.30]. Strengthened to equivariant γ-positivity by BGKMNT [arXiv:2408.00745, 2024]. But graded dims of `A(M)` = Whitney numbers, NOT f-vector.

- **Face ring `R(M) = k[IN(M)]`**: only Swartz's 2002 *generic* WLP [arXiv:math/0210376]. No equivariant or specific-form extension in 23 years.

This is the cleanest statement of where our problem sits. ANR's program reaches one matroid invariant (Whitney) equivariantly; the analogous result on the face ring (which carries our f-vector) has not been done.

### Asymmetry 2: SLP fails for graphic-matroid basis-generating-polynomial Gorenstein algebras, but not for our face ring (empirically)

Takahashi [arXiv:2501.13348, 2025] disproves Maeno-Numata's SLP conjecture for the *basis-generating-polynomial* Gorenstein algebra of *graphic* matroids, via higher Hessian degeneracy. This is a different algebra from `R(M)`, but it's a warning that "Lefschetz on matroid-derived algebras" can fail for graphic matroids — so any equivariant lift on the face-ring side must use the specific structure of `R(M)`.

Crucially: our empirical evidence shows the symmetric form *does* work for graphic matroids on the X-restricted face ring. The X-restriction must be what makes the difference.

### Asymmetry 3: The X-restriction has no published treatment

I searched for "balanced indep bipartitions", "complementary independent pair", "matroid pair", "dual-independent partition", and synonyms. No published Lefschetz / face-ring result restricts to this subspace. The X-restriction is genuinely new, and its role as "rescuer" of the symmetric Lefschetz is structurally specific to our setup.

## Most-promising specific approaches identified

### Approach A: Adapt ANR's Chow-ring proof to the face ring

ANR's proof that `A(M)` has a G-invariant Lefschetz element uses the semi-small decomposition (Braden-Huh-Matherne-Proudfoot-Wang, arXiv:2002.03341). The face ring `R(M)` is structurally different (= simpler relations, weaker Hodge structure), but the technique might adapt. **Highest reward, longest path.**

### Approach B: Gui-Xiong's explicit equivariant L on free exterior algebra, restricted to R(M)

Gui-Xiong [arXiv:2205.05420] construct an explicit equivariant operator `L = Σ_k e_{θ_k} ⊗ i_{θ_k}` on the free exterior algebra `Λ(V)` with G-action. They prove equivariant HL + Hodge-Riemann.

For our problem: the matroid face ring `R(M)` is the quotient of the free exterior algebra `Λ(k^n)` by the circuit relations `(x_C : C ∈ Circ)`. If the equivariant HL on `Λ(V)` "survives" the quotient (= the matroid relations form an Aut(M)-subrep on which their `L` is well-behaved), we'd get equivariant WLP on `R(M)`.

**This is the most concrete first thing to test.** Computational: take Gui-Xiong's explicit `L`, restrict to our matroid quotient `R(M)`, and check whether it's still injective on X-restricted graded pieces.

### Approach C: Structural understanding of the X-restriction

The empirical finding (notes 12, 16, 19, 20): the symmetric form fails WLP on full `R(M)` for non-paving M (= kernel of ∂* on Indep_k is non-trivial), but succeeds on the X-restriction. **This is the new mathematics**: a specific subspace of the matroid face ring where the symmetric Lefschetz operator works precisely because the matroid axioms "balance" the constraints.

Connecting this to the literature: the X-restriction corresponds to the matroid intersection of M with itself (via complementation A ↔ E\A). This puts our problem in matroid-intersection territory, which has its own active literature (Anari-Liu-Vuong mixing, etc., but those are about spectral gap, not face-ring Lefschetz).

## Specific theorems to attempt

> **Theorem candidate 1 (Gui-Xiong restriction).** The Gui-Xiong equivariant Lefschetz operator `L_{GX}` on `Λ(V)` descends to `R(M)` with the property that `L_{GX}: R(M)_k|_X → R(M)_{k+1}|_X` is injective.

> **Theorem candidate 2 (ANR-style for face ring).** The matroid face ring `R(M)` admits a semi-small-style decomposition under stressed-flat relaxation such that an Aut(M)-invariant Lefschetz element exists.

> **Theorem candidate 3 (X-restriction as natural subspace).** The X-restriction `R(M)|_X` is exactly the subspace of `R(M)` on which the symmetric form `ω = Σ x_i` is *guaranteed* to be Lefschetz, regardless of whether the matroid is paving or not.

## Key references

| Paper | What it gives | What it lacks for us |
|---|---|---|
| **Swartz 2002** (arXiv:math/0210376) | Generic WLP on `R(M)/Θ` | Specific symmetric form, equivariance |
| **ANR 2023** (arXiv:2309.14312) | G-invariant Lefschetz on `A(M)` | Wrong algebra (Chow not face) |
| **BGKMNT 2024** (arXiv:2408.00745) | Equivariant γ-positivity of `A(M)` | Wrong algebra |
| **AHK 2018** (arXiv:1511.02888) | Hodge theory of `A(M)` | Wrong algebra |
| **BHMPW 2020** (arXiv:2002.03341) | Semi-small decomposition for `A(M)` | Wrong algebra |
| **Adiprasito 2018** (arXiv:1812.10454) | HL for spheres | `IN(M)` is not a sphere |
| **Gui-Xiong 2022** (arXiv:2205.05420) | Equivariant HL on `Λ(V)` (free exterior) | Doesn't quotient by matroid relations |
| **Takahashi 2025** (arXiv:2501.13348) | Disproves SLP for basis-gen-poly Gorenstein algebra of graphic matroids | Different algebra from `R(M)` |
| **Ardila-Denham-Huh 2020** (arXiv:2004.13116) | Conormal-fan Lefschetz → f-vector LC | Non-equivariant |
| **Hausel-Sturmfels 2002** (Doc. Math.) | Re-proof of Swartz via toric hyperkähler | Same generic-only limitation |
| **Maeno-Numata 2011** (arXiv:1107.5094) | SLP conjecture for basis-gen-poly | Conjecture refuted in graphic case |
| **Bohm-Papadakis 2015** (arXiv:1501.01513) | WLP under stellar subdivision (Gorenstein) | Matroid relaxation isn't stellar |

## The cleanest statement of what's open

**Problem.** Prove (or refute) the following: for every loopless matroid M on `n` elements with rank `r`, the symmetric linear form `ω = Σ x_i ∈ R(M)_1` satisfies `ω: R(M)_k|_X → R(M)_{k+1}|_X` injective for every `k < r/2` satisfying our bigrade hypothesis.

Equivalently: the equivariant log-concavity of the f-vector of `M`, which we've reduced to this single statement via the orbit decomposition.

**Status of the problem:**
- Verified empirically on > 2 × 10⁵ orbits.
- Proven for paving matroids (PAPER.md).
- For non-paving matroids: open. **No existing theorem in matroid Lefschetz / Hodge literature directly applies.** This is a genuine research-level open problem.

The most promising next-session direction is computationally testing Gui-Xiong's `L` operator after restriction to `R(M)` (= Approach B). If their explicit `L` gives the right behavior on our test matroids, we have a clear technical path.
