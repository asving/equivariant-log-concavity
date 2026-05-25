# Final picture (after the big GPU run)

## Headline

**CONJ-A is FALSE.** Hard Lefschetz `L^d : S_{-d} → S_d` is NOT iso in general. Counterexamples:

| Matroid   | d | deficit |
|-----------|---|---------|
| M(K_5)    | 2 | 180     |
| M(K_6)    | 2 | 35610   |
| M(K_6)    | 3 | 4500    |

**The user's WEAKER conjecture survives.** Injectivity of `L : S_{-d} → S_{-d+2}` for d≥2 holds in every test, including M(K_5) and M(K_6).

## Per-internal-degree breakdown

`L^d` on `S_{-d} → S_d` splits across internal-degree blocks `m = |S|`. Each block
maps `R_m ⊗ R^∨_{-(m+d)} → R_{m+d} ⊗ R^∨_{-m}` (dimensions match: `f_m · f_{m+d}`).

**M(K_5) `L^2` deficit 180 is fully localized at m=2:**
- m=0 (size 45→45): ISO
- m=1 (size 1100→1100): ISO
- m=2 (size 5625→5625): rank 5445, deficit 180   ←  the *entire* failure lives here
- (m=3, m=4 trivial)

**M(K_6) `L^2` deficit 35610:**
- m=0 (105→105): ISO
- m=1 (6525→6525): ISO
- m=2 (113400→113400): deficit 1170
- m=3 (563760→563760): deficit 34440

**M(K_6) `L^3` deficit 4500:**
- m=0: ISO
- m=1: ISO
- m=2 (136080→136080): **deficit exactly 4500**

Curiously, this 4500 equals `f_2² − f_1·f_3 = 11025 − 6525 = 4500` — the level-2 LC defect of M(K_6)'s f-vector. This might be coincidence or genuine; would need to verify the analogous identity at other (M, d, m) triples.

## The user's INJ conjecture: status table

| Matroid       | d=2 INJ | d=3 INJ | d=4 INJ | d=5 INJ |
|---------------|---------|---------|---------|---------|
| M(K_4)        | ✓       | ✓       | -       | -       |
| M(K_5)        | ✓       | ✓       | ✓       | -       |
| M(K_6)        | ✓       | ✓       | ✓       | ✓       |
| M(K_7)        | testing | -       | -       | -       |
| Fano          | ✓       | ✓       | -       | -       |
| Pappus        | ✓       | ✓       | -       | -       |
| Vamos V_8     | ✓       | ✓       | ✓       | -       |
| AG(3,2)       | ✓       | ✓       | ✓       | -       |

ALL test cases support the user's conjecture.

## ELC consequence

For each matroid in the table, **injectivity of `L : S_{-2} → S_0` directly proves ELC of the f-vector**:

> For each `m`, the `Aut(M)`-rep `[f_{m+1}]² − [f_m][f_{m+2}]` is **effective**
> (an honest virtual rep, not just having non-negative dim).

This is because the map decomposes per internal-degree-m block:
  `L : R_m ⊗ R^∨_{-(m+2)} → R_{m+1} ⊗ R^∨_{-(m+1)}`
is `Aut(M)`-equivariant; injectivity gives `[f_m]·[f_{m+2}] ↪ [f_{m+1}]·[f_{m+1}] = [f_{m+1}]²` as Aut(M)-reps. Cokernel = `[f_{m+1}]² − [f_m]·[f_{m+2}]` is effective.

**Conclusion: ELC is established for the f-vectors of M(K_4) through M(K_6) (at least) by direct computation.** This is a genuine result.

(Note: ELC for M(K_n) under the S_n action is presumably already covered by representation-stability arguments in MMPR's framework — but those work on OS algebras, not the f-vector ring. Our independent calculation gives a different proof path.)

## Hybrid CONJ-A' for the induction

We checked `(M\e, M/e)` hybrid pairs on `M = M(K_5)` (all 3 edges-up-to-symmetry) and on `M = Fano`. For each:

- d=1 hybrid: sometimes fails INJ (kernel of 12 for K_5 hybrid; for Fano, holds).
- **d=2, d=3 hybrid: INJ ✓ in every case tested.**

So CONJ-A' (hybrid INJ at d≥2 on all `M_2 ≼ M_1` pairs) is alive and supported by data. This is the right object for an inductive proof.

## What we now know about the geometric picture

The fact that CONJ-A fails *at intermediate internal degrees* but the **single-step L injectivity** holds is highly informative:

- Hard Lefschetz iso at d=2 would mean `L^2` on the m-block is an iso between two `f_m · f_{m+2}`-dim spaces. The deficits are positive (= the "primitive" part of the Lefschetz decomposition at that bigrade).
- These primitives **do not obstruct injectivity of L (single step)**, because L composes with another L to get L^2, and L is INJ on the m-source, while L can have a kernel "downstream" on `S_0`.

So the right object is the **Lefschetz decomposition** of S, not just hard Lefschetz. Decompose `S = ⊕ L^k · P_j` where `P_j` is primitive at bigrade `-j`. Each `P_j` carries a non-degenerate bilinear pairing (Hodge-Riemann). The user's INJ conjecture is then a statement about the primitive pieces — much cleaner geometrically.

**Revised geometric framing:** the structure on `S(M)` is **not** quite a hard-Lefschetz package (CONJ-A fails). It IS a "*weak Lefschetz package*" with `L` injective (the user's conjecture), and the failure of hard-Lefschetz is governed by the **primitive classes** at each internal degree. These primitives are the **new matroid invariants** — they detect, e.g., the 180-dim space at M(K_5)'s m=2 piece.

Computing the structure of these primitives across matroids is the next natural step — they should have a clean combinatorial / representation-theoretic description.

## Strategic next steps (revised)

1. **Prove user's INJ conjecture inductively via CONJ-A' on hybrid pairs.** Test hybrid INJ at d≥2 on more `(M_1, M_2)` to ensure CONJ-A' holds across the relevant cases.

2. **Decompose the primitive classes**: for `M(K_5)` at `m=2, d=2`, the 180-dim space is an `S_5`-rep. Find which irreps. This is the "new matroid invariant" — likely related to KL polynomial or top-heavy data.

3. **Test M(K_7)** if compute permits; otherwise larger Vamos-type matroids of rank 5+.

4. **The doubled Lorentzian polynomial approach**: most likely path to a clean proof. The "matrix-tree-like" expression for our `L^d` matrix is closely related to Hessians of `f_M(z) ⊗ f_M(z)`, and Brändén-Huh-style techniques may give INJECTIVITY (not iso!) directly.
