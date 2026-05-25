# Running ideas — let it roam

Working log. Not polished. Marked **PROVED**, **OBS** (observed numerically), **CONJ**,
**WILD** (speculation), **TODO**.


## A. What the first run says

The first pass (script: `computations/matroid_lefschetz.py`) tested
`U_{1,2}, U_{2,3}, U_{2,4}, U_{3,4}, U_{2,5}, U_{3,5}, M(K_4), Fano, NonFano`. Every
matroid satisfies, for `d ≥ 2`,

  **OBS-1.** `L^d : S_{-d} → S_d` is an iso (hard Lefschetz).
  **OBS-2.** `L^{d-1} : S_{-d} → S_{d-2}` is injective.
  **OBS-3.** `L : S_{-d} → S_{-d+2}` is injective for every `d ≥ 2`.

And:
  **OBS-4.** `L : S_{-1} → S_1` is iso for *uniform* matroids; for non-uniform
  it has a kernel/cokernel of dimensions (`d=1` case):
  - `M(K_4)`: 6   (= n)
  - `Fano`: 21    (≈ # circuits? Fano has 7 circuits of size 3 → no, 21 = `f_2 = C(7,2)`)
  - `NonFano`: 15

So both inj and surj fail simultaneously at `d=1`. Note that `d=1` is the trivial-ELC
case: it would give `[f_m][f_{m+1}] ≥ [f_{m+1}][f_m]` (vacuous). So failure at d=1
does **not** affect ELC.

**Possible upgraded conjecture (mine, not yet user's):**

  **CONJ-A**:  For every matroid `M` and every `d ≥ 2`, the map
  `L^d : S_{-d} → S_d` is an isomorphism, equivalently each component
  `L^d : R_m ⊗ R^∨_{-(m+d)} → R_{m+d} ⊗ R^∨_{-m}` is iso.

If CONJ-A holds it gives **equivariant Poincaré duality on a richer object**, and
all of `L^k : S_{-d} → S_{-d+2k}` are injective for `1 ≤ k ≤ d` (by composition with
the iso `L^{d-k} : S_{-d+2k} → S_d`, since `L^d = L^{d-k} ∘ L^k`). In particular it
implies the user's "L injective on S_{-d}" conjecture, hence ELC.


## B. Why d=1 is special and what its kernel is

`L : S_{-1} → S_1`. Bigraded: source is `⊕_m R_m ⊗ R^∨_{-(m+1)}`, with `m`-piece
of dim `f_m f_{m+1}`. Target is `⊕_m R_{m+1} ⊗ R^∨_{-m}`, with `m`-piece dim
`f_{m+1} f_m`. Same dimensions block-by-block.

`L(x_S ⊗ y_T)` where `|T| = m+1, |S| = m`:
`= ∑_{i ∈ T, i ∉ S, S∪{i} indep} x_{S∪{i}} ⊗ y_{T \ {i}}`.

For uniform `U_{r,n}`: when `m < r`, every `i ∈ T \ S` with `|S ∪ {i}| = m+1 ≤ r`
gives an indep set ⇒ all `i ∈ T \ S` contribute. **Iso conjectured / observed.**

For non-uniform: there are independent `T`'s of size `m+1` and elements `i ∈ T \ S`
where `S ∪ {i}` is dependent. These "blocked" exchanges may produce kernel elements.

**TODO.** Compute the kernel of `L : S_{-1} → S_1` for `M(K_4)` explicitly. Is the
kernel canonically identifiable with some matroid invariant? Guess: it's related to
the **broken-circuit complex** or **circuit boundaries**.

  **WILD-1.** The kernel of `L : S_{-1} → S_1` is isomorphic, as `Aut(M)`-rep, to
  `⊕_{C ∈ 𝒞(M)} (signed circuit space)`? Could test on Fano vs NonFano (both have
  many circuits; we'd compare kernel dim to circuit invariants).

  **NEW DATA POINTS NEEDED.** Add M(K_5) minus edge, U_{r,n} for larger n, V_8 (Vamos).
  Run kernel-extraction for d=1.


## C. The geometric / algebraic identity of S

### C.1 As End(R)

There is the canonical map `α : R ⊗ R^∨ → End_k(R)` sending `r ⊗ φ ↦ (s ↦ φ(s) r)`,
the **rank-1 operator picture**. Since `dim R < ∞`, `α` is an iso. Under `α`:

- The Aut(M)-action by conjugation on End(R) becomes the **diagonal** Aut(M)-action
  on `R ⊗ R^∨`.
- The "diagonal element" `∑ x_i ⊗ y_i = α^{-1}(π_1)` is the rank-`n` projector
  `π_1 : R → R_1 → R`.
- *Composition* on End(R) corresponds to a non-trivial product on `R ⊗ R^∨`:
  `(a ⊗ b)(c ⊗ d) = a · b(c) · d`. Under this, `L · L = L` (since `π_1^2 = π_1`),
  so the "L^d" the user defines is **not** composition; it is the operator
  `T_L : S → S, a ⊗ b ↦ ∑ (x_i a) ⊗ (x_i · b)`. We need to be careful here.

`T_L` viewed via End(R): take `Φ ∈ End(R)` corresponding to `a ⊗ b`. Then
`T_L(Φ) = ∑ x_i · Φ · ∂_i` where `x_i` is left mult on the codomain and `∂_i`
is right contraction on the domain. **So `T_L` is a "conjugation-like" operator**:

  `T_L(Φ) = ∑_i M_{x_i} ∘ Φ ∘ M_{x_i}^*`

where `M_{x_i}^* = ∂_i` is the adjoint of multiplication w.r.t. the standard pairing.

This is **completely positive** if we work over `ℂ` and view End(R) as `Mat_N(ℂ)`!

  **OBS / WILD-2.** `T_L` is a completely positive map on `End(R)`. Iterating
  `T_L^d` gives a Kraus-decomposition of a CP map with Kraus operators `M_{x_{i_1}}
  · ... · M_{x_{i_d}}`. **Hard-Lefschetz then says: this CP map is invertible on
  the "external-degree (-d, d)" pair.** Random thought: connection to *quantum
  channels* defined by a matroid?

### C.2 As tautological End-bundle on the matroid

In the Eur–Larson / Berget–Eur–Spink–Tseng *tautological classes* picture, the
matroid `M` has a tautological subbundle `𝒮_M` and quotient `𝒬_M` on the Bergman
fan / permutohedral variety. The Chow ring of the matroid is built from Chern
classes of these. **Our `R` corresponds to taking `Sym(𝒬_M^∨)` modulo torsion** or
something similar (the squarefree face ring of `IN(M)` arises as the K-theoretic
"flag" of `M` cut down to a single open part).

  **WILD-3.** `S = R ⊗ R^∨` is the section ring of the line bundle `𝒪(1) ⊠ 𝒪(-1)`
  (or `End` of a fixed rep) on `X_M × X_M`. The diagonal Lefschetz `L` would be
  pullback of the diagonal Kähler class. Hard Lefschetz on `S` would follow from
  hard Lefschetz on `X_M × X_M` along the diagonal.

  **CHECK.** This is the version of "Lefschetz holds on Bergman fan squared"
  which would be a *new* theorem if true. Does it follow from AHK on `X_M`?

### C.3 As Schur–Weyl / GL_n diagonal

In `Sym(V) ⊗ Sym(V^*)` with `V = k^n`, the element `∑ x_i ⊗ y_i` is the
**diagonal** of `V ⊗ V^*`, i.e., the identity in `End(V)`, sitting inside
`Sym^1(V) ⊗ Sym^1(V^*) ⊂ Sym(V) ⊗ Sym(V^*)`.

GL(V) acts on `Sym(V) ⊗ Sym(V^*)` diagonally; `L` is GL(V)-invariant. So
`T_L : S → S` commutes with GL(V) on the unrestricted (matroid-free) ambient space.
**The matroid relations are the GL(V)-non-invariant part** — they break GL down
to `Aut(M) ⊂ S_n`. Still `T_L` commutes with `Aut(M)`.

  **WILD-4.** There is a *natural symmetric polynomial* `p_d ∈ Sym^d(V) ⊗ Sym^d(V^*)`,
  namely the "diagonal of `Sym^d`": `∑_{|α|=d} (multinomial) x^α ⊗ y^α`.
  In the matroid-modified `S = R ⊗ R^∨` this becomes `∑_{S indep, |S|=d} x_S ⊗ y_S`.
  Call this element `Δ_d`. Then **`L^d (1 ⊗ 1) ≠ Δ_d` in general** (different
  combinatorics), but they should be closely related. Probably: `L^d = d! · Δ_d`
  in some sub-quotient. **Test in script.**

### C.4 As Weyl algebra / Heisenberg representation

Identifying `y_i = ∂_i`, R becomes a quotient of `k[x_1,...,x_n]`, and `R^∨` is the
Verdier dual / `D(R)`. There is a natural action of the Weyl algebra
`A_n = k⟨x_i, ∂_j : [∂_i, x_j] = δ_{ij}⟩` on `k[x]`. The user's `R` is `k[x]/I_M`
where `I_M` is the **matroid Stanley-Reisner ideal**. Then `D(R)` is the
"derived dual": `Ext^*_{A_n}(R, A_n)`. Under nice circumstances `D(R)` is
concentrated in one cohomological degree and represents `R^∨` (graded dual).

So **`S = R ⊗_k D(R)` is a sort of `Hom`-complex** in the Weyl-algebra category.
`L = ∑ x_i ⊗ ∂_i` is the natural "evaluation/identity" element.

  **WILD-5.** Hard Lefschetz at `d`-th level on `S` is the statement that the
  `d`-th *Yoneda product* in the Weyl-algebra Ext-algebra is non-degenerate.

### C.5 As graded representation of the bigraded ring `A = k[x_i, y_i]`

Let `A = k[x_1,...,x_n, y_1,...,y_n]` with `deg x_i = (1,0)`, `deg y_i = (0,1)`.
Consider the bigraded ideal `J` generated by:
- `x_I` for `I` a circuit (defines R on the x-side)
- `y_I` for `I` a circuit (defines R^∨ on the y-side, but with a sign trick — see
  below)
- `x_i^2, y_i^2` (the "squarefree" relations)

Then `A/J` is bigraded with `(A/J)_{(a,b)} = R_a ⊗ R^∨_{-b}` — wait, this matches
**only if we replace `y_i = ∂_i` action by a separate "y-multiplication"**. To get
the contraction action, we need to mod out further by the **relations expressing
that `y_i` acts as `∂_{x_i}`**:

  `y_i x_i - 1` for the diagonal? No, more correctly **commutator relations**
  `[y_i, x_j] = δ_{ij}`. With these we get the Weyl algebra `A_n`, not a commutative
  thing.

Let me try a different bigraded approach. Define `B = R ⊗_k R^∨_{shifted}` where
`R^∨_{shifted}` is the dual ring of `R` with its own product (the "Macaulay dual"
product, making it isomorphic to `R` when `R` has Poincaré). This product makes
`R^∨` itself a commutative ring (the "inverse system" ring), generated by `y_i`
in degree `-1`. Then `S = R ⊗ R^∨` is a commutative bigraded ring.

The operator `L = ∑ x_i y_i` is then just an element of `S` of bidegree `(1, -1)`
(external degree 1 - 1 = 0?!? — wait then it doesn't raise external degree by 2!)

Hmm — this discrepancy. The user's `L` does raise external degree by 2. So `L`
is NOT a degree (1,-1) element of the bigraded ring `S` (which would have degree 0).
Rather, `L` acts as an **operator** lifting `(m, k) ↦ (m+1, k+1)` in the (m=|S|,
k=|T| = -extdeg)-bigrading. As an operator on `S`, `L` has total external degree
`(1+1) = 2`.

So `L` is an **operator on `S`**, not an element. The action: multiply by `x_i`
on first factor (degree +1 in first factor), differentiate (Macaulay dual mult by
`y_i`... no, contraction!) on second factor (degree +1 in second factor in the
`-|T|` grading, since |T| → |T|-1 means -|T| → -|T|+1).

OK. So in the bigraded ring `S = R ⊗ R^∨` with bigrading `(a, b) = (|S|, -|T|)`,
`L` is a **degree (1, 1) operator on `S`** (NOT an element of `S`).

The element of `S` of bidegree (1,1) is `∑ x_i ⊗ y_i^{-1}`... wait, `y_i^{-1}` doesn't
exist. So there's no element of bidegree (1,1) in `S`. So `L` is genuinely just an
operator.

Hmm, but then we can ask: is `L` the **multiplication-by-some-element** action of an
element of some larger bigraded ring `S'`? In particular, the obvious candidate is
the element `∑ x_i ⊗ y_i^{(-1 to +1 shift)}`...

Let's try: consider the bigraded vector space `S'` with bidegree shifted so that
`R^∨` is in degrees `+ |T|` (not `-|T|`). Then `S' = R ⊗ (R^∨ with shifted grading)`
has positive bigrading, and the element `∑ x_i ⊗ y_i` is bidegree (1, 1).

But then "L acts by multiplication" on `S'` — well, only if we define multiplication
on R^∨. The Macaulay dual makes R^∨ a ring via the "inverse system" (= apolar
algebra) product: `y_S · y_T = y_{S ⊔ T}` if `S ∩ T = ∅` and `S ⊔ T` indep, else 0.

  **THEN!** `S' = R ⊗ (R^∨ with apolar product, shifted to + grading)` is a bigraded
  algebra. And **L = ∑ x_i ⊗ y_i is the diagonal element of total degree 2**, acting
  by multiplication.

  In this setting, hard Lefschetz `L^d : S'_{-d} → S'_d` (after un-shifting back to
  the user's convention) becomes the question of whether multiplication by `L^d`
  is iso between two bigraded pieces.

  This is a *commutative-ring* Lefschetz statement on a bigraded ring with diagonal
  Lefschetz element. **Very clean!**

  **WILD-6.** `S' := R ⊗ R^∨_{apolar}` is the "double Chow ring" / "matroid TT*-ring".
  Hard Lefschetz on `S'` is **a new conjecture, and a much cleaner statement** than
  the user's.


## D. Functoriality / deletion-contraction

The user noted that `R` and `R^∨` have opposite functoriality.

- **`R(M)`**: `R_d(M)` is the permutation rep on indep sets of size `d`. For
  `M \ e` (deletion), the indep sets of `M \ e` are precisely those of `M` not
  containing `e`. So `R(M \ e)` is the **subring** `R(M)|_{x_e = 0}`.
  For `M / e` (contraction, assuming `e` not loop), indep sets of `M/e` are
  `{S ⊆ [n] \ e : S ∪ e indep in M}`. So `R(M/e) = "x_e · R(M)" / x_e`-type structure
  — actually `R(M/e)_d` injects into `R(M)_{d+1}` by `x_S ↦ x_{S ∪ e}`.

- **`R^∨(M)`**: Dual functorialities. For `M \ e`: `R^∨(M \ e)` is a *quotient*
  (the projection forgetting all `y_T` with `e ∈ T`). For `M / e`: `R^∨(M/e)`
  is a subspace of `R^∨(M)` (those `y_T` with `e ∉ T`, shifted in degree).

So `S = R ⊗ R^∨` has, under deletion `M ↦ M \ e`:
- left tensor factor: **subring** (project out `x_e`).
- right tensor factor: **quotient** (project out `y_T` with `e ∈ T`).

So overall: ne obvious nice functor. **The combination is the "tensor of a contra-
variant and a covariant functor"**, which has no inherent direction.

**WILD-7.** Maybe the right home is not `S` but `Hom(S(M \ e), S(M))` or similar.
Or maybe `S` is best viewed as a *Bridgeland-type stability category* attached to
`M`, in which deletion and contraction are *t-structure tilts*.

Alternatively, the deletion-contraction structure might be cleaner on
**`S' = R ⊗ R^∨_{apolar}`** since both factors then have *the same* functoriality
(both quotients under deletion-of-loop-or-coloop-style operations).


## E. Variants of S worth considering

### E.1 Augmented version
Add an "augmentation" element `0` and add `x_0` to all relations: `R^aug = k[x_0, x_1,...] / (x_I : ...)`. This is the BHMPW augmented Chow ring style, where `x_0`
unifies things. Then `S^aug = R^aug ⊗ R^aug,∨`.

### E.2 Lefschetz with linear ℓ
Replace `L = ∑ x_i ⊗ x_i` with `L_ℓ = ℓ ⊗ ℓ` for a generic linear form `ℓ ∈ R_1`.
This is the "true Lefschetz" element (in the SR-ring world). Test if this is the
*right* Lefschetz; maybe the diagonal `∑ x_i ⊗ x_i` is overdetermined and a generic
`ℓ ⊗ ℓ` does better (or worse).

Equivalent reformulation: `L = ∑ x_i ⊗ y_i` is the *Frobenius-type trace*. A
generic Lefschetz is `(ℓ_1) ⊗ (ℓ_2)` for two generic forms `ℓ_1, ℓ_2`. **Test.**

### E.3 Anti-symmetric / Exterior version
Replace `R` by `Λ(x_1,...,x_n) / (x_I : circuit)`. This is **the Orlik–Solomon-style
exterior face ring**. (Not the usual OS algebra, which has boundary relations.)
Sometimes more functorial. Then `S^ext = Λ R ⊗ Λ R^∨`.

### E.4 Drop x_i^2 = 0 (full Stanley-Reisner)
Then `R` has Krull dim `rk(M)` and is infinite-dim graded. Modulo a regular system
of parameters (linear forms in general position) one gets an artinian quotient whose
Hilbert series is the **h-vector** (not f-vector). The h-vector LC is a famous theorem
(AHK 2018; also Anari et al via Lorentzian). **The right Lefschetz statement here
is the AHK one on the Chow ring, which is a different quotient.**

### E.5 Replace dual with itself via Poincaré
If `R` had Poincaré duality (it doesn't, in general), we could write `S = R ⊗ R`.
For the **Chow ring** `A^*(M)` (AHK), Poincaré does hold. **Conjecture-A on the
Chow-ring version** of `S` would say: on `A^* (M) ⊗ A^*(M)` with diagonal Lefschetz
`L = ∑ Λ_i ⊗ Λ_i`, hard Lefschetz at level `d ≥ 2` holds. This is *new content
beyond AHK's hard Lefschetz on a single copy of A^*(M)*. Might be: tensor product
of hard-Lefschetz packages is automatically hard-Lefschetz under "diagonal" L?

Recall for a Kähler X: `H^*(X) ⊗ H^*(X)` has the diagonal Lefschetz from
`X × X` with Kähler class `pr_1^* ω + pr_2^* ω`. The diagonal `L = pr_1^* ω ∪ pr_2^* ω`
is *not* the X × X Kähler class but its *square minus the symmetric parts*. So
asking hard Lefschetz for diagonal L on X × X is not automatic from X's hard
Lefschetz — but maybe holds in good circumstances (e.g., motivic / Tate twists).


## F. Pieces to compute next

1. **Bigger matroids**: U_{3,6}, U_{4,6}, U_{4,7}, V_8 (Vamos), AG(3,2), W^3, Pappus,
   non-Pappus, the cycle matroids of K_5, etc.
2. **The kernel of `L: S_{-1} → S_1`** for non-uniform: extract a basis, identify
   structure (representation under Aut(M)).
3. **Test if `T_L` is the *unique* `Aut(M)`-equivariant Lefschetz**: try
   `T_{ℓ⊗ℓ}` for generic `ℓ` and see if it works equally well / worse.
4. **Test CONJ-A more aggressively**: try a matroid where AHK hard-Lefschetz fails
   (there isn't one for the Chow ring proper, but maybe over char p? or for
   non-realizable matroids — Vamos, V_8, Pappus, Fano-in-char-2 etc.).
5. **Compare with the augmented Chow ring** of BHMPW.


## G. Maximally speculative connections

  **WILD-8 (categorification).** S = R ⊗ R^∨ is the **trace** of an `End`-bundle:
  Tr(End(V)) = End(V) ↔ V ⊗ V^∨. Hard Lefschetz on `S` ↔ a numerical statement
  about the **trace cohomology** of an action. Specifically, there's a (conjectural)
  Khovanov-Rozansky-style "matroid Khovanov homology" whose Euler characteristic is
  ELC, and whose underlying complex has `S` as a graded piece.

  **WILD-9 (cluster / total positivity).** The matrix of `L^d` in monomial basis
  is non-negative (entries are `d!`). Total positivity of large minors might be
  the right framework; this connects to **Lorentzian polynomials** (Brändén–Huh)
  via the determinant-positivity formulation.

  **WILD-10 (TT* equations).** In string-theory speak, `R ⊗ R^∨` is the "tt* bundle"
  of a Frobenius manifold. There's a natural connection on such bundles whose
  curvature is governed by **Lefschetz-type identities**. ELC may have a
  tt*-geometry interpretation.


## H. Bottom line for the project

The most promising structural targets to pursue:

  (a) **Prove CONJ-A**: `L^d : S_{-d} → S_d` is iso for `d ≥ 2` and every matroid.

  (b) **Prove the bigraded variant (C.5)**: there is a clean bigraded commutative
  ring `S' = R ⊗ R^∨_{apolar}` on which `L = ∑ x_i y_i` is an honest ring element
  and a Lefschetz statement is then natural.

  (c) **Identify the kernel** of `L : S_{-1} → S_1` for non-uniform matroids —
  it might be a known matroid invariant in disguise (broken-circuit module?
  Orlik-Solomon? KL-polynomial?).

  (d) **Test deletion-contraction** for the kernel/cokernel: a long-exact sequence
  in `S(M)`, `S(M \ e)`, `S(M / e)` would be a major structural advance.
