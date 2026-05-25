# X-ULC conjecture: the central conjecture for the dim half of Theorem 4'

**Date: 2026-05-22 (session end).**

**UPDATE (same session, later):** **X-ULC is already a theorem.** It is Corollary 1.7 of [Ardila-Mantilla, Cristancho, Denham, Eur, Huh, Wang, arXiv:2601.02547](https://arxiv.org/abs/2601.02547) (Jan 2026), where they define `N_M(a, b) := #{ordered partitions E = A ⊔ B, A indep, B indep, |A|=a, |B|=b}` (= our `|X_a(M)|` when `a + b = n`) and prove

> For any matroid M and any `0 ≤ i ≤ j ≤ k ≤ l ≤ n` with `i + l = j + k`,
> `j! k! N_M(j, k) ≥ i! l! N_M(i, l)`.

Specializing `(i, l) = (a−1, n−a+1)`, `(j, k) = (a, n−a)` gives the normalized monotonicity `|X_a|/C(n, a) ≥ |X_{a-1}|/C(n, a-1)` for `a ≤ n/2`, which combined with palindromicity gives unimodality. Theorem 1.6 of the same paper gives the stronger coefficient-wise Lorentzian inequality `I_{q,ν;k}^2 ⪰ (1 + 1/k) I_{q,ν;k-1} I_{q,ν;k+1}` for all M^♮-concave functions ν — matroid independence indicators are a special case.

A companion paper, [Cao-Chen-Li-Wu, arXiv:2601.03809](https://arxiv.org/abs/2601.03809), proves the same dim-half statement specifically for matroid independent sets (their `π_{i,j}(N)` = `|X_i(N)|`, Theorem 3.2: `π_{k,k}(M) ≥ (1 + 1/k) π_{k-1, k+1}(M)` for matroids of size `2k`), as part of resolving Dowling's 1980 polynomial conjecture.

**So the dim half of Theorem 4' is closed.** The Lorentzianness of `G_M(z, w) = Σ_d |X_d(M)| z^d w^{n-d}` follows from arXiv:2601.02547 Theorem 1.6.

The **full-rank half** of Theorem 4' (= the bipartite incidence `∂*|_{X_k} : ℝ^{X_k} → ℝ^{X_{k+1}}` has rank `|X_k|`) is, as far as I can tell, **not** addressed by either paper. It remains the genuinely open piece of our proof.

---

(Original content of this note follows; superseded by the update above as far as the dim half is concerned.)


## The X-ULC conjecture

For a matroid `N` on ground set `E` with `n' = |E|`, define
```
|X_d(N)| := # { A ⊆ E : |A| = d,  A ∈ Indep(N),  E \ A ∈ Indep(N) }
```
— the count of *balanced bipartitions of E into two independent sets of sizes (d, n'−d)*.

**Conjecture (X-ULC).** For every matroid N, the X-vector `(|X_d(N)|)_{d=0}^{n'}` satisfies the Ultra Log-Concavity inequality:
```
( |X_d| / C(n', d) )² ≥ ( |X_{d-1}| / C(n', d-1) ) · ( |X_{d+1}| / C(n', d+1) )
```
for every d in the support of the X-vector.

**Empirical evidence.** Verified across 510 matroids and N(C,U) submatroids in `computations/x_vector_ULC.py`: **0 violations**.

## Why this is the right conjecture

(i) **By complementation**, `|X_d(N)| = |X_{n' - d}(N)|`: the X-vector is palindromic around `n'/2`.

(ii) **Combined with ULC**, palindromic + log-concave ⇒ unimodal with peak at `⌊n'/2⌋`.

(iii) **For our application** (Theorem 1's reduction), we need `|X_k(N(C,U))| ≤ |X_{k+1}(N(C,U))|` for `(k, d)` with `n' = 2k + d`, `d ≥ 2`, `r' ≥ k + d`. Under the X-vector unimodality with peak at `n'/2 = k + d/2 ≥ k + 1` (true for `d ≥ 2`), this inequality is automatic.

So **X-ULC ⇒ dim part of Theorem 4'**.

## Two routes to proving X-ULC

### Route I: Lorentzian polynomials on a "doubled" structure

Define the bivariate generating polynomial
```
G_N(z, w) := ∑_d  |X_d(N)| · z^d · w^{n' - d}
            = ∑ { z^|A| · w^|E\A|  :  A ⊆ E, A indep, E\A indep }.
```
This is a homogeneous polynomial of degree `n'` in two variables `(z, w)`.

By Brändén-Huh: `G_N` is *Lorentzian* (= positive coeffs, M-convex support, Lorentzian-signature Hessian) ⇒ ULC of its coefficients. So **proving `G_N` is Lorentzian closes the dim part of Theorem 4'**.

**Observation:** `G_N` can be expressed as a restriction of the bivariate Lorentzian polynomial `f_M(z_1, ..., z_n) f_M(w_1, ..., w_n)` (which is Lorentzian for loopless `M` by Brändén-Huh) via the substitution `w_i ↔ \bar{z_i}` — but this is *not* a standard Lorentzian-preserving operation. So a fresh proof is needed.

For specific examples in the tested set:
- **N₁ = M(K_6)|_{0..7}**: `G_{N_1}(z, w) = 20 z^3 w^5 + 40 z^4 w^4 + 20 z^5 w^3 = 20 z^3 w^3 (z + w)^2`. **Stable / Lorentzian.**
- **N₂ = M(K_6)|_{0..6,9}**: `G_{N_2}(z, w) = 12 z^3 w^5 + 24 z^4 w^4 + 12 z^5 w^3 = 12 z^3 w^3 (z + w)^2`. **Stable / Lorentzian.**
- **U_{4,6}**: `G(z, w) = 15 z² w⁴ + 20 z³ w³ + 15 z⁴ w² = 5 z² w² (3 z² + 4 zw + 3 w²)`. Discriminant of `3 z² + 4 zw + 3 w²` is `-20 < 0`, so the quadratic factor has complex conjugate roots. Lorentzian iff the polynomial is "stable", which holds for complex-conjugate roots with negative discriminant. (Yes — stable.)

**Open:** General proof that `G_N` is Lorentzian for every matroid N.

### Route II: Direct combinatorial inequality

The X-vector |X_d| counts balanced bipartitions. There's a natural bijective interpretation:
- `(A, E \ A)` with both indep ↔ a "2-coloring of E by independent classes".
- Going from level `d` to `d+1` corresponds to swapping one element from `E\A` to `A`.

The X-ULC inequality can be reformulated as an *inequality between three counts* via the M-convex / "common indep" interpretation:
```
|X_d|² · C(n', d-1) · C(n', d+1) ≥ |X_{d-1}| · |X_{d+1}| · C(n', d)².
```
For matroids viewed as intersection `N ∩ N*` (via the "indep + co-indep" interpretation), this is a Mason-style log-concavity inequality on the *common* indep sets of two matroids — a topic studied in subsequent ALOGV / Brändén-Leake / Anari et al. work on the *matroid intersection polytope*.

Currently I don't recall a direct theorem in the literature that gives X-ULC, but it appears to fit naturally into the matroid-intersection log-concavity framework.

## What X-ULC does NOT give us

X-ULC only gives the **dimensional inequality** `|X_k| ≤ |X_{k+1}|` for `k < n'/2`. The full Theorem 4' also requires:

> The bipartite incidence `∂*|_{X_k(N)} : ℝ^{X_k(N)} → ℝ^{X_{k+1}(N)}`,
> `∂*(x_A) = ∑_{i ∈ E \ A, A ∪ i ∈ Indep(N)} x_{A ∪ i}`,
> has rank `|X_k(N)|` (= injective).

This *full rank* statement is **not** implied by X-ULC. The earlier draft's "Mason / Edmonds / Brändén-Huh / ALOGV full-rank theorem" that we hoped would give this was *not* a theorem of matroids in general (see `notes/12_mason_fails_X_restores.md`).

So Theorem 4' has two halves:
- **(I)** `|X_k(N)| ≤ |X_{k+1}(N)|` for `k < n'/2` — provable (route I or II above) if X-ULC.
- **(II)** Bipartite incidence on `X_k → X_{k+1}` is full rank — still open, no candidate proof.

## A possible cleaner formulation of half (II)

Theorem 4'-II says: the kernel of the unrestricted level-walk `∂*: ℝ^{Indep_k(N)} → ℝ^{Indep_{k+1}(N)}` has trivial intersection with `ℝ^{X_k(N)}`.

Equivalently, view `ℝ^{X_k} ↪ ℝ^{Indep_k}` as a subspace. We need the level-walk to be injective ON this subspace.

A possible characterization of `ker(∂*)`: via the **circuit space** of the matroid `N`. The kernel is spanned by "syzygies" of indep_k sets that share extensions. The X-restriction filters these syzygies — concretely, on the failing examples, the syzygies that DO have X-support are linearly independent on X-coordinates.

A formal proof might come from analyzing the structure of `ker(∂*)` in terms of matroid circuits, then showing the X-coordinates of those syzygies span a subspace transverse to `ℝ^{X_k}`.

## Concrete next steps

1. **Attempt to prove X-ULC via Route I (Lorentzian).** Either via direct Hessian computation on `G_N(z, w)`, or by realizing `G_N` as a specialization of an already-known Lorentzian polynomial.

2. **Attempt to prove Theorem 4'-II directly.** Possible approaches:
   - Characterize `ker(∂*)` via matroid circuits.
   - Use Anari–Liu–Oveis Gharan's matroid intersection spectral gap framework.
   - Exploit the **`(N, N*)` symmetry** of the X-construction: `X_d(N)` is a self-dual matroid invariant.

3. **Combine I + II** to close Theorem 4', hence Theorem 1, hence ELC.

## Strategic recommendation

X-ULC (or equivalently, Lorentzianness of `G_N`) is a clean, well-defined, empirically robust conjecture that may well be tractable. It connects directly to the existing Lorentzian / matroid-intersection literature. **This is the recommended next mathematical attack point.**

The dim part of Theorem 4' is half of what we need. The "full rank" part is harder and requires genuine new structure.
