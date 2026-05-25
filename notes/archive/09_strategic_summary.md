# Strategic summary after the big GPU run

## What we now know

### 1. CONJ-A (the strong "ISO" form) is FALSE.

Confirmed counterexamples — hard Lefschetz `L^d : S_{-d} → S_d` is NOT iso:
- **M(K_5)** at d=2: deficit 180, fully localized at internal degree m = 2.
- **M(K_6)** at d=2: deficit 35610, split as 1170 at m=2 + 34440 at m=3.
- **M(K_6)** at d=3: deficit 4500, fully localized at m=2 (equals `f_2² − f_1·f_3` exactly).

### 2. The user's conjecture (INJ at d≥2) is alive — and gives ELC.

L : S_{-d} → S_{-d+2} **injective** at every d ≥ 2 confirmed for:
- All small uniform matroids
- M(K_4), M(K_5), M(K_6)
- Fano, NonFano, Pappus, NonPappus, Vamos V_8, AG(3,2)

ELC for the f-vector of these matroids is **established by direct computation**.

### 3. Per-internal-degree localization of the HL failure.

`L^d` failure on `S_{-d} → S_d` localizes to "middle" internal-degree blocks `m`. The
top (m=0, near-top) and bottom (m=rank) blocks are always iso. The deficit lives at
intermediate m, which is exactly where the f-vector log-concavity is "barely" satisfied
(small slack).

For M(K_6) at d=3, deficit equals the LC defect at (f_1, f_2, f_3). Likely a clue
to the deep structure.

### 4. The hybrid CONJ-A' (INJ on `R(M_1) ⊗ R^∨(M_2)` for `M_2 ≼ M_1`) is the right
   inductive object.

Tested for `(M\e, M/e)` on M = M(K_5) (3 edges) and M = Fano: CONJ-A' INJ at d≥2 holds in every test. d=1 hybrid may fail.

### 5. Geometric reframing.

The structure on S(M) is a **weak Lefschetz package**, not a hard one. `L` is injective
(user's conjecture); the failure of hard-Lefschetz is governed by **primitive classes**
at intermediate internal degrees. These primitives are non-trivial new matroid invariants.

The clean geometric home is likely the **Lefschetz-Hodge decomposition with primitives**,
or equivalently the **doubled Lorentzian polynomial** structure (extending Brändén-Huh).

## Strategic recommendations

### A. The inductive proof should target the WEAKER user-conjecture, generalized to hybrid pairs (CONJ-A').

Statement to prove inductively:
> For every pair `(M_1, M_2)` of matroids on `[n]` with `M_2 ≼ M_1`, every `d ≥ 2`,
> and every internal `m`: the map
> `L : R(M_1)_m ⊗ R^∨(M_2)_{-(m+d)} → R(M_1)_{m+1} ⊗ R^∨(M_2)_{-(m+d-1)}` is INJECTIVE.

Induction on `|E(M_1)|` via deletion/contraction. Base case: `M_1 = M_2 = U_{1,1}` or boolean (trivial). Step: use the 4-piece decomposition `A ⊕ B ⊕ C ⊕ D` of `S(M_1, M_2)` with mixing `L_e : B → C`; INJ on `A, B, C, D` + L_e-compatibility ⇒ INJ on the whole.

Drop the iso requirement entirely — we don't need it for ELC, and it's false anyway.

### B. The Lorentzian polynomial approach is concretely viable.

Brändén-Huh: the f-vector polynomial `f_M(z_1,...,z_n) = ∑ z^S` is Lorentzian. The
matrix of `L : R_m ⊗ R^∨_{-(m+2)} → R_{m+1} ⊗ R^∨_{-(m+1)}` is, entry-by-entry, the
mixed derivatives of `f_M ⊗ f_M`. Injectivity of this map should reduce to:

> The **doubled polynomial** `f_M(z) ⊗ f_M(w)` is Lorentzian in `(z, w) ∈ ℝ²ⁿ` with
> respect to the diagonal cone.

(Or some refinement of "Lorentzian" — possibly **stable** or **completely log-concave**.)

This is a direct, tractable generalization of Brändén-Huh and would give ELC for ALL
matroids in one shot.

### C. Stop chasing CONJ-A (the iso version).

It's false; the primitive classes are interesting but they're not the path to ELC.

### D. Test M(K_7) via symmetry reduction.

For M(K_n) under S_n action: decompose S_{-d} into S_n-isotypic blocks (small dim
each), check L's rank in each block. This could push the verification to M(K_7) and
beyond efficiently.

### E. Possible publishable nugget right now.

> **Theorem (computational).** For each `M ∈ {M(K_4), M(K_5), M(K_6), Fano, NonFano,
> Pappus, NonPappus, Vamos V_8, AG(3,2)}`, and every `d ≥ 2`, the map
> `L : S_{-d}(M) → S_{-d+2}(M)` is `Aut(M)`-equivariantly injective. Consequently
> ELC of the f-vector holds for each.

This is a concrete result that could appear in an arXiv note. The construction (R ⊗ R^∨)
and conjecture are clean enough to publish even without the general proof.
