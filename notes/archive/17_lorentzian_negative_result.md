# Decisive negative: G̃_M is NOT Lorentzian in 2n variables

**Date: 2026-05-22 (continued).**

## What I tested

Define `G̃_M(z₁, …, z_n; w₁, …, w_n) := Σ_{(A,B) ord. indep partition of E} z^A w^B`, a homogeneous polynomial of degree n in 2n variables.

**Conjecture (now disproven):** `G̃_M` is Lorentzian in the sense of Brändén-Huh.

**Test:** A homogeneous degree-n polynomial in N=2n variables is Lorentzian iff every (n-2)-fold partial derivative — yielding a quadratic in the remaining variables — has Hessian with at most one positive eigenvalue.

For `G̃_M` after differentiating with respect to `I_z ⊆ {z}` and `I_w ⊆ {w}` with `|I_z| + |I_w| = n-2` (disjoint, by squarefreeness), the resulting quadratic has 4 monomials in the variables of the two free indices. Its Hessian has block form
`H = [[0, C], [C^T, 0]]`
where `C = [[c_AA, c_AB], [c_BA, c_BB]] ∈ {0, 1}²ˣ²`, with each `c_{αβ}` being 1 iff a specific ordered indep partition exists.

Eigenvalues of `H` are `±σ_1, ±σ_2` where `σ_i` are singular values of `C`. For Lorentzian (≤ 1 positive eigenvalue): need `rank(C) ≤ 1`, i.e., `det(C) = c_AA · c_BB − c_AB · c_BA = 0`.

## Results

| Matroid | (n-2)-fold partials | Lorentzian failures |
|---------|---------------------|---------------------|
| `U_{2,3}` | 6 | **6** (all fail) |
| `U_{4,4}` (boolean) | 24 | 0 (all pass) |
| `U_{3,4}` | 24 | 12 |
| `U_{3,5}` | 80 | 60 |
| `U_{4,6}` | 240 | 120 |
| `M(K_4)` | 240 | 30 |
| `N₁ = M(K_6)\|_{0..7}` | 1792 | 288 |

The failure pattern is identical across cases: `(c_AA, c_AB, c_BA, c_BB) = (1, 1, 1, 0)` (or a permutation), giving Hessian eigenvalues `±1.618, ±0.618` (or `±1, ±1`).

## Why `G̃_M` fails Lorentzian

The failure `c_AA = c_AB = c_BA = 1, c_BB = 0` translates to:
> There exist two free indices `m_1, m_2` and a fixed assignment on `E \ {m_1, m_2}` such that the partition `(A, B)` with `m_1, m_2 ∈ A` is indep, the partition with `m_1 ∈ A, m_2 ∈ B` is indep, the partition with `m_1 ∈ B, m_2 ∈ A` is indep, BUT the partition with `m_1, m_2 ∈ B` is NOT indep.

This is precisely the **failure of a matroid 2-partition "Plücker exchange"**: you can't always swap free elements between the two halves of a partition. The classical Plücker relations hold for matroid *bases* (= matroid exchange axiom). The "doubled" version for *bipartitions* is *not* a theorem of matroids — `U_{2,3}` is a direct counterexample.

## Concrete `U_{2,3}` case

`I_z = ∅, I_w = {0}`, free indices `{1, 2}`. Compute:
- `c_AA` (both `1, 2 ∈ A`): `A = {1, 2}, B = {0}`. Both size ≤ rank=2. **Indep ✓** → `c_AA = 1`.
- `c_AB` (`1 ∈ A, 2 ∈ B`): `A = {1}, B = {0, 2}`. Both indep ✓ → `c_AB = 1`.
- `c_BA`: `A = {2}, B = {0, 1}`. Indep ✓ → `c_BA = 1`.
- `c_BB` (both in `B`): `A = ∅, B = {0, 1, 2}`. `|B| = 3 > rank = 2`. **NOT indep** → `c_BB = 0`.

So `c_AA · c_BB = 0` but `c_AB · c_BA = 1`. Plücker fails. Hessian rank 2, two positive eigenvalues, Lorentzian fails. ∎

## What does this mean for the proof strategy?

**Lorentzian methods cap out at the DIM half of Theorem 4'.**

The Ardila et al. polynomial `Z_{q, ν}(x, y) = Σ_{S indep} x^S y^{n-|S|}` (Lorentzian in n+1 variables — proven) gives:
- `|X_d(M)| / C(n, d)` is log-concave in `d` (= dim half of Theorem 4').

But it does NOT give:
- The bipartite incidence matrix `∂*|_{X_k}: ℝ^{X_k(M)} → ℝ^{X_{k+1}(M)}` is injective (= rank half).

The natural 2n-variable lift `G̃_M(z, w)` that would have given the rank half via Hessian rank theory is **not Lorentzian** for non-boolean matroids. This isn't an "almost Lorentzian" situation; the failure is systematic and immediate at the smallest non-boolean matroid.

## Which methods are still in play

Reordering my earlier ranking based on this negative result:

**1. ✗ Brändén-Huh Lorentzian on multivariate G̃_M.** Eliminated.

**2. Eur-Huh-Larson stellahedral geometry.** Still in play. The stellahedral variety `Y_M` has rich cohomology and supports hard Lefschetz; need to identify our X-vector / bipartite incidence as some specific structure there.

**3. AHK Hodge theory on a doubled / augmented Chow ring.** Still in play. The augmented Chow ring of Pagaria-Pezzoli / BMPW has equivariant Hodge theory but graded dims = "augmented Whitney numbers", not directly the X-vector. May require a new construction.

**4. Karn-Wakefield stressed-hyperplane relaxation.** Still in play, most matroid-natural. Relax stressed hyperplanes to reduce to uniform case.

**5. Anari-Liu-Vuong matroid intersection HDX.** Still in play but open at the literature level. Matroid intersection mixing not yet proven.

## What I'd recommend trying next

Given the negative result on Lorentzian, my updated ranking is:

### Most promising: KW stressed-hyperplane relaxation (#4)

The Karn-Wakefield framework is closest to our equivariant goal:
- They prove equivariant log-concavity of KL polynomials for paving matroids.
- Their method: starting from a paving matroid M, identify a "stressed" hyperplane (= near-circuit hyperplane), relax it to a basis, iterate to uniform. At each step, show the desired property (log-concavity) is preserved.
- For our problem: the analogous step would be "relax M → M' and show Theorem 4'-II(M) ⟸ Theorem 4'-II(M')".

**Tractability:** the relaxation step is combinatorial; doesn't require AG. Could be attempted directly.

**Limitation:** KW works for paving matroids. Our failing N₁ is graphic, not paving. May need a generalization.

### Second-most: Stellahedral geometry (#2)

The stellahedral variety Y_M has cohomology = Tutte polynomial. If the X-polynomial G_M(z, w) can be realized as a specialization of T_M(x, y), then hard Lefschetz on Y_M (proven by EHL) gives our injectivity for free.

**Tractability:** requires reading EHL paper + figuring out the X-vector connection. Heavy AG.

**Limitation:** "If" is doing a lot of work. May not realize G_M directly.

### Third: New Chow ring construction

Construct a Chow ring `A^*_X(M)` whose graded dimensions equal `|X_d(M)|`, then prove hard Lefschetz on it via the AHK paradigm.

**Tractability:** Research-level work.

**Reward:** Would resolve the conjecture directly.

## Honest assessment

The Lorentzian approach was the cleanest computational path, and it's now eliminated. The remaining high-power methods (#2, #3, #4) all require substantial engagement with the algebraic geometry / matroid combinatorics literature beyond what I can productively do in this session.

The most actionable next step is **(#4) Karn-Wakefield relaxation**, which is matroid-combinatorial and doesn't require AG. A natural starting point: try to relate Theorem 4'-II for M and M\e (deletion) or M/e (contraction), and see if induction on |E| gives a path.

Want me to try the KW relaxation approach in the next session?

## Files

- `computations/test_g_tilde_lorentzian.py` — Lorentzian test on G̃_M
- `computations/test_g_tilde_lorentzian.log` — Results: G̃_M not Lorentzian for any non-boolean test matroid.
