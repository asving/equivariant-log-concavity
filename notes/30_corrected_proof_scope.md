# Note 30 — Geometric proof template: corrected scope matches project conjecture (2026-05-24)

## TL;DR

The hexagon+chord matroid (genuinely connected, non-uniform, in the d≥2 bigrade hypothesis) gives the cleanest empirical verification yet:

- **∂*: X_2 → X_3 injective** at the hypothesis bigrade (m=2, d=3). ✓
- **∂*: X_3 → X_4 NOT injective** at the non-hypothesis bigrade (m=3, d=1). ✗
- Hence HL on R(M)|_X overall fails, but the project's conjecture holds.

This is a **structural alignment**: the geometric proof template inherits injectivity at exactly the bigrades the project conjectures.

## The matroid

M = M(G) where G = hexagon 0-1-2-3-4-5-0 with chord (0, 3).

- n = 7 edges, rank = 5.
- Circuits: 2 four-cycles ({e_0, e_1, e_2, e_6} and {e_3, e_4, e_5, e_6}) and 1 six-cycle (the hexagon).
- Connected (G is 2-edge-connected).
- Non-uniform (has size-4 circuits, less than rank).
- In d≥2 bigrade hypothesis: rank 5 > (n+2)/2 = 4.5. Valid bigrades (m=2, d=2), (m=2, d=3).

X-vector: (0, 0, 15, 33, 33, 15, 0, 0) at grades 0..7. Palindromic. Total 96.

## Empirical results (`computations/hexagon_chord_test.py`)

| Operator | Source dim | Target dim | Rank | Status |
|---|---|---|---|---|
| ∂*: X_2 → X_3 | 15 | 33 | 15 | **INJECTIVE** ✓ |
| ∂*: X_3 → X_4 | 33 | 33 | 32 | ker=1 (NOT inj) |
| ∂*: X_4 → X_5 | 33 | 15 | 15 | (surjective, not inj — expected) |
| ∂*³: X_2 → X_5 | 15 | 15 | 14 | NOT ISO — HL fails |

## What this confirms

1. **Project's conjecture is alive.** ∂*: X_m → X_{m+1} injective at the d≥2 hypothesis bigrade. For M(hexagon+chord): the unique relevant bigrade is (m=2, d=3), and ∂* IS injective there. ✓

2. **My over-broad claim from notes/25 is wrong.** "HL on R(M)|_X for all matroids" fails on connected non-uniform matroids when symmetric pairs cross the bigrade-hypothesis boundary.

3. **The geometric proof template's scope is exactly the project's conjecture scope.** Inside the bigrade hypothesis: HL on Y_M restricts to injectivity of ∂*. Outside: classes that were "carrying" injectivity on Y_M get dropped under the restriction.

## The corrected proof template

**What HL on Y_M provides:**
- Mult ω̃: H^{2k}(Y_M) → H^{2(k+1)}(Y_M) is injective for k < complex_dim(Y_M)/2 (= classical Kähler Hard Lefschetz, lower half is the "weak Lefschetz" / "injectivity" half).
- Iso between symmetric pairs (the full HL statement).

**What we inherit on R(M)|_X:**
- For the d≥2 bigrade hypothesis (= m ≤ (n-2)/2 AND m+d ≤ rank with d=n-2m): ∂* injective at these specific bigrades.
- NOT iso between symmetric pairs (since R(M)|_X may not be Lefschetz-stable across all grades).

**Why the restriction preserves d≥2 injectivity:**
Block-triangular argument: at the relevant grades, the X-restricted subspace of R(M) sits inside the pullback subspace of H*(Y_M). The injectivity of mult ω̃ on H^{2k}(Y_M) → H^{2(k+1)}(Y_M) restricts to injectivity on the X-subspace within R(M), provided the X-subspace at grade k+1 is large enough to receive the image.

For k in the d≥2 hypothesis range: empirically, X_k and X_{k+1} satisfy this. For k outside (e.g., k=3, d=1 for hexagon+chord), they don't.

## Refined geometric proof template

For any loopless matroid M satisfying the d≥2 bigrade hypothesis at some (m, d):

1. Build wonderful compactification Y_M = iterated blow-up of (P^1)^n along the matroid coordinate subspace arrangement. Y_M is smooth projective Kähler.

2. Hard Lefschetz on Y_M with the Aut(M)-invariant Kähler class ω̃ = (Σ x_i) - ε·(exceptional corrections). In particular, mult ω̃: H^{2k}(Y_M) → H^{2(k+1)}(Y_M) is injective for k in the lower-half range.

3. R(M) = H*(Y_M) / (exceptional ideal). The exceptional ideal is closed under mult ω̃, so the operator descends.

4. R(M)|_X at the d≥2 bigrades corresponds to a Lefschetz-stable sub-piece of the pullback subspace of H*(Y_M). The block-triangular structure isolates this sub-piece.

5. The injectivity of mult ω̃ on H^{2k}(Y_M) restricts to injectivity of ∂* on R(M)|_X at the bigrade (m=k, d=n-2k).

## Status

- **Empirically supported across many matroids:** the project's conjecture at d≥2 bigrades.
- **Triangle: completely proven geometrically** (notes/28).
- **Hexagon+chord: verified at the d≥2 bigrade**; the non-hypothesis case shows why the proof template's scope is exactly the conjecture's scope.
- **M(K_4 − e): verified to be outside the hypothesis** (X-bipartite at non-d≥2 grades). The HL failure there is OK; it's outside scope.

## What remains for a full general proof

The technical step is **Step 4** of the refined template: identifying R(M)|_X as a specific Lefschetz-stable sub-piece of H*(Y_M) for general matroids M. For Triangle this was manifest. For hexagon+chord, we'd need to:

1. Build Y_{hexagon+chord} explicitly = wonderful compactification with multiple iterated blow-ups (along 3 circuit subspaces in (P^1)^7, with their intersections).
2. Identify R(M)|_X at grades 2 → 3 inside H*(Y_M) → R(M).
3. Verify the block-triangular structure preserves injectivity.

This is research-level intersection theory but follows a clear template. For each matroid in the d≥2 hypothesis, the proof is concrete (if tedious).

## Files

- `computations/hexagon_chord_test.py` — verifies HL behavior on hexagon+chord.
- `notes/27, 28, 29` — geometric setting, Triangle proof, scope correction.
- `notes/30` — this file (refined template).

## What we've actually accomplished this session

1. **Identified the geometric setting**: R(M) = H*((P^1)^n minus matroid arrangement), R(M)|_X is a specific sub-piece, mult ω̃ from Kähler class of (P^1)^n descends to our L.

2. **Complete geometric proof for Triangle**: HL on R(Triangle)|_X follows from classical Kähler HL on Bl_p((P^1)^3) via block-triangular argument. Solid.

3. **Identified scope correctly**: the proof template works at the d≥2 bigrade hypothesis, not universally. M(K_4 − e) and hexagon+chord at non-hypothesis grades demonstrate that the broader "HL on R(M)|_X" claim is FALSE.

4. **Verified project conjecture on a genuinely connected non-uniform matroid**: hexagon+chord at (m=2, d=3) — ∂* is INJECTIVE as predicted. ✓

The geometric proof framework is real, structurally clean, and matches the project's conjecture exactly. The remaining work is making the framework rigorous for each matroid (or in general).
