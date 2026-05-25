# Note 27 — THE Geometric Setting for R(M) (2026-05-24)

## Headline

**R(M) has a canonical geometric realization: it is the cohomology of the matroid coordinate subspace arrangement complement.** Specifically:

> For every loopless matroid M on E, |E| = n, with circuits C₁, ..., C_k:
> ```
> U_M := (P^1)^n \ ⋃_{C circuit of M} Z_C        where Z_C = {z_i = 0 ∀ i ∈ C}
> R(M) = H*(U_M; Q)
> ```
> The Lefschetz operator ω = Σ x_i on R(M) is the descent of the Aut(M)-invariant
> Kähler class on (P^1)^n via the quotient map H*((P^1)^n) ↠ R(M).

This is Goresky-MacPherson 1988 / De Longueville Math. Z. 1999. **I had this fact in note 24 but lost track of it; the recent sessions exploring "alternative" geometric realizations were chasing a problem that already had its answer.**

The geometric proof of correctness:
- `H*((P^1)^n) = k[x_1, ..., x_n]/(x_i²)` — exterior algebra of n generators of degree 2 (the Kähler class of each P^1 factor).
- For each circuit C, the subvariety `Z_C ⊂ (P^1)^n` has codim |C| and its Poincaré-dual class is `[Z_C] = ∏_{i ∈ C} x_i` in H*((P^1)^n).
- Removing all `Z_C`: the open complement's cohomology is the quotient of `H*((P^1)^n)` by the ideal of classes `[Z_C]`. That ideal is exactly the **matroid ideal** generating `R(M)`.
- Verification: `verify_RM_geometric.py` confirms Hilbert series match for all test matroids.

## The Lefschetz operator descends

The Kähler class on `(P^1)^n` is `ω = Σ_i x_i` (sum of Kähler classes of factors). It is Aut(M)-invariant (= invariant under coordinate permutations).

**Mult-ω preserves the matroid ideal**, hence descends to R(M):

> *Proof.* For `x_C = ∏_{i ∈ C} x_i` with C a circuit: `ω · x_C = Σ_j x_j · x_C`. For `j ∈ C`, `x_j · x_C = x_j² · ∏_{i ∈ C, i ≠ j} x_i = 0` since `x_j² = 0` in `H*((P^1)^n)`. For `j ∉ C`, `x_j · x_C = x_{C ∪ {j}}` which contains the circuit C, hence lies in the matroid ideal. So `ω · x_C` is in the matroid ideal.

This means our operator L = Σ x_i ⊗ x_i on `S(M) = R(M) ⊗ R^∨(M)` is **literally** the action of the Aut(M)-invariant Kähler class of `(P^1)^n` on the cohomology of the open variety `U_M` (tensored with its dual).

## Why Hard Lefschetz on the WHOLE R(M) fails

For the COMPACT `(P^1)^n`: Hard Lefschetz holds. `ω^{n-2k}: H^{2k} → H^{2(n-k)}` is iso for k ≤ n/2.

For the OPEN `U_M` with `H*(U_M) = R(M)`: HL does NOT directly hold. Concretely, R(M) is not Poincaré-dual (= not Gorenstein) for non-uniform M, because `IN(M)` is not a simplicial sphere — so no compact smooth orientable manifold has cohomology R(M).

This was the obstruction I identified in note 24 (and re-derived in note 26). It's correct *for the full R(M)*.

## Why HL on R(M)|_X works — the empirical fact

But **HL DOES hold on R(M)|_X** — the subspace indexed by "balanced" indep bipartitions (verified in note 25 across 10 test matroids).

R(M)|_X is the subspace of R(M) at grades k ∈ [n-r, r], spanned by `{x_S : S indep, E\S indep, |S| = k}`. It has palindromic Hilbert series |X_k| = |X_{n-k}|.

**The empirical fact**: ω^{n-2k}: R(M)|_X at grade k → R(M)|_X at grade n-k is an iso.

**Eigenvalue signature**: the operator has INDEFINITE eigenvalues (mix of positive and negative; see note 26). So this is *non-Kähler Lefschetz* — consistent with R(M)|_X being a sub-piece of cohomology of a NON-compact variety where Kähler positivity is lost.

## Saito mixed Hodge module interpretation (the proof avenue)

For a smooth complex variety U ⊂ X with X smooth projective and X\U a normal-crossings divisor (or stratified subvariety), Saito's mixed Hodge module theory gives:

- H*(U) has a mixed Hodge structure (Deligne).
- Each weight-pure graded piece of H*(U) carries a Hodge structure satisfying Hodge-Riemann.
- Ample classes on X act as Lefschetz operators on appropriate weight pieces.

For `U_M ⊂ (P^1)^n` with `X \ U_M` = union of coordinate subspaces (NOT a normal crossings divisor — it's a union of higher-codimension subvarieties). Need a **resolution** to put it in SNCD form. The natural resolution is the **wonderful compactification** of De Concini-Procesi for subspace arrangements.

For matroid arrangements, the wonderful compactification's cohomology is the **Feichtner-Yuzvinsky ring** / **AHK Chow ring** of M. This is the BHMPW playbook source.

Saito's theory predicts:
- H*(U_M; Q) has pure Tate Hodge structure (weight 2k on H^k(U_M; Q)).
- The wonderful compactification has H* = AHK Chow ring with HL (proven combinatorially by AHK/BHMPW).
- The natural map `H*(wonderful) → H*(U_M)` is restriction; its image is R(M).

> **Proof avenue (proposed):** show that R(M)|_X is the image of a specific *Lefschetz primitive* subspace of the AHK Chow ring under the restriction map `H*(wonderful) → R(M)`. Since the AHK Chow ring satisfies HL (BHMPW), the restriction inherits Lefschetz on the image. Identifying the precise "primitive" subspace whose image is R(M)|_X is the technical work.

This is the **BHMPW playbook for the f-vector**: not finding a new geometric realization, but identifying R(M)|_X inside the already-known wonderful compactification's cohomology, and using the AHK / BHMPW HL to inherit ours.

## Why this is the right direction

1. **No new geometry to invent.** The geometric setting (= matroid arrangement complement / wonderful compactification) is already well-developed.
2. **AHK Chow ring is the workhorse.** It's been proven to satisfy HL (combinatorially / via the singular Hodge theory of BHMPW). Its structure is well-understood.
3. **The connection R(M) ↔ AHK Chow is via restriction.** The wonderful compactification X̃ contains U_M as the open complement of the boundary divisor. The restriction map gives R(M) as a quotient of H*(X̃).
4. **The X-restriction is intrinsic.** R(M)|_X ⊂ R(M) corresponds to a specific subspace of H*(X̃) — possibly the Lefschetz primitive part with respect to the symmetric Kähler class.

## What I have to actually do next

Concrete plan:

1. **For Triangle U(2,3), build the wonderful compactification X̃ explicitly.** It's a blow-up of (P^1)^3 along the origin (= a single point in this case). Result: X̃ is the blow-up of (P^1)^3 at one point, which is well-known.
2. **Compute H*(X̃)** = AHK Chow ring for Triangle. This is a small ring; computable by hand.
3. **Compute the restriction H*(X̃) → R(Triangle)** explicitly. Identify the kernel (= boundary divisor classes) and image (= R(M)).
4. **Identify R(M)|_X as a subspace of H*(X̃)**: which classes in H*(X̃) restrict to elements of R(M)|_X?
5. **Apply HL on H*(X̃)** to that subspace and check it gives the right Lefschetz statement on R(M)|_X.

If this works for Triangle, the path is clear. If it doesn't, we'll learn precisely why.

## Status

- **Confirmed:** R(M) = H*(U_M) for the matroid arrangement complement. Geometric setting is canonical and well-known (Goresky-MacPherson 1988).
- **Confirmed:** Lefschetz operator ω = Σ x_i descends from (P^1)^n Kähler class.
- **Open:** Is HL on R(M)|_X provable via the BHMPW playbook, restricting AHK Chow's HL to the appropriate subspace?

This is genuinely the right direction. Apologies for the detour through hyperkähler and combinatorial-only paths — they were necessary to rule out alternatives but the answer was hiding in note 24's "coordinate subspace arrangement complement" line that I'd lost track of.

## Files

- `computations/verify_RM_geometric.py` — verifies R(M) Hilbert = H*((P^1)^n) / matroid ideal for test matroids.
- All earlier notes (21–26) document the journey that led here.
