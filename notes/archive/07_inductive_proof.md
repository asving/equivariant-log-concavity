# Inductive proof attempt and its scope

## Setup of deletion-contraction for `R`, `R^∨`, and `S`

Fix `M` on `[n]`, choose `e ∈ [n]` non-loop. Two SES of graded vector spaces:

**On R (covariant under deletion):**
  `0 → R(M/e)[−1] →^{x_e ·} R(M) →^{x_e ↦ 0} R(M\e) → 0`
where the left map is multiplication by `x_e`, shifting degree by `+1` (i.e. `[−1]` means
degree shifts up by 1 because `x_e` increases degree).

This SES *splits* (as graded vector spaces) when `M` is **simple** (no parallels):
  `R(M) ≃ R(M\e) ⊕ x_e · R(M/e)`.
Otherwise the SES is non-split and the analysis becomes messier.

**On R^∨ (contravariant: roles swapped):**
  `0 → R^∨(M\e) → R^∨(M) → R^∨(M/e)[−1] → 0`
with the left map inclusion (those `y_T` with `e ∉ T`) and the right map projection
(those `y_T = y_e · y_{T\e}` for `e ∈ T`). Splitting: same condition.

## The S-decomposition

For simple `M`, write `S(M) = R(M) ⊗ R^∨(M) = A ⊕ B ⊕ C ⊕ D` where:

  | piece | left factor      | right factor       |
  |-------|------------------|--------------------|
  | A     | `R(M\e)`         | `R^∨(M\e)`         |
  | B     | `R(M\e)`         | `y_e·R^∨(M/e)`     |
  | C     | `x_e·R(M/e)`     | `R^∨(M\e)`         |
  | D     | `x_e·R(M/e)`     | `y_e·R^∨(M/e)`     |

with `A ≅ S(M\e)` and `D ≅ S(M/e)`.

## How `L = ∑_i x_i ⊗ x_i` acts on the decomposition

Split `L = L' + L_e` with `L' = ∑_{i≠e}` and `L_e = x_e ⊗ x_e`. Computing case-by-case:

- `L'(A) ⊆ A`, action = `L(M\e)`.
- `L'(D) ⊆ D`, action = `L(M/e)`.
- `L'(B) ⊆ B`, acting as the **hybrid Lefschetz** on `R(M\e) ⊗ R^∨(M/e)` (left factor uses M\e indep, right factor M/e indep), call it `L_{(M\e, M/e)}`.
- `L'(C) ⊆ C`, similarly the hybrid `L_{(M/e, M\e)}`.
- `L_e(A) = L_e(C) = L_e(D) = 0` (because either `x_e^2 = 0` on left, or `∂_e b = 0` on right).
- `L_e(B) ⊆ C`. This is the **mixing map** `B → C` given by `x_S ⊗ y_{T'∪e} ↦ x_{S∪e} ⊗ y_{T'}`.

In block-matrix form, with rows/cols ordered (A, B, C, D):

```
L  =  [ L(M\e)   0          0          0    ]
      [ 0        L_{(M\e,M/e)}  0      0    ]
      [ 0        L_e          L_{(M/e,M\e)} 0    ]
      [ 0        0          0          L(M/e) ]
```

`L` is **block-lower-triangular** with the diagonal blocks `L(M\e), L_{(M\e,M/e)}, L_{(M/e,M\e)}, L(M/e)`.

## The induction step

Compute `L^d` block-wise. Because the block matrix is lower-triangular,

`L^d  =  diag( L(M\e)^d,  L_{(M\e,M/e)}^d,  L_{(M/e,M\e)}^d,  L(M/e)^d )  +  (lower-triangular extras involving L_e)`.

The off-diagonal pieces involve `L_e ∘ L'^{d-1}` and similar — they map B-derived blocks into C-derived blocks.

**Inductive hypothesis (assume on smaller matroids):** Hard-Lefschetz `L^d : S_{-d} → S_d` is iso on smaller matroids `M\e`, `M/e`, **AND on the hybrid 2-matroid packages** `R(M\e) ⊗ R^∨(M/e)` and `R(M/e) ⊗ R^∨(M\e)`.

**Snake-lemma / filtration argument:** With L block-lower-triangular, hard Lefschetz on each diagonal block plus a compatible analysis of the off-diagonal `L_e`-mixing implies hard Lefschetz on the total.

This is the 5-lemma you've worked through before.

## The catch: hybrid packages

The diagonal blocks include **`L_{(M\e, M/e)}`** — Lefschetz on `R(M\e) ⊗ R^∨(M/e)`. This is *not* `S(N)` for any matroid `N`; it is a *generalized Lefschetz package on two distinct matroids* sharing a ground set.

**For the proof to be self-contained, the inductive statement must include hybrid packages.** So the right inductive statement is:

  *For every pair `(M_1, M_2)` of matroids on the same ground set with `M_2 ≼ M_1`
  (i.e., every indep set of `M_2` is indep in `M_1`), hard Lefschetz holds on
  `R(M_1) ⊗ R^∨(M_2)` for `d ≥ 2`.*

Pairs `(M\e, M/e)` satisfy `M/e ≼ M\e` (indep sets of M/e are subsets of those of M\e once we forget `e`). So the inductive statement is well-stated.

## Where the induction works cleanly — the largest class

The induction works if for some choice of `e`:
1. `M\e = M/e` (so the hybrid packages reduce to `S(N)` for `N = M\e = M/e`).
2. The SES of `R` and `R^∨` split.

Both happen iff `e` is a **coloop** of `M` (= "free" element, `M ≃ (M\e) ⊕ {e}`). Then
hard Lefschetz on `M` follows by Künneth from hard Lefschetz on `M\e` and on the
trivial 1-element matroid.

**Largest class with clean induction: matroids built recursively from uniform matroids by direct sum.** These are exactly the **transversal matroids** of "rank-disjoint" union form, OR equivalently **direct sums of uniform matroids** — equivalent to **matroids with no rank-2 flat of size ≥ 3 (other than within a uniform summand)**.

These are sometimes called **"paving"** or **"direct-sum-of-uniforms"** matroids — already a fairly broad class.

## The barrier for graphic matroids like M(K_5)

`M(K_5)` is **not** a direct sum of uniforms — it has triangles (rank-2 flats of size 3), and 4-cycles, all interacting. So the clean induction does *not* apply.

For `M(K_5)`, the hybrid `(M\e, M/e)` already requires hard-Lefschetz-on-hybrid for
*smaller* matroid pairs — but those smaller pairs may themselves have non-trivial
mixing structure.

**Crucially**: our computational data now shows **CONJ-A (hard Lefschetz at d=2)
fails for `M(K_5)` with deficit 180.** So the unrestricted version of CONJ-A is
**FALSE**. The induction cannot establish a false statement.

But the user's weaker conjecture — *injectivity* of `L : S_{-d} → S_{-d+2}` — does
hold for `M(K_5)` (confirmed). The induction for this *weaker* statement might still
go through — see next section.

## Inductive proof of the WEAKER user-conjecture (sketch)

Replace "hard Lefschetz iso `L^d`" everywhere by "L injective on `S_{-d} → S_{-d+2}`".

In the block-lower-triangular form, L being injective on each diagonal block
plus the mixing `L_e : B → C` being "consistent" implies L injective on S(M).

**Subtle point:** Injectivity is preserved by the "5-lemma" only in some directions
of the short exact sequences. Specifically: if `0 → X → Y → Z → 0` is exact and
`L : Y → Y'` factors through `L|_X : X → X'` and `L|_Z : Z → Z'`, then injectivity
on `X` AND `Z` gives injectivity on `Y` ONLY IF the mixing map `X → Z'` (the "extension class" composed with L) is compatible.

For our case the mixing is exactly `L_e : B → C`. After computing this and checking
compatibility, the induction should give injectivity on `S(M)`.

**The clean inductive statement for the weaker conjecture:**

  *For every M_1 ≽ M_2 on `[n]` and every `d ≥ 2`, the map `L : R(M_1)_m ⊗ R^∨(M_2)_{-(m+d)} → R(M_1)_{m+1} ⊗ R^∨(M_2)_{-(m+d-1)}` is injective for each `m`.*

(The map uses M_1 relations for multiplication and M_2 relations for contraction.)

This is the right "category of inductive statements" — and I conjecture it goes through
for ALL `(M_1, M_2)` with `M_2 ≼ M_1`, giving a proof of the user-conjecture and hence ELC.

## Comparing to AHK's induction

AHK use induction on "matroid flips" (a particular sequence of stellar subdivisions
of the Bergman fan). At each step they prove **the full Hodge-Riemann package
simultaneously for all degrees** using a single linear-algebra fact about how flips
move classes.

For our setup the analog would be: prove "user's L-injectivity for all `d≥2`
simultaneously" using the deletion-contraction step as the "flip". This is a single
step but proving it requires the **hybrid** generalization above.

## What is the "right" statement to inductively prove?

**Best candidate:**

> **CONJ-A'.** For every pair `(M_1, M_2)` of matroids on `[n]` with `M_2 ≼ M_1`
> (= each indep of M_2 is indep in M_1) and every `d ≥ 2`:
> the operator `L : R(M_1) ⊗ R^∨(M_2) → R(M_1) ⊗ R^∨(M_2)` (raising external degree by 2)
> is INJECTIVE on each `(R(M_1)_m ⊗ R^∨(M_2)_{-(m+d)})`-block.

This statement:
- is preserved under direct sum (Künneth);
- has a clean inductive step via deletion-contraction;
- implies ELC for every matroid M (by taking M_1 = M_2 = M);
- avoids the failure mode of CONJ-A (which asked for ISO, not just INJ).

The boolean / free / direct-sum cases prove a Künneth-style starting basis. The induction
on `|E|` propagates via the SES + block-triangular L.

## Largest class for which this proof currently works

- **Direct sums of uniform matroids** ✓ (Künneth).
- **Coloop-extensions of direct-sums-of-uniforms** ✓ (induction goes through cleanly
  because M\e = M/e = (the smaller matroid) for a coloop e).
- **For general M**: the induction step requires CONJ-A' on hybrid pairs, and we have
  no proof of that yet.

**Verdict**: clean inductive proof for the class of **transversal direct-sums** (matroids
that are direct sums of uniforms). For broader classes, the hybrid version of the
conjecture is needed.

For matroids like `M(K_5)`, `M(K_6)`, `M(K_n)` graphic, we need either:
  (a) prove CONJ-A' on hybrid pairs (a new piece of theory),
  (b) use a different approach (Lorentzian polynomials, geometric realization, ...).

The numerical data so far (M(K_5) confirmed INJ at d=2 and d=3) is consistent with
CONJ-A' being true even in the M(K_5) regime, so the conjecture is alive.

Once M(K_6) and M(K_7) finish, we'll have stronger data.
