# Main findings — summary

## Data (computational, mod-p rank, exact for the small ones)

| Matroid              | f-vector                | ker L (d=1) | L^d iso for d≥2? |
|----------------------|-------------------------|-------------|-------------------|
| U_{1,2}              | (1,2)                   | 0           | trivial           |
| U_{2,3}              | (1,3,3)                 | 0           | **ISO**           |
| U_{2,4}              | (1,4,6)                 | 0           | **ISO**           |
| U_{3,4}              | (1,4,6,4)               | 0           | **ISO**           |
| U_{2,5}              | (1,5,10)                | 0           | **ISO**           |
| U_{3,5}              | (1,5,10,10)             | 0           | **ISO**           |
| U_{2,6}–U_{4,7}      | various                 | 0           | **ISO**           |
| U_2 ⊕ U_2 ⊕ U_2      | (1,6,12,8)              | 0           | **ISO**           |
| M(K_4)               | (1,6,15,16)             | **6**       | **ISO**           |
| Fano                 | (1,7,21,28)             | **21**      | **ISO**           |
| NonFano              | (1,7,21,29)             | **15**      | **ISO**           |
| Pappus               | (1,9,36,75)             | **27**      | **ISO**           |
| NonPappus            | (1,9,36,76)             | **21**      | **ISO**           |
| Vamos V_8            | (1,8,28,56,65)          | **16**      | **ISO**           |
| AG(3,2)              | (1,8,28,56,56)          | **168**     | **ISO**           |

**Including the Vamos V_8 (non-realizable over any field)**. So CONJ-A is consistent
with non-realizability — strong evidence the conjecture is matroid-theoretic, not
algebro-geometric.

## Three propositions, in order of certainty

### **PROP-1 (proved).**  Injectivity of `L^{d-1} : S_{-d} → S_{d-2}` implies ELC.

  - Proof in `01_setup_and_inj_implies_ELC.md`. Restrict to each internal-degree-`m`
    block; cokernel is an honest `Aut(M)`-rep ⇒ `[f_{m+1}][f_{m+d-1}] - [f_m][f_{m+d}] ≥ 0`
    in `Rep(Aut(M))`. Setting `d=2` gives standard ELC on consecutive `(f_m, f_{m+1}, f_{m+2})`.

### **CONJ-A (strong, all data supports).**  For every matroid `M` and every `d ≥ 2`, the map

  `L^d : S_{-d} → S_d`  is an `Aut(M)`-equivariant isomorphism.

  Equivalently, on each `(internal-degree, ext-degree)` block,
  `L^d : (R_m ⊗ R^∨_{-(m+d)}) → (R_{m+d} ⊗ R^∨_{-m})`
  is iso between equidimensional `Aut(M)`-reps.

  **Consequence.** CONJ-A implies user's "injective `L^{d-1}` on `S_{-d}`" (just factor `L^d` as `L · L^{d-1}` ⇒ `L^{d-1}` is injective). Hence CONJ-A ⇒ ELC.

  **Stability.** CONJ-A also holds for arbitrary positive rescalings: `L_c = ∑ c_i (x_i ⊗ x_i)`
  for any tuple of nonzero scalars `c_i` (data confirms even mixed positive c_i give iso).
  But **random rank-1 two-forms `ℓ ⊗ ℓ'` with `ℓ ≠ ℓ'` FAIL hard Lefschetz**. The
  Lefschetz here is *intrinsically a sum-of-squares*, not a generic linear form.

### **CONJ-B (weaker, the user's original).**  For every matroid `M` and `d ≥ 2`,
  `L : S_{-d} → S_{-d+2}` is injective. (Direct consequence of CONJ-A.)


## Key structural insights

### The Lefschetz is a Casimir

`L = ∑_i x_i ⊗ x_i` is the unique (up to scaling) `Aut(M)`-invariant element of
`R_1 ⊗ R_1^∨`, the "diagonal" or "identity-tensor" element of `V ⊗ V^*` for
`V = k^n`. **Generic Lefschetz fails; the symmetry-canonical Lefschetz works.**
This is unlike the AHK Chow-ring story, where generic linear forms give Lefschetz.

It is much more like the **Casimir** / **Laplacian** of an `sl_2` triple or
representation-theoretic Hodge package.

### T_L as completely-positive map

Via `S ≅ End_k(R)` (canonical iso for finite-dim `R`), the operator `T_L` becomes

  `T_L(Φ) = ∑_i M_{x_i} ∘ Φ ∘ M_{x_i}^*`

where `M_{x_i}` is left-multiplication by `x_i` and `M_{x_i}^* = ∂_{x_i}` is its
adjoint w.r.t. the monomial inner product. **`T_L` is a completely positive map on
`End(R)`** — formally a "quantum channel without trace preservation".

Specifically: `∑ K_i K_i^* = E` (Euler op = degree on `R`), so `T_L(id_R) = E`,
and `T_L^2(id_R), ...` produce a sequence of "spectral averages" of the matroid's
multiplication operators. The Kraus operators `K_i = M_{x_i}` generate `R ⊂ End(R)`
as a subalgebra (since `M_{x_i} M_{x_j} = M_{x_i x_j}`).

**Hard Lefschetz on S** ⟺ **invertibility of `T_L^d` between "external degree ±d"
spectral subspaces**.

### sl_2 triple

Define adjoint `T_Λ(Φ) = ∑_i M_{x_i}^* Φ M_{x_i}` (lowering external degree by 2).
Then `[T_L, T_Λ]` is approximately the external-degree operator `E_{ext}`. In a
"free" approximation this is exactly an `sl_2`-triple, so hard Lefschetz follows
from standard `sl_2` representation theory.

**Refinement.** `[T_L, T_Λ] = E_{ext} + (correction from matroid relations)`. The
correction is what we must control. For the matroid relations to "respect" the
`sl_2`, we expect:

  **CONJ-C.** `[T_L, T_Λ] - E_{ext} = (degree-0 operator vanishing on each
  Aut(M)-irreducible)` — i.e., the correction is *scalar on each irrep*, hence
  doesn't break Lefschetz decomposition.

### Tensor / direct sum compatibility

For `M = M_1 ⊕ M_2`: `R(M) = R(M_1) ⊗ R(M_2)`, `S(M) = S(M_1) ⊗ S(M_2)`,
`T_{L(M)} = T_{L_1} ⊗ id + id ⊗ T_{L_2}` (diagonal).

By the **Künneth Lefschetz package theorem**, hard Lefschetz on both factors implies
hard Lefschetz on the product. So CONJ-A is automatically compatible with direct sums.

In particular, every direct sum of uniform matroids satisfies CONJ-A (including d=1!).
The data confirms this: `U_2 ⊕ U_2 ⊕ U_2` has hard Lefschetz at d=1.


## The d=1 kernel as a matroid invariant

For non-uniform matroids with rank-2 flats of size ≥ 3 (= non-trivial "lines"):

  **Empirical formula:**  `dim ker(L : S_{-1} → S_1)  =  ∑_p C(L_p, 2)`

where `L_p` = number of rank-2 flats of size ≥ 3 through point `p`. Verified for
M(K_4), Fano, NonFano, Pappus, NonPappus (and trivially for uniforms / direct sums).

For matroids without non-trivial lines but with non-trivial 4-circuits (Vamos, AG(3,2)):

  **Empirical formula:**  `dim ker  =  ∑_{(C_1,C_2) pair of girth-circuits} |C_1 ∩ C_2|`

Verified for Vamos (16), AG(3,2) (168).

**Unified speculation.** The kernel at d=1 captures something like the **"matroid
H^1"** — secondary obstructions to global indep-exchange. It may be canonically
identifiable with `Tor` between `R(M)` and a co-`R(M)`-module, or with the
"rank-2 obstruction" of a derived deletion-contraction long exact sequence.

These d=1 kernels are NOT obstacles to ELC (the d=1 ELC content is trivial), but
they are a beautiful matroid invariant in their own right.


## Geometric / categorical pictures (more speculative)

### Tautological End-bundle

In the Eur–Larson–Berget tautological framework, `M` has subbundle `𝒮_M` of rank
`rk(M)` on the stellahedral / permutohedral variety. `End(𝒮_M)` is a rank-`r^2`
bundle. `S = R ⊗ R^∨` corresponds to a graded slice of `Sym(End(𝒮_M)^∨)`; the
Lefschetz `L = ∑ x_i ⊗ x_i` is the "identity-section" / "trace class" in
`End(𝒮_M)|_{torus-fixed point}`.

Hard Lefschetz on `S` would then be a Lefschetz statement for the equivariant
cohomology of the bundle `End(𝒮_M)`, parallel to AHK but for matroid-tautological
endomorphism bundles.

### Bigraded / "Cox-ring" reformulation

Define `S' = R(M) ⊗ R^∨_{apolar}(M)`, where the second factor uses the **Macaulay
inverse-system / apolar product** (so that `y_S · y_T = y_{S∪T}` if `S ∩ T = ∅` and
`S ∪ T` indep, else `0`). Then `S'` is a commutative bigraded ring, with `L = ∑ x_i ⊗ y_i`
an honest element of bidegree `(1, 1)`.

However, the user's `T_L` is NOT just "multiplication by L" — it's a second-order
operator. The relation between commutative-`S'`-multiplication and the user's `T_L`
is via the **diagonal / shift**: multiplication by `L` preserves external degree
`|S| - |T|` (sends `(m, n)` to `(m+1, n+1)`, ext-deg `m-n` unchanged), while `T_L`
**raises** external degree by 2. So `T_L = (mult by L) ∘ (degree-shift)`.

A clean reformulation requires identifying the right co-multiplication structure on
`S'` that compensates for this — possibly connected to the **Soergel-bimodule**
formalism for matroid Kazhdan-Lusztig polynomials.

### Deletion-contraction

`R(M) ↦ R(M\e)` is a quotient (in the deletion direction). `R^∨` quotient direction
is reversed (a sub). So `S(M) ↦ S(M\e)` is neither a quotient nor a sub — it's a
**twisted** functor.

  **PROPOSAL.** The right object to consider is the **complex**

      `S(M\e) ← S(M) ← S(M/e)[shift]`

  with `T_L` compatible. If this is a short exact sequence (or distinguished
  triangle in some derived sense), induction on `n` proves CONJ-A: assume CONJ-A
  for `M\e`, `M/e`, deduce for `M`. This mirrors the AHK proof strategy.


## Variants to try

1. **`L_c = ∑ c_i x_i ⊗ x_i` for `c_i > 0`**: probably works for any positive c.
   (Data: works for several random positives.)
2. **`L_q = ∑ q_{ij} x_i ⊗ x_j` for a positive-semi-definite matrix `Q = (q_{ij})`**:
   should still work as long as `Q` is PSD. **Test.**
3. **Exterior version (anticommuting `x_i`)**: same dim, signed multiplication; may
   give a *more rigid* Lefschetz. **Test.**
4. **Augmented version (BHMPW-style)**: add `x_0` with relations matching `Σ x_F`.
   **Test.**


## What I'd recommend next, concretely

1. **Try to prove CONJ-A by deletion-contraction induction**. This was AHK's strategy
   for the Chow ring; it should work here too. The hard step is establishing the
   "five-lemma compatibility" between `S(M)`, `S(M\e)`, `S(M/e)`.

2. **Test CONJ-A on a few more pathological matroids**: non-Pappus (done), Reid
   matroid, P_8 (perspective), Q_8, the non-Pappus non-Vamos non-Fano oddballs.
   Currently 0 counterexamples in ~20 matroids tested.

3. **Identify the d=1 kernel canonically.** It looks like a genuine new matroid
   invariant. Maybe relate to **Orlik-Solomon's algebra**, **broken-circuit module**,
   or **Stanley-Reisner Tor**.

4. **Find the right geometric model for `S`.** The "End-bundle" picture is the
   most plausible — try to make it rigorous via the **stellahedral / Bergman-fan**
   formalism (Eur, Eur-Larson, Berget-Eur-Spink-Tseng).

5. **Write up CONJ-A as a paper**: even if proof eludes, the conjecture + data
   for non-realizable matroids (Vamos passing!) is publishable. ELC follows from
   CONJ-A, so this provides a clean, statable-and-checkable target for ELC.
