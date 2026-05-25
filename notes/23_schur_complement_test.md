# Note 23 — Schur-complement / deletion-contraction test (2026-05-23)

## TL;DR

**The deletion-contraction block-triangular decomposition is structurally clean and works perfectly at the first level. But naive "induction via diagonal blocks alone" breaks at recursion depth 2–3: the off-diagonal `+e` block is structurally essential, and the recursion descends into paired operators that are genuinely not injective. The KNPV-style Schur-complement bookkeeping is therefore non-trivial, not an off-the-shelf reduction.**

## Setup

For a matroid `N` on ground set `E`, the X-bipartite operator `∂* : ℝ^{X_k(N)} → ℝ^{X_{k+1}(N)}` is what we need to prove injective.

**Block decomposition by `e ∈ E`.** Partition `X_k(N) = X_k^{no e} ⊔ X_k^{has e}`. Then `∂*` has block-lower-triangular form
```
   ⎡ A   0 ⎤   ← X_{k+1}^{no e}
   ⎣ B   C ⎦   ← X_{k+1}^{has e}
```
where
- `A` = `∂*_{(N\e, N/e)}` at grade `k` (paired X-bipartite on the deletion/contraction pair),
- `C` = `∂*_{(N/e, N\e)}` at grade `k-1` (paired X-bipartite on the swapped pair),
- `B` = "add `e`" map sending `X_k^{no e} → X_{k+1}^{has e}`.

The natural "paired" generalization: for any two matroids `P, Q` on a common ground set `E`, define
```
   Y_k(P, Q) := {A ⊆ E : |A|=k, A indep in P, E\A indep in Q}.
```
Then `Y_k^{no e}(P, Q) = Y_k(P\e, Q/e)` and `Y_k^{has e}(P, Q) = Y_{k-1}(P/e, Q\e)`.

The recursion is well-defined on paired operators.

## Level-1 empirical result (clean)

`computations/test_block_decomp.py`. Tested on non-paving matroids constructed by direct-summing a small non-paving piece with `U_{r,r}` (free elements) to lift rank above `|E|/2`:

| Matroid                          | Bigrades tested              | Diagonal blocks injective for every `e`? |
|----------------------------------|------------------------------|------------------------------------------|
| Triangle ⊕ U_{2,2} (5 elts)      | (k=1, d=3)                   | ✓                                        |
| Triangle ⊕ U_{3,3} (6 elts)      | (k=1, d=4), (k=2, d=2)        | ✓                                        |
| Triangle ⊕ U_{4,4} (7 elts)      | (k=1, d=5), (k=2, d=3)        | ✓                                        |
| Triangle ⊕ U_{5,5} (8 elts)      | (k=1, d=6), (k=2, d=4), (k=3, d=2) | ✓                                  |
| M(K_4) ⊕ U_{3,3} (9 elts)        | (k=3, d=3)                    | ✓                                        |
| M(K_4) ⊕ U_{4,4} (10 elts)       | (k=3, d=4), (k=4, d=2)        | ✓                                        |

At the **first** level of decomposition, **both diagonal blocks are individually injective for every choice of `e`**. This is much stronger than what we need (it's a sufficient, not necessary, condition for the full operator's injectivity).

## Level-3 failure (the Schur-complement penalty)

`computations/test_block_decomp_recursive.py`, `computations/inspect_depth3_failure.py`.

Recursing deeper (= decomposing the smaller paired operators in the same way), we hit **non-injective sub-operators** at depth 3.

Concrete example (Triangle ⊕ U_{3,3}, depth-3 trace, decomposing by `e=0, 0, 1` in succession):

```
Depth 2 pair (P_2, Q_2) on |E|=4, ∂* at k=2:
    Y_2 = {{0,1}, {0,2}, {0,3}},  Y_3 = {{0,1,2}, {0,1,3}, {0,2,3}}
    Matrix:
        ⎡1 1 0⎤
        ⎢1 0 1⎥                    rank 3 — INJ
        ⎣0 1 1⎦

Depth 3 sub-block ∂*_{no e=1} (the "delete-contract" branch):
    Y_2^{no 1} = {{0,2}, {0,3}},   Y_3^{no 1} = {{0,2,3}}
    Matrix: [1, 1]                    rank 1 — NOT INJ (kernel dim 1)
```

The depth-2 operator IS injective. But its top-left block (the depth-3 "no-e" paired operator) is NOT.

**Mechanism.** Reorganize the depth-2 matrix into block form with the new order [no e=1 | has e=1]:
```
                       no_1 cols     has_1 col
                       {0,2} {0,3}   {0,1}
    no_1 row {0,2,3}:    1     1       0          ← A = [1,1] (rank 1, KER = span (1,-1))
    has_1 rows:          1     0       1          ← B = ⎡1 0⎤   C = ⎡1⎤
                         0     1       1                ⎣0 1⎦       ⎣1⎦
```

Block A has kernel `v = (1, -1)` (the column kernel: the formal difference `{0,2} − {0,3}` in `X_k`).

Block C has image span `{(1, 1)}` (the diagonal). The kernel of A maps under B to `B(1,-1) = (1,-1)`, which is **transverse to image C**. The full operator stays injective only because `B · ker(A) ∩ image(C) = {0}`.

This is the **Schur-complement structure**: the full matrix has full column rank not because diagonal blocks individually do, but because the off-diagonal `B` lifts `ker(A)` into the cokernel of `C`.

## Implications

1. **The block decomposition itself is correct and structural.** This is a real reduction of a single-matroid claim to a paired-matroid claim.

2. **A clean "induction via diagonal-block injectivity" does NOT close.** Diagonal blocks fail injectivity at depth 3+; the off-diagonal `+e` map is doing essential work.

3. **A genuine Schur-complement proof would have to track the (A, B, C) triple inductively** — proving that `B · ker(A) ∩ image(C) = {0}` is preserved under deletion-contraction. This is exactly the KNPV-style bookkeeping (matrix modification under one-element changes), but adapting it to **paired X-bipartite** operators is non-trivial work and we have no theorem yet.

4. **The recursion descends into "non-diagonal pairs" `(P, Q)` with `P ≠ Q`** that don't have an obvious matroid-theoretic interpretation. We are working in the space of **pairs of matroids on a common ground set**, where the relevant operator is `∂*_{P,Q} : Y_k(P, Q) → Y_{k+1}(P, Q)`. Empirically these operators sometimes ARE injective, sometimes NOT (the depth-3 failure). The "good" pairs form some structured subset; identifying it cleanly is open.

## Bottom line

The deletion-contraction approach is not a dead end, but it requires substantially more machinery than the diagonal-block argument alone provides. A KNPV-style Schur complement proof would need to:
- Formalize the invariant `B · ker(A) ⊆ X_{k+1}^{has e} \ image(C)`.
- Show this invariant is preserved under all deletion-contraction operations.
- Verify the base case for small ground sets.

This is comparable in difficulty to the original conjecture, but with the advantage that it has been REDUCED to a statement about pairs of matroids, which is a more flexible category for induction.

The verification scripts:
- `test_block_decomp.py` — verifies first-level diagonal-block injectivity (clean PASS).
- `test_block_decomp_recursive.py` — verifies recursion (FAILS at depth 3 for non-trivial bigrades).
- `inspect_depth3_failure.py` — dissects the failure mechanism.
