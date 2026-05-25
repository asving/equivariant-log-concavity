# QLC — Equivariant Log-Concavity of matroid f-vectors

**Goal:** prove ELC for the f-vector of independent sets of an arbitrary loopless matroid `M` — i.e., that the virtual `Aut(M)`-representation `[f_{m+1}(M)]² − [f_m(M)] · [f_{m+2}(M)]` is effective for each `m ≥ 0`. Equivalently (§2 of `PAPER.md`), prove injectivity of the tensor Lefschetz operator `L = Σ x_i ⊗ x_i` on `S(M) = R(M) ⊗ R^∨(M)`.

## Current state (2026-05-25)

### Proven result — paving matroids

> **Theorem** (PAPER.md, PAPER.tex). ELC of the f-vector holds for every **paving matroid** (= every matroid where every circuit has size ≥ rank).

This is the first proof of f-vector ELC for an infinite class of matroids beyond direct sums of uniforms. The class includes all sparse paving matroids (conjecturally asymptotically almost all matroids), Steiner system matroids, and many specific combinatorial designs.

**Method:** stressed-hyperplane relaxation (Karn–Nasr–Proudfoot–Vecchi paradigm) applied to the X-restricted bipartite incidence operator on the matroid's independence complex. A single inductive step from the boolean Lefschetz base case suffices.

The paper compiles (`PAPER.tex` → `PAPER.pdf`, 7 pages).

### Open conjecture — full ELC

> **Conjecture** (PAPER.md §5.3). For every loopless matroid `M` and every bigrade `(m, -d)` with `2m+d ≤ n`, `m+d ≤ rank(M)`, `d ≥ 2`, the bipartite-incidence operator `∂*: ℝ^{X_m(M)} → ℝ^{X_{m+1}(M)}` is injective.

Empirically verified across **200,000+ matroid orbits** (graphic `M(K_n)` for `n ≤ 6`, Fano, NonFano, Pappus, NonPappus, Vámos, AG(3,2), various restrictions of `M(K_6)`). No counterexample known.

### Geometric proof framework (sketched in this session)

The session of 2026-05-24/25 identified the canonical geometric setting and proved the conjecture for Triangle = U(2,3):

- **R(M) = H*(U_M)** where `U_M = (P^1)^n \ ⋃_{C circuit} Z_C` is the matroid coordinate subspace arrangement complement (Goresky-MacPherson 1988).
- **The Lefschetz operator L** is the Aut(M)-invariant Kähler class of `(P^1)^n` descended to `R(M) ⊗ R^∨(M)`.
- **Triangle proof complete** (`notes/28`): HL on `R(Triangle)|_X` follows from classical Kähler Hard Lefschetz on `Y = Bl_p((P^1)^3)` via block-triangular inheritance under the restriction `H*(Y) → R(M)`.
- **Scope correctly identified** (`notes/29-30`): the geometric proof template applies at exactly the `d ≥ 2` bigrade hypothesis. Outside this hypothesis, HL on `R(M)|_X` can fail (verified on M(K_4 − e) and hexagon+chord at non-hypothesis grades).
- **X-restriction rescues injectivity** (`notes/32`): even when the f-vector decreases (so mult ω on `R(M)` cannot be injective), the X-restriction picks a Lefschetz-stable subspace where injectivity is preserved. This is the structural content.

**To complete the general proof:** develop a "matroid semi-small decomposition" for the wonderful compactification of the matroid coordinate subspace arrangement, parallel to BHMPW (arXiv:2002.03341) for the AHK Chow ring. The decomposition would identify `R(M)|_X` as the appropriate Lefschetz-stable sub-piece of `H*(Y_M)`. This is research-level but follows a clear template.

## Repository structure

```
qlc/
├── README.md                   ← you are here: project entry point
├── HANDOFF.md                  ← condensed state for the continuing instance
├── PAPER.md / PAPER.tex / PAPER.pdf   ← the formal short paper (paving ELC)
├── PREPRINT_DRAFT.md           ← earlier longer draft, useful exposition
├── notes/                      ← session notes documenting the journey
│   ├── HISTORY.md              ← compressed journey: ideas tried, what worked/failed
│   ├── 18_kw_proof_sparse_paving.md  ← the proven theorem in detail
│   ├── 19–22                   ← non-paving extensions, Gui-Xiong analysis
│   ├── 23–26                   ← Schur-complement, HL framing, twistor attempts
│   ├── 27–32                   ← geometric setting, Triangle proof, scope, X-rescue
│   └── archive/                ← raw historical notes 01–17 (early exploration)
└── computations/               ← Python verification scripts
    ├── gpu_rank.py             ← Matroid class, GPU mod-p rank
    ├── sparse_rank.py          ← sparse mod-p rank for big matrices
    ├── test_kw_relaxation.py   ← verifies the proven theorem's inductive step
    ├── verify_paper.py         ← canonical regression test (1195 OK / 0 FAIL)
    ├── triangle_blowup_HL.py   ← complete geometric proof for Triangle
    ├── verify_RM_geometric.py  ← verifies R(M) = H*(arrangement complement)
    ├── hexagon_chord_test.py   ← HL verification for connected non-uniform matroid
    ├── k4_minus_edge_geometric.py  ← HL failure outside d≥2 hypothesis
    ├── test_hard_lefschetz_x.py  ← HL on R(M)|_X for various matroids
    └── ...                     ← many exploratory scripts
```

## Quick start

### Verify the proven result (paving theorem)

```bash
cd computations/
python verify_paper.py         # canonical regression test (1195 OK / 0 FAIL)
python test_kw_relaxation.py   # verifies the KW inductive step
```

### Reproduce Triangle's geometric proof

```bash
python computations/triangle_blowup_HL.py
```

Shows the 4×4 Lefschetz matrix on `H*(Bl_p((P^1)^3))`, its block-triangular structure, and the 3×3 ∂* matrix on `R(Triangle)|_X` inherited from the classical Kähler HL.

### Test HL on other matroids

```bash
python computations/test_hard_lefschetz_x.py    # multiple matroids
python computations/hexagon_chord_test.py       # connected non-uniform
python computations/k4_minus_edge_geometric.py  # shows HL fails outside d≥2 hypothesis
```

## How to pick up the project

1. **Read `PAPER.md`** for the proven result (paving theorem) and its proof.
2. **Read `HANDOFF.md`** for current state and recommended next directions.
3. **Read `notes/HISTORY.md`** for the compressed journey of ideas tried.
4. **For the geometric program**: read notes/27 → 28 → 30 → 32 in order. Notes 21–26 document earlier exploration that led to the current framework.

## Open directions, ranked

1. **Develop matroid semi-small decomposition for subspace-arrangement wonderful compactifications.** Adapt BHMPW (arXiv:2002.03341) from the AHK Chow ring setting to our setting. This would complete the general geometric proof. Research-level, 6–12 months estimated. See `notes/31, 32` for the precise technical content needed.

2. **Verify X-Identification computationally on M(K_4) or hexagon+chord.** Build the wonderful compactification's cohomology ring explicitly via intersection theory and verify that the Lefschetz primitives of `H*(Y_M)` project to `R(M)|_X` under the natural quotient. 1–2 month computational AG project.

3. **Connect to ALOV polynomial capacity** (arXiv:1810.04341). The X-bipartite structure is essentially matroid intersection. ALOV proved (non-equivariant) log-concavity. An equivariant lift would give an alternative proof. Research-level.

4. **Treat the paving theorem as the publishable result on its own.** PAPER.tex compiles to a 7-page paper ready for submission. The non-paving case can be stated as a clean open conjecture for the community.

## Compute environment

`/workspace-vast/asving/qlc/` ran on 8× NVIDIA H200 GPUs, 224 cores, 2 TB RAM. Mod-`p` Gaussian elimination (sparse, mod `p = 10007`) is the workhorse for the largest matroid computations.

## Files generated during sessions

- `*.log` files in `computations/` are gitignored — they're raw stdout from verification runs and can be regenerated.
- `*.aux`, `*.log`, `*.out` from LaTeX builds are gitignored.
- `PAPER.pdf` is committed (7 pages, compiles from `PAPER.tex` with `pdflatex`).
