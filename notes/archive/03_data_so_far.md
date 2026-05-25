# Data so far + interpretation

## Test matroids and outcomes

| Matroid              | f-vector                        | hard-L at d≥2 | d=1 ker = coker |
|----------------------|---------------------------------|---------------|-----------------|
| U_{1,2}              | (1,2)                           | trivial       | 0               |
| U_{2,3}..U_{4,7}     | uniform                         | **ISO**       | 0               |
| M(K_4)               | (1,6,15,16)                     | **ISO**       | **6**           |
| Fano                 | (1,7,21,28)                     | **ISO**       | **21**          |
| NonFano (F_7^-)      | (1,7,21,29)                     | **ISO**       | **15**          |
| U_2 ⊕ U_2 ⊕ U_2      | (1,6,12,8) (three parallel prs) | **ISO**       | **0** ← !       |

**Pending**: Pappus, Vamos V_8, AG(3,2). v2 still running on Pappus (large).

## Key observations from v3

### 1. The d=1 kernel is NOT a "circuit phenomenon"

The matroid `U_2 ⊕ U_2 ⊕ U_2` (= three disjoint 2-circuits) has plenty of circuits but
**no d=1 kernel**. By contrast, M(K_4) has no parallel pairs (no 2-circuits) but
*does* have a 6-dim kernel.

So the d=1 kernel correlates with **circuits of size ≥ 3** (or "triangles" / "lines"),
not with circuits in general. This suggests: the d=1 kernel detects **rank-2 flats
of size ≥ 3** ("non-trivial lines" — points, parallel classes, *plus* multi-point lines).

  **CONJ-B.** `dim ker(L : S_{-1} → S_1) = ∑_F (|F| - 2)` summed over rank-2 flats `F` of `M`? Or some Whitney number?

Check:
  - M(K_4): rank-2 flats are pairs of distinct edges (= a single rank-2 flat in the matroid
    is two edges that span a rank-2 set; the closed rank-2 flats of M(K_4) are exactly
    the *bonds* — wait, this is graphic matroid; rank-2 flats of M(K_4) are 2-element
    indep sets, all `C(6,2)=15`? Hmm, but a *rank-2 flat* is a maximal rank-2 set,
    which means a flat F with rk(F)=2 and F = closure(F)).
    In K_4, two edges sharing a vertex span 2 in M(K_4) and their closure is the
    triangle they're in (if any). K_4 has 4 triangles. Each triangle is a rank-2 flat
    of size 3.

    Rank-2 flats of M(K_4): every triangle (4 of them, size 3) + every pair of non-adjacent
    edges (= matching pair, closure is just those 2 edges, size 2). K_4 has 3 perfect
    matchings of size 2, contributing 3 rank-2 flats of size 2.

    So flats of rk 2: 4 of size 3 + 3 of size 2 = 7 total. Sum of (|F| - 2) = 4·1 + 3·0 = 4.
    But ker dim = 6. So CONJ-B (above formula) **fails** at M(K_4) — gives 4, not 6.

  Hmm. Try: number of rank-2 flats? 7. No, dim = 6.
  Number of edges? 6 = n. So **ker dim = n** for M(K_4).
  Fano: n = 7, ker dim = 21 = `C(7,2)` (or 3·7 — Fano: each pt on 3 lines, total flag = 21).
  NonFano: n = 7, ker dim = 15.

  Try: ker dim = # circuits? Fano has 7 size-3 circuits + circuits of size 4. Actually
  Fano has only size-3 lines (7 of them); 4-circuits are all 4-subsets not containing
  a line (= 35 - 7 = 28 bases, the rest 35 - 28 = 7 → wait, 4-subsets containing exactly
  one 3-line is also dependent → these are circuits of size 4). Hmm complicated.

  Try: ker dim = # rank-2 flats of size ≥ 3 weighted by (|F| - 1):
   - K_4: 4 triangles, each |F|=3, weighted (|F|-1) = 2. Total 4·2 = 8. ≠ 6.

  Try: ker dim = ∑_{F rank-2 flat, |F|≥3} f_1(F|_M restricted) - 2 ... .

  **TODO**: Compute kernel dim for one more matroid and triangulate the formula. Try
  Pappus (rank 3, 9 elts, 9 lines of size 3): ker dim should be predictable if a pattern
  exists.

### 2. Random diagonal c_i still gives hard Lefschetz

`L_c = ∑ c_i (x_i ⊗ x_i)` with random *positive* integer c_i (different per i!) still
gives `L_c^d` iso at d ≥ 2 on M(K_4), Fano, NonFano. So the conjecture is:

  **For any tuple c = (c_i) of nonzero scalars, L_c^d : S_{-d} → S_d is iso for d ≥ 2.**

This is a "Zariski-open" statement on the c-space.

### 3. Generic two-form a ⊗ b WITH a ≠ b FAILS

The generic Lefschetz `L_{a,b} = (∑ a_i x_i) ⊗ (∑ b_j ∂_j)` is **rank 1** as a tensor,
and gives `L_{a,b}^d : rank 1` — which is far below the expected source dim.

**Interpretation.** `L = ∑ x_i ⊗ x_i` (or `L_c = ∑ c_i x_i ⊗ x_i`) is a **rank-n,
"positive"** tensor (sum of squares of rank-1 tensors `x_i ⊗ x_i`). It is the
*Casimir* / *diagonal* element — and is **completely positive** as a quantum-channel
analog (T_L = ∑ K_i • K_i^* with K_i = mult. by x_i, Kraus form).

A generic two-form `a ⊗ b` is rank 1 as a tensor; the CP-map analog has a single
Kraus operator, which can't have full spectral rank.

**Sharper conjecture.** Hard Lefschetz at d ≥ 2 holds for **any sum-of-squares
tensor** `∑_α ℓ_α ⊗ ℓ_α` (with `ℓ_α ∈ R_1`, sum has enough terms — at least `n`?
or maybe at least `f_2 / f_1`?). Like Lorentzian / hyperbolic polynomial setups.

### 4. The d=1 kernel basis elements (for NonFano)

From v3 output, sample kernel element:

  k_2 = -(x_{03} ⊗ y_{456}) - (x_{04} ⊗ y_{356}) + (x_{05} ⊗ y_{346}) + (x_{06} ⊗ y_{345})

Note: the **union of all indices** is {0,3,4,5,6}. This is the union of the two Fano lines
(0,3,4) and (0,5,6) through 0. The signs alternate based on which 2-set is contained.

Pattern (tentative): for each "near-pencil" P = L_1 ∪ L_2 of two lines sharing a
common point p, we get a kernel element supported on pairs (S, T) with S ⊂ P, T ⊂ P.

  **CONJ-C.** The kernel of L : S_{-1} → S_1 has a basis indexed by **rank-2 flags**
  of `M` (pairs of nested flats, or related). The basis elements are explicit "boundary"
  elements.

### 5. Direct-sum behavior

For `M = M_1 ⊕ M_2`: indep sets are S_1 ⊔ S_2. So `R(M) = R(M_1) ⊗ R(M_2)`. Likewise
`R^∨(M) = R^∨(M_1) ⊗ R^∨(M_2)`. And `S(M) = (R(M_1) ⊗ R(M_2)) ⊗ (R^∨(M_1) ⊗ R^∨(M_2))
≅ S(M_1) ⊗ S(M_2)` via the swap of middle factors. The Lefschetz
`L(M) = ∑_{i ∈ [n_1] ⊔ [n_2]} x_i ⊗ x_i = L(M_1) ⊗ id + id ⊗ L(M_2)`.

So **(S(M), L(M)) is the tensor product of (S(M_1), L(M_1)) and (S(M_2), L(M_2))**.

Hard Lefschetz on `(S(M), L(M))` at level d follows from hard Lefschetz on the tensor
factors only via a **delicate** argument — the standard hard-Lefschetz tensor-product
result needs sl_2-symmetry of each factor. This is essentially the **Lefschetz package
on products** of Kähler manifolds.

But the data shows: `U_2 ⊕ U_2 ⊕ U_2` (a direct sum of 2-uniform matroids) has hard
Lefschetz at every d (including d=1!). Each `U_{1,2}` factor has hard Lefschetz at d=1
trivially (only d=1 exists). So the tensor product also gives hard Lefschetz at d=1
— matching observation 1 above that d=1 kernel needs *non-direct-sum* structure
(specifically rank-2 lines, not parallel pairs).

  **CONJ-D.** Hard Lefschetz at all `d ≥ 1` holds for a matroid M iff M is a
  direct sum of uniform matroids (= no "non-trivial line" of length ≥ 3).

  Equivalently: **L : S_{-1} → S_1 is iso ⟺ M is a "U-direct-sum"**.

Equivalent reformulation: a matroid is a direct sum of uniform matroids iff it has
no rank-2 flat of size ≥ 3 (equivalently, no "non-trivial parallel-class-free line").
These are sometimes called "loopless-coloopless paving-free direct-sums".

  **TODO**: Test against Pappus, Vamos, AG(3,2). Also test small direct sums.
