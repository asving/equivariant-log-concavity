# QLC Handoff — condensed state of the project

**Last updated:** 2026-05-25 (after the geometric proof framework session).

This document is the entry point for any future instance continuing this project. It assumes familiarity with the surrounding matroid combinatorics literature (AHK, Brändén–Huh, ALOGV, Karn–Wakefield, etc.).

For the **proven theorem (paving ELC)**, see `PAPER.md`/`PAPER.tex`/`PAPER.pdf`.
For the **journey**, see `notes/HISTORY.md` and notes 18–36 chronologically.
For the **detailed earlier exploration**, see `notes/archive/`.
For the **geometric proof framework**, see `notes/27` → `28` → `30` → `32`.
For the **Hall + matroid intersection proofs**, see `notes/33` → `34` → `35` → `36`.

## Proof status (2026-05-25 evening)

The project's main conjecture (PAPER §5.3) is now proven in:
- **Paving matroids**: all d≥2 bigrades (PAPER §4).
- **Any matroid at d ≥ m+1 bigrades** (notes/33, via Hall's marriage theorem).
- **Simple matroids at m=2 d=2 boundary** (n=6, rank=4) (notes/34, refined Hall via girth).
- **High-girth matroids at d=2 boundary** (girth > corank+1) (notes/36, alternative Hall proof).
- **Triangle = U(2,3) completely** (notes/28, geometric via Kähler HL on Bl_p((P^1)^3)).

**Open remaining:** d=2 boundary at m ≥ 3 for low-girth (girth ≤ corank+1) non-paving non-uniform matroids. Structural foundation laid: **X_m at d=2 boundary IS standard matroid intersection** Indep(M) ∩ Indep(M*) (notes/34), connecting to ALOV's Lorentzian polynomial machinery.

The remaining case is empirically verified extensively and well-characterized. Path forward: ALOV polynomial capacity adapted to give bipartite operator rank statements.

## Goal

Prove ELC for the f-vector of every matroid:

> For every loopless matroid `M` on `n` elements and every `m ≥ 0`, the virtual `Aut(M)`-representation `[f_{m+1}(M)]² − [f_m(M)] · [f_{m+2}(M)]` is effective (= a genuine representation, i.e., all multiplicities non-negative).

Here `[f_d(M)]` is the permutation representation of `Aut(M)` on size-`d` independent sets.

## What's been proven

### Three reductions (all clean, see `PAPER.md` §§2–3)

1. **ELC ⟺ Injectivity of `L`.** Define `R(M) := k[x_i]/(x_C : C ∈ Circ(M); x_i^2)`. Then `dim R(M)_d = f_d(M)` and `R(M)_d ≅ [f_d(M)]` as Aut(M)-rep. Set `S(M) := R(M) ⊗ R^∨(M)` (with R^∨ the graded dual). The Lefschetz operator `L := Σ x_i ⊗ x_i` is Aut(M)-equivariant. **ELC for f-vector of M ⟺ L is injective on each bigrade `(m, -d)` for `d ≥ 2`.**

2. **L injectivity ⟺ Orbit-wise bipartite injectivity.** `L` preserves orbits indexed by `(C, U) = (S∩T, S∪T)`, and each orbit's `L` is the natural bipartite incidence on `X_k(N) = {A ⊆ E(N) : |A|=k, A indep, E\A indep}` for the contracted-restricted minor `N := N(C, U)`.

3. **Reduces to:** for every minor `N` of `M` of the form `N = N(C, U)` with `|E(N)| = 2k+d`, `rank(N) ≥ k+d`, `d ≥ 2`, the operator `∂*: ℝ^{X_k(N)} → ℝ^{X_{k+1}(N)}` is injective.

### Main theorem (this session, see `PAPER.md`)

**For every paving matroid M (= every circuit has size ≥ rank), the X-bipartite incidence is injective at every applicable bigrade. Hence L is injective on S(M), and ELC of the f-vector holds for every paving matroid.**

**Proof sketch.** Induction over the CH set of `M = U_{r,n}(H)`:
- **Base case (`H = ∅`, uniform):** `X_k(U_{r,n}) = C(n, k)` and `∂*` is the boolean simplicial coboundary, injective for `k < n/2` by classical sl₂-Lefschetz.
- **Inductive step (add a collection F of new CHs simultaneously, when matroid axioms require multiple to be added together):** At the relevant bigrade, `X_{k+1}` is unchanged (since `r ≥ k+d ≥ k+2 > k+1`) and `|X_k|` decreases by exactly the number of new CHs whose complements lie in X_k (= 0 unless we're in the boundary case r = k+d). The bipartite incidence in the new matroid is a SUBMATRIX of the original (delete certain columns, no rows deleted), and full column rank is preserved since the original matrix's columns are linearly independent and any subset of linearly independent columns is still linearly independent.

The argument applies to sparse paving (add CHs one at a time) and non-sparse paving (axioms force multiple CHs to be added together) uniformly.

### Concrete partial result on Hall (was a stepping stone)

For `d > k`, Hall's condition `|N(S)| ≥ |S|` on the X-bipartite graph follows from double-counting: forward-degree ≥ `d`, back-degree ≤ `k+1`, ratio ≥ 1 when `d ≥ k+1`. (Documented in `notes/archive/14_hall_reduction.md`.) Hall was *initially* hoped to imply Theorem 4'-II, but that implication has a subtle gap for general 0/1 matrices (see `notes/archive/16_hall_reduction_correction.md`); the KW relaxation proof bypasses Hall entirely.

## What's open

**The full conjecture** (ELC for arbitrary loopless matroids) remains open. Empirically verified on > 2 × 10⁵ orbits across `M(K_n)` for `n ≤ 6`, Fano, NonFano, Pappus, NonPappus, Vámos, AG(3, 2), and the failing-Lemma-5 submatroids of `M(K_6)`. No counterexample known.

The technical obstruction: the KW-relaxation proof relies on circuit-hyperplanes (= circuits of size *equal to* the rank). For matroids with **smaller circuits** (e.g., `M(K_n)` for n ≥ 5, which has triangle-circuits of size 3 ≪ rank), this argument breaks: the "relax a CH" operation isn't naturally defined for smaller circuits.

## Open directions, ranked

### 1. Non-paving matroids — clean conjecture identified, proof open ⭐

**Failed reformulation attempt (2026-05-23, see `notes/22`).** Hoped to reduce ELC to a "Matroid Ideal Containment" conjecture via the Gui-Xiong equivariant Kähler package (arXiv:2205.05420). Specifically, we conjectured that our `L = Σ x_i ⊗ x_i` on `R(M) ⊗ R^∨(M)` was the descent of Gui-Xiong's `L_amb` on `Λ(V) ⊗ Λ(V*)` along the matroid projection. This **fails**: `L_amb` does not preserve the matroid ideal `I_M`. Concrete counterexample in `computations/verify_descent.py`. Our `L` on the matroid quotient is defined intrinsically (drops non-indep contributions), not as a descent. So the Gui-Xiong HL on the ambient does not transfer to ours.

**The X-restricted face ring problem remains open.** The clean statement is: for the matroid face ring `R(M) = k[x_i]/(x_C, x_i^2)`, does the Aut(M)-invariant linear form `ω = Σ x_i` act as a Weak Lefschetz Element on the X-restricted bigrading? Swartz 2002 (arXiv:math/0210376) gives *generic* WLP for matroid face rings; the specific/Aut-invariant version, restricted to X-balanced bigrades, remains the open question. Empirically holds across 200k+ orbits.

**Position in the literature:** Our conjecture rephrases cleanly as **"the Aut(M)-invariant linear form `ω = Σ x_i` is a Weak Lefschetz Element for the X-restricted face ring of `IN(M)`"** — the f-vector / matroid-face-ring analog of equivariant hard Lefschetz.

Three asymmetries are now clear:
- **Chow ring side: solved equivariantly** (Angarone-Nathanson-Reiner 2023, arXiv:2309.14312, Cor. 2.30): G-invariant Lefschetz element exists for `A(M)`. But `A(M)` carries Whitney numbers, not f-vector.
- **Face ring side: open** (Swartz 2002, arXiv:math/0210376): only generic WLP, no specific/equivariant version. **No improvement in 23 years.**
- **X-restriction: novel** — no published Lefschetz/Hodge result restricts to balanced indep bipartitions.

**Cautionary data:** Takahashi 2025 (arXiv:2501.13348) *disproves* SLP for graphic matroids' basis-generating-polynomial Gorenstein algebra. This is a different algebra from our `R(M)`, but warns that "Lefschetz on matroid-derived algebras" can fail in the graphic case. The X-restriction must be doing real structural work to rescue the symmetric form for non-paving (especially graphic) matroids.

**Three concrete approaches identified:**

**(A) Adapt ANR's Chow-ring proof to the face ring.** ANR use the BHMPW semi-small decomposition. The face ring is structurally different from the Chow ring but related. Highest reward, longest path.

**(B) ~~Gui-Xiong descent~~ — ruled out.** Tested 2026-05-23: Gui-Xiong's `L_amb` on `Λ(V) ⊗ Λ(V*)` does *not* preserve the matroid ideal `I_M`, so it does not descend to our `L` on `R(M) ⊗ R^∨(M)`. See `notes/22` and `computations/verify_descent.py`. Our `L` is intrinsically defined on the quotient, not inherited from the ambient.

**(C) Structural understanding of the X-restriction.** Why does the symmetric form succeed on the X-subspace when it fails on the full face ring? The X-restriction connects to matroid intersection (via complementation A ↔ E\A), so matroid-intersection-mixing literature (Anari-Liu-Vuong) may be relevant. Genuinely new mathematics likely.

### 2. Beyond paving: deletion-contraction induction

For arbitrary matroids `M`, one can attempt induction on `|E(M)|` via deletion `M\e` or contraction `M/e`. The challenge is that the X-bipartite incidence doesn't decompose cleanly under `\e`/`/e` — the X-sets transform non-trivially. A clean decomposition argument would resolve the conjecture in general.

### 3. Geometric realization (high-power) — landscape mapped 2026-05-23 (see `notes/24`)

**Decisive obstruction:** for non-uniform-or-rank-1 M, `IN(M)` is NOT a simplicial sphere, so `R(M)` lacks Poincaré duality. Hence **no smooth projective Y_M can satisfy H*(Y_M) ≅ R(M)** in general. The naive "find Y_M, apply HL" program is provably impossible as stated.

**Re-framing:** realize **R(M)|_X** (the X-restriction, where the bilinear form IS non-degenerate empirically) as a subspace/subquotient of the cohomology of a smooth projective variety, with Σx_i acting as ample. This is unexplored.

**Survey of matroid varieties (none realize f-vector except the last):**
- AHK Chow ring, BHMPW augmented Chow, EHL stellahedral, BEST permutohedral, Pagaria-Pezzoli, Binder singular cohomology — all realize **Whitney / Tutte / augmented Whitney** invariants, indexed by **flats**, not by independent sets.
- **Hausel–Sturmfels toric hyperkähler** (arXiv:math/0203096) — only known geometric realization with f-vector dimensions. Limitations: representable matroids only; generic linear system of parameters Θ (not symmetric Σx_i); non-compact.

**Three avenues investigated 2026-05-24, all blocked or misidentified:**

**(A) Embed R(M)|_X into AHK / BHMPW Chow ring — RULED OUT.** Hilbert-series dimensional check (`computations/test_chow_hilbert_vs_x.py`): |X_k| > dim A(M)_k for 11 of 12 test matroids at multiple bigrades. Structural reason: X-vector is **subset-indexed** (top degree n), every Chow ring is **flat-indexed** (top degree r or r-1). For n > 2r the X-vector's peak lies outside the Chow ring's support entirely. This rules out every flat-indexed matroid variety in the literature (AHK, BHMPW augmented, Pagaria-Pezzoli, EHL, BEST, Binder).

**(B) Hausel-Sturmfels symmetric Lefschetz — addresses wrong question.** H*(X^HK_M) = k[IN(M)]/Θ has **h-vector** dims (Stanley), not f-vector. Equivariant lift of "h-vector LC ⟹ f-vector LC" is non-trivial and not published.

**(C) New subset-indexed variety / non-Kähler Lefschetz theory.** The only subset-indexed cohomology realizing R(M) is the coordinate-subspace-arrangement complement / moment-angle manifold — these are non-compact / non-Kähler, so Hard Lefschetz doesn't directly apply. L²-cohomology or mixed-Hodge-structure approaches remain unexplored.

**Practical recommendation:** the geometric realization route is essentially closed for f-vector ELC in standard formulations. Realistic options: (i) pursue Schur-complement KNPV-style proof despite the depth-3 obstacle (`notes/23`); (ii) treat the paving theorem as the publishable result and let the non-paving case stand as an open question. See `notes/24` for full landscape.

**HL re-framing (2026-05-24, `notes/25`):** Verified that R(M)|_X satisfies Hard Lefschetz with the symmetric Aut-invariant operator ω = Σ x_i for 10 test matroids (`computations/test_hard_lefschetz_x.py`). LATER CORRECTED — see below.

**Geometric framework identified (2026-05-24, `notes/27-30`):** The geometric setting for R(M) is canonical and well-known: **R(M) = H*(U_M)** where `U_M = (P^1)^n \ matroid_coord_subspace_arrangement` (Goresky-MacPherson). The Lefschetz operator L = Σ x_i ⊗ x_i is *literally* the Aut(M)-invariant Kähler class on (P^1)^n descended to R(M) ⊗ R^∨(M) via the quotient by the matroid ideal.

**Triangle: complete geometric proof (`notes/28`).** Y = Bl_p((P^1)^3) (= wonderful compactification of (P^1)^3 minus the single matroid coord subspace = origin) is smooth projective Kähler. Classical Hard Lefschetz on Y. R(Triangle) = H*(Y) / (e) where e = exceptional class. The 4×4 matrix of mult ω̃ on H^2(Y) → H^4(Y) is block lower-triangular in (pullback / exceptional) decomposition, with the 3×3 pullback block = ∂* on R(Triangle)|_X. det of 4×4 = 2(3+ε) ≠ 0 (HL on Y) ⟹ det of 3×3 = -2 ≠ 0 ⟹ HL on R(Triangle)|_X.

**Scope correction (`notes/29, 30`):** The earlier "HL on R(M)|_X universally" claim was OVER-STRONG. Counterexamples:
- M(K_4 − e) (connected non-uniform, OUTSIDE d≥2 hypothesis): ∂*: X_2 → X_3 has kernel dim 1.
- Hexagon+chord (connected non-uniform, IN d≥2 hypothesis): ∂* INJECTIVE at hypothesis bigrade (m=2, d=3), but fails at non-hypothesis bigrade (m=3, d=1).

**The geometric proof template's scope is EXACTLY the project's conjecture scope.** For matroids in d≥2 hypothesis: HL on Y_M restricts to injectivity of ∂* on R(M)|_X at the relevant bigrades. For matroids/bigrades outside hypothesis: no inheritance guarantee.

**Remaining technical work:** for general matroids in d≥2 hypothesis, build wonderful compactification Y_M explicitly, identify R(M)|_X as Lefschetz-stable sub-piece of H*(Y_M), verify block-triangular inheritance. For Triangle: manifest. For larger M: concrete intersection theory work, not blue-sky.

**This is a viable proof framework for the project.** The geometric setting is canonical; the proof template is structurally aligned with the conjecture scope; only the explicit per-matroid verification is non-trivial.

### 4. Refute or refine the empirical conjecture

We have no counterexample, but the empirical verification has only covered matroids of rank ≤ 5 in any depth. Testing on `M(K_7)` (= 21 edges, rank 6), `PG(2, 3)` (= 13 points, rank 3), or randomly-generated matroids of larger rank could either further support or refute the conjecture.

## Tools and infrastructure

`computations/` contains all verification scripts.

**Core infrastructure:**
- `gpu_rank.py`, `sparse_rank.py` — matroid definitions, mod-p rank computation infrastructure.

**Verification of the proven paving theorem:**
- `verify_paper.py` — canonical regression test (1195 OK / 0 FAIL).
- `test_kw_relaxation.py` — verifies the inductive step.
- `test_paving_extension.py` — verifies the non-sparse-paving example from PAPER §4.4.

**Geometric proof framework (this session):**
- `verify_RM_geometric.py` — verifies R(M) = H*(arrangement complement).
- `triangle_blowup_HL.py` — explicit Lefschetz matrix on Bl_p((P^1)^3), Triangle proof.
- `wonderful_compactification_HL.py` — computes Lefschetz primitives, verifies X-Identification for Triangle.
- `test_hard_lefschetz_x.py` — HL on R(M)|_X across multiple matroids.
- `hexagon_chord_test.py` — verifies project conjecture on connected non-uniform matroid.
- `k4_minus_edge_geometric.py` — shows HL fails outside d≥2 hypothesis.

**Exploration / earlier attempts:**
- `test_block_decomp.py`, `test_block_decomp_recursive.py`, `inspect_depth3_failure.py` — Schur-complement attempt (failed at depth 3).
- `test_twistor_matching.py`, `test_x_factorization.py` — hyperkähler twistor matching (failed).
- `test_geom_candidates.py`, `test_compactification_hypothesis.py` — Hilbert series searches.
- `test_chow_hilbert_vs_x.py` — Chow ring vs X-vector comparison (Avenue 1 ruled out).
- `verify_descent.py` — Gui-Xiong descent failure verification.
- `aut_orbit_hall.py`, `hall_stress.py`, `verify_k23.py`, etc. — early Aut-orbit analyses.

All scripts are runnable from `/workspace-vast/asving/qlc/` with `python computations/<file>.py`. `.log` files in `computations/` are gitignored — regenerable from the scripts.

## Personal notes for the continuing instance

- The user is a research mathematician comfortable with AHK, BHMPW, Lorentzian polynomial machinery, and equivariant combinatorics. They prefer **clean proofs over hand-waving**, and **honest reporting of partial results and limitations**.
- Several methods were tried this session and *failed*; the journey is in `notes/HISTORY.md` and the archived notes. Don't re-invent these — read the history first.
- The proven theorem (sparse paving ELC) is **genuinely new** and worth publishing on its own. The full conjecture is a separate, harder goal.
- Compute is plentiful; don't be shy about running larger verification jobs to test conjectures.

## Where to pick up

If you have an hour:
- Read `PAPER.md` (or `PAPER.pdf`) for the proven paving theorem.
- Run `python computations/verify_paper.py` (canonical regression test, 1195 OK / 0 FAIL).
- Run `python computations/triangle_blowup_HL.py` for the complete Triangle geometric proof.
- Skim notes 27 → 28 → 30 → 32 for the geometric framework.

If you have a week:
- Build the wonderful compactification `Y_M` cohomology explicitly for **M(K_4)** or **hexagon+chord**. Verify the X-Identification Conjecture (= Lefschetz primitives of `H*(Y_M)` project onto `R(M)|_X`). See `notes/32` and `computations/wonderful_compactification_HL.py` for the Triangle case as a template.

If you have a research program:
- Develop the **matroid semi-small decomposition** for subspace-arrangement wonderful compactifications, parallel to BHMPW (arXiv:2002.03341) for the AHK Chow ring. This would complete the general geometric proof of the project's full conjecture. Estimated 6–12 months focused work.

## Session 2026-05-24/25 deliverables

The session focused on developing a geometric proof framework:

1. **Identified the canonical geometric setting**: `R(M) = H*(U_M)` for `U_M = (P^1)^n` minus matroid arrangement (Goresky-MacPherson 1988). The Lefschetz operator L is the Aut(M)-invariant Kähler class of `(P^1)^n` descended through the matroid ideal.

2. **Complete geometric proof for Triangle = U(2,3)**: HL on `R(Triangle)|_X` follows from classical Kähler HL on `Y = Bl_p((P^1)^3)` via block-triangular inheritance. Verified numerically in `computations/triangle_blowup_HL.py` and `wonderful_compactification_HL.py`.

3. **Scope correctly identified**: the geometric proof template applies exactly at d≥2 bigrade hypothesis. Outside this hypothesis, HL on R(M)|_X can fail — verified on M(K_4 − e) and hexagon+chord at non-hypothesis bigrades. **The framework scope matches the project's conjecture scope.**

4. **Structural insight**: the X-restriction is the Lefschetz-stable sub-piece of R(M) that rescues injectivity even when the f-vector decreases. For M(K_4) ⊕ U(4,4) at bigrade (4, 2): f_4=179 > 162=f_5 (no R(M) injectivity possible by dim count), but X_4=48 < 72=X_5 (∂* IS injective on the X-subspace). The X-restriction picks out the canonical kernel-avoiding subspace.

5. **Failed avenues honestly documented**: hyperkähler twistor matching (notes/26), Schur-complement at depth 3+ (notes/23), Gui-Xiong descent (notes/22). All recorded so future instances don't re-invent.

The session's net effect: the project has a viable geometric proof framework where before it had only combinatorial methods. The remaining work to complete the general proof is research-level but tractable, following the BHMPW playbook adapted to subspace arrangements.
