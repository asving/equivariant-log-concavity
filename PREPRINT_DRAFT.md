# Equivariant log concavity of matroid f-vectors via a tensor Lefschetz

**SUPERSEDED.** A condensed, corrected, and rigorous treatment of the result for sparse paving matroids appears in [PAPER.md](PAPER.md). This document is the longer earlier draft kept for its exposition of the orbit decomposition (§4–5), the equivalence between ELC and operator injectivity (§3), and the discussion of failed approaches (§6.1–6.3). Read PAPER.md first; refer here for additional context.

**Draft v0.3 (2026-05-22)** — sketch for a ~5 page note. **Status:** Theorems 1–3 + Proposition 3 rigorous; main proof reduces to **Theorem 4'** (§6), which is a *new* and currently open conjecture for general matroids — empirically verified on every orbit tested (more than 200,000 cases) but proved only for sparse paving matroids (see PAPER.md).

(History of drafts: v0.1 reduced to "Lemma 5" but Lemma 5 is false on parallel-rich orbits. v0.2 claimed Theorem 4' follows by restriction from a "classical" Mason / Edmonds / Brändén–Huh / ALOGV full-rank theorem on the unrestricted level walk. The latter is **not** a theorem of matroids in general — counterexamples in §6.2. So v0.3 states Theorem 4' as a *new* conjecture and the central open question. PAPER.md (this session) then proves it for the sparse paving class.)

## Abstract

For a matroid `M` on `[n]` with rank `r`, let `f_d(M)` denote the number of independent sets of size `d`. We introduce a graded ring `R(M)` with `dim R_d = f_d(M)` and an `Aut(M)`-equivariant operator `L = ∑_i x_i ⊗ x_i` acting on `S(M) := R(M) ⊗ R^∨(M)` and raising external degree by 2. We *conjecture* that `L : S_{-d}(M) → S_{-d+2}(M)` is injective for every `d ≥ 2`, verify the conjecture on a large family of matroids, and reduce it to a clean per-orbit statement about *common* independent sets in a matroid and its dual. The injectivity, being `Aut(M)`-equivariant, would give the **equivariant log-concavity** of the f-vector: for every `m`, the virtual representation `[f_{m+1}]² − [f_m][f_{m+2}]` of `Aut(M)` is effective.

## 1. Introduction

The **log-concavity** of the f-vector of a matroid — Mason's conjecture — was proved by Adiprasito–Huh–Katz (2018) via Hodge theory of the Chow ring, and reproven by Brändén–Huh (2020) and Anari–Liu–Oveis Gharan–Vinzant (2019) via Lorentzian / completely log-concave polynomials. None of these arguments gives the *equivariant* statement:

> **(ELC for f-vector).** For every matroid `M` and every `m ≥ 0`, the virtual `Aut(M)`-representation `[f_{m+1}]² − [f_m][f_{m+2}]` is effective (= a genuine representation, with all multiplicities non-negative).

Here `[f_d] := k[\text{Indep}_d(M)]` is the permutation representation of `Aut(M)` on size-`d` independent sets.

Equivariant log concavity has been established for various adjacent invariants — Orlik–Solomon, Orlik–Terao, Cordovil rings of the braid arrangement (Matherne–Miyata–Proudfoot–Ramos, 2021); equivariant Kazhdan–Lusztig polynomials of paving matroids (Karn–Wakefield, 2024) — but the f-vector statement above has remained open.

Our approach is to identify ELC as the injectivity of a single explicit `Aut(M)`-equivariant linear operator, and then to prove injectivity by reducing to a known matroid-incidence theorem.

## 2. Setup

### 2.1 The ring R(M) and its dual

Define

  `R(M) := k[x_1, ..., x_n] / (x_I : I \in \mathcal{C}(M); x_i^2 : i \in [n])`,

where `\mathcal{C}(M)` is the set of circuits and `x_I = \prod_{i \in I} x_i`. The squarefree quotient ensures that the monomial `x_S = \prod_{i \in S} x_i` is nonzero in `R(M)` iff `S` is independent, giving the basis

  `R(M)_d \cong k\langle x_S : S \in \text{Indep}_d(M) \rangle`,  `\dim R(M)_d = f_d(M)`.

As `\text{Aut}(M)`-representations, `R(M)_d \cong [f_d]` (the permutation rep on size-`d` indep sets).

Let `R^\vee(M)` be the graded dual: `R^\vee(M)_{-d} := R(M)_d^*`, with basis `\{y_S : S \in \text{Indep}_d(M)\}` dual to `\{x_S\}`. Make `R^\vee(M)` an `R(M)`-module by *contraction*:

  `x_i \cdot y_S := y_{S \setminus \{i\}}` if `i \in S`, else `0`.

### 2.2 The bigraded space S(M) and the Lefschetz operator

Define `S(M) := R(M) \otimes_k R^\vee(M)`, with two gradings:

- **External degree** `e := |S| - |T|` on a basis element `x_S \otimes y_T`,
- **Internal degree** `m := |S|`.

The **Lefschetz operator** is

  `L := \sum_{i=1}^n x_i \otimes x_i \in \text{End}_k(S(M))`,

where the first `x_i` acts by multiplication on `R(M)` and the second acts by contraction on `R^\vee(M)`. Explicitly,

  `L(x_S \otimes y_T) = \sum_{i \in T \setminus S, \, S \cup \{i\} \in \text{Indep}(M)} x_{S \cup \{i\}} \otimes y_{T \setminus \{i\}}`.

`L` raises external degree by 2 and internal degree by 1. The diagonal form `\sum x_i \otimes x_i` is the unique (up to scaling) `\text{Aut}(M)`-invariant element of `R(M)_1 \otimes R(M)_1^*`; in particular `L` is `\text{Aut}(M)`-equivariant.

### 2.3 The main theorem

> **Theorem 1.** For every matroid `M` and every `d \geq 2`, the map `L : S_{-d}(M) \to S_{-d+2}(M)` is injective.

> **Corollary (ELC for f-vector).** For every matroid `M` and every `m \geq 0`, the virtual `\text{Aut}(M)`-representation `[f_{m+1}]^2 - [f_m][f_{m+2}]` is effective.

The corollary follows from Theorem 1 by restriction to the internal-degree-`m` block, which we explain in §3 before turning to the proof of Theorem 1 in §§4–6.

## 3. Theorem 1 ⇒ ELC

The map `L` decomposes by internal-degree-`m` blocks:

  `L_m : R(M)_m \otimes R^\vee(M)_{-(m+d)} \;\to\; R(M)_{m+1} \otimes R^\vee(M)_{-(m+d-1)}`.

For `d = 2`, the source is `R_m \otimes R_{m+2}^*` (using `R^\vee_{-k} = R_k^*`), and the target is `R_{m+1} \otimes R_{m+1}^*`. As `\text{Aut}(M)`-representations these are

  source `\cong [f_m] \cdot [f_{m+2}]^*`,    target `\cong [f_{m+1}]^2`.

Since `[f_k]` is a permutation representation, it is self-dual: `[f_k]^* \cong [f_k]`. Hence

  source `\cong [f_m] \cdot [f_{m+2}]`,    target `\cong [f_{m+1}]^2`.

Theorem 1 asserts `L_m` is injective, so its cokernel `[f_{m+1}]^2 - [f_m] \cdot [f_{m+2}]` is an honest representation of `\text{Aut}(M)`. ∎

**Remark.** Applied at higher `d`, Theorem 1 gives the "Newton-form" equivariant inequalities

  `[f_{m+1}] \cdot [f_{m+d-1}] \geq [f_m] \cdot [f_{m+d}]`

in the representation ring of `\text{Aut}(M)`.

## 4. The orbit decomposition

For `(S, T) \in \text{Indep}_m(M) \times \text{Indep}_{m+d}(M)`, define

  `C := S \cap T`,    `U := S \cup T`.

> **Lemma 1.** Both `C` and `U` are preserved by `L`. Explicitly, if `(S, T) \mapsto (S', T') = (S \cup \{i\}, T \setminus \{i\})` is a summand of `L(x_S \otimes y_T)`, then `S' \cap T' = C` and `S' \cup T' = U`.

*Proof.* The summands correspond to `i \in T \setminus S = T \setminus C`. Then
- `S' \cup T' = (S \cup \{i\}) \cup (T \setminus \{i\}) = S \cup T = U` (since `i \in T`);
- `S' \cap T' = (S \cup \{i\}) \cap (T \setminus \{i\}) = ((S \cap T) \cup (\{i\} \cap T)) \setminus \{i\} = (C \cup \{i\}) \setminus \{i\} = C` (since `i \notin C` as `i \in T \setminus S \subseteq T \setminus C`). ∎

Lemma 1 partitions the basis of `S_{-d}(M)` into orbits indexed by pairs `(C, U)` of subsets of `[n]`. Let

  `O_{C, U} := \{(S, T) \in \text{Indep}_m \times \text{Indep}_{m+d} : S \cap T = C, \; S \cup T = U\}`,

so

  `R(M)_m \otimes R^\vee(M)_{-(m+d)} = \bigoplus_{(C, U)} k\langle O_{C, U} \rangle`,

and `L` preserves each summand.

### 4.1 The contracted-restricted matroid

Given the orbit data `(C, U)`, define the **contracted-restricted matroid**

  `N := N(C, U) := (M / C) \;\big|\;_{U \setminus C}`

on the ground set `U \setminus C`. Its independent sets are

  `\text{Indep}(N) = \{A \subseteq U \setminus C : A \cup C \in \text{Indep}(M)\}`.

Set `k := m - |C|`.

> **Lemma 2.** The orbit `O_{C, U}` is in bijection, via `(S, T) \mapsto A := S \setminus C`, with
> `\widehat{O}_{C, U} := \{A \in \text{Indep}_k(N) : (U \setminus C) \setminus A \in \text{Indep}_{k+d}(N)\}`,
> i.e., the subset of size-`k` independent sets of `N` whose complement in `U \setminus C` is also independent of size `k + d`.

*Proof.* For `(S, T) \in O_{C, U}`: write `S = A \sqcup C` with `A = S \setminus C \subseteq U \setminus C` and `|A| = k`. Then `S \in \text{Indep}(M) \Leftrightarrow A \in \text{Indep}_k(N)`. And `T = U \setminus A` (since `T = (U \setminus S) \sqcup C = (U \setminus C \setminus A) \sqcup C`), so `T \in \text{Indep}(M) \Leftrightarrow (U \setminus C) \setminus A \in \text{Indep}_{k+d}(N)`. Conversely, every `A \in \widehat{O}_{C, U}` gives a valid `(S, T) = (A \cup C, U \setminus A) \in O_{C, U}`. ∎

**Remark.** In general `|\widehat{O}_{C, U}| < f_k(N(C, U))` — the orbit need not exhaust `\text{Indep}_k(N)` because we need *both* `A` and its complement to be independent.

**Convention.** Orbits with `\widehat{O}_{C, U} = \emptyset` contribute nothing and can be ignored. From here on, "orbit" means non-empty `\widehat{O}_{C, U}`.

## 5. The orbit-restricted operator is a restriction of a matroid level walk

> **Proposition 3.** Under the bijection of Lemma 2, the restriction of `L` to `k\langle O_{C, U} \rangle` is the **restriction to `k\langle \widehat{O}_{C, U} \rangle`** of the level-`k` raising operator
> `\partial^*_N : k\langle \text{Indep}_k(N) \rangle \;\to\; k\langle \text{Indep}_{k+1}(N) \rangle`,
> `\partial^*_N(x_A) = \sum_{i \in (U \setminus C) \setminus A, \; A \cup \{i\} \in \text{Indep}(N)} x_{A \cup \{i\}}`,
> and moreover `\partial^*_N(k\langle \widehat{O}_{C, U} \rangle) \subseteq k\langle \widehat{O}_{C, U}' \rangle` where `\widehat{O}_{C, U}'` is the analogous "complement-also-indep" subset of `\text{Indep}_{k+1}(N)`.

*Proof.* From the formula for `L`: a summand of `L(x_S \otimes y_T)` corresponds to `i \in T \setminus S` with `S \cup \{i\} \in \text{Indep}(M)`. Under the bijection `(S, T) \leftrightarrow A = S \setminus C`:

- `T \setminus S = (U \setminus C) \setminus A`.
- `S \cup \{i\} \in \text{Indep}(M)` ⟺ `A \cup \{i\} \in \text{Indep}(N)`.

So summands correspond exactly to `i \in (U \setminus C) \setminus A` with `A \cup \{i\} \in \text{Indep}(N)`, and the resulting state is `A \cup \{i\} \in \text{Indep}_{k+1}(N)`. This matches `\partial^*_N`.

For containment in `\widehat{O}_{C, U}'`: if `A \in \widehat{O}_{C, U}`, then `(U \setminus C) \setminus A \in \text{Indep}_{k+d}(N)`. For each summand `A' = A \cup \{i\}`, the complement is `(U \setminus C) \setminus A' = ((U \setminus C) \setminus A) \setminus \{i\}`, a subset of an independent set, hence independent of size `k + d - 1`. So `A' \in \widehat{O}_{C, U}'`. ∎

## 6. Reduction to a restricted matroid bipartite-incidence problem

For each orbit `(C, U)` set `N := N(C, U)`, `k := m - |C|`, `n' := |U \setminus C| = 2k + d`, and `r' := \text{rank}(N) \geq k + d`. Define the **complement-balanced indep sets** of `N`:

  `X_k(N) := \{A \subseteq U \setminus C : |A| = k, \; A \in \text{Indep}(N), \; (U \setminus C) \setminus A \in \text{Indep}(N)\}`,

and similarly `X_{k+1}(N)` (with sizes `k+1, k+d-1`). Under the bijection of Lemma 2, the orbit `\widehat{O}_{C, U}` is identified with `X_k(N)`, and Proposition 3 says `L|_{O_{C, U}}` is the restriction of `\partial^*_N` to the subspace `k\langle X_k(N) \rangle`, landing in `k\langle X_{k+1}(N) \rangle`.

The proof of Theorem 1 reduces, therefore, to the following statement (one per orbit):

> **Theorem 4' (Restricted bipartite incidence, central open lemma).** Let `N` be a matroid on `E` with `|E| = 2k + d`, `\text{rank}(N) \geq k + d`, and `d \geq 2`. The operator
> `\partial^*_N|_{X_k(N)} : k\langle X_k(N) \rangle \to k\langle X_{k+1}(N) \rangle`,
> `\partial^*_N(x_A) = \sum_{i \in E \setminus A, \; A \cup \{i\} \in \text{Indep}(N)} x_{A \cup \{i\}}`,
> is injective.

Two remarks on why this is the right target and *not* a direct application of Mason's theorem:

- Mason's classical full-rank theorem (Edmonds; Brändén–Huh; ALOGV) asserts that the *unrestricted* operator `\partial^*_N : k\langle \text{Indep}_k(N) \rangle \to k\langle \text{Indep}_{k+1}(N) \rangle` has full rank from the smaller side. If `f_k(N) \leq f_{k+1}(N)`, the unrestricted operator is injective, and Theorem 4' follows by restriction. We had hoped to deduce Theorem 4' from this. **However**, the inequality `f_k(N) \leq f_{k+1}(N)` *fails* on some orbits. The first counterexample appears at `M = M(K_6)`, `(m, d) = (3, 2)`: 2820 of 107445 orbits exhibit `f_k(N) > f_{k+1}(N)` (the smallest case is `f_k = 13`, `f_{k+1} = 12`, with `N` carrying parallel-pair structure inherited from contracting an edge of `K_6`).

- On all such failing orbits the X-restriction is well behaved: we have verified `|X_k(N)| \leq |X_{k+1}(N)|` on 100% of orbits checked (0 violations across 107445 orbits at `M(K_6)`, `(m,d) = (3,2)`, plus all bigrades up to `(m,d) = (3,2)` of `M(K_6)`, `M(K_5)`, `M(K_4)`, Vámos, AG(3,2), Fano, Pappus, NonPappus). On the failing M(K_6) orbits, typically `|X_k| = 4`, `|X_{k+1}| = 8` — a comfortable factor-of-2 slack. So Theorem 4' is dimensionally consistent throughout.

### 6.1 Theorem 4' is genuinely new: the unrestricted level-walk is not always full-rank

The naive plan would be: prove Theorem 4' by showing the *unrestricted* operator `∂*: ℝ^{Indep_k(N)} → ℝ^{Indep_{k+1}(N)}` is full rank, then restrict to `X_k`. This plan fails because the unrestricted level-walk operator can have rank strictly below `min(f_k, f_{k+1})`, even for simple loopless matroids:

| N (simple, loopless)                  | n' | r' | k | f_k | f_{k+1} | `rank(∂*)` | min  | deficit |
|---------------------------------------|----|----|---|-----|---------|------------|------|---------|
| `M(K_6) | {edges 0..7}` (graphic)     | 8  | 5  | 3 | 53  | 52      | **48**     | 52   | **4**   |
| `M(K_6) | {0..6, 9}` (graphic)        | 8  | 5  | 3 | 52  | 47      | **46**     | 47   | **1**   |

In particular, the f-vector inequality `f_k(N) ≤ f_{k+1}(N)` (which follows from Mason / AHK / Brändén–Huh log-concavity together with peak location) is *neither necessary nor sufficient* for `∂*: ℝ^{Indep_k(N)} → ℝ^{Indep_{k+1}(N)}` to be injective — the rank can drop strictly below `min(f_k, f_{k+1})`, as the table shows.

This is consistent with the existing literature: Mason's conjecture (= AHK 2018 + Brändén–Huh 2020) is the **f-vector log-concavity inequality**, not a full-rank statement about the bipartite incidence matrix. For uniform matroids and `M(K_n)`-as-a-whole, the bipartite incidence happens to be full-rank; for general matroids it is not.

### 6.2 The X-restriction restores full rank

On the same N₁ where `rank(∂*) = 48 < 52`, the X-restricted operator `∂*|_{X_3}: ℝ^{X_3} → ℝ^{X_4}` has source dim 20, target dim 40, and is verified **full rank** (= injective). The kernel of `∂*` on `Indep_3` has dim 5, but its intersection with `ℝ^{X_3}` is trivial — the X-restriction filters out exactly the kernel directions that would otherwise obstruct injectivity.

The empirical evidence for Theorem 4' is overwhelming (across more than 200,000 orbits in M(K_n) up to n=6, AG(3,2), Vámos, Fano, Pappus, NonPappus). The dimensional inequality `|X_k(N)| ≤ |X_{k+1}(N)|` holds with 0 counterexamples (`d ≥ 2`), and the bipartite incidence is full rank in every case (verified via the global INJ check on `L`).

### 6.3 Why X-restriction is natural

For a matroid `N` with `n' = 2k+d`:

- A subset `A ⊆ E` is in `X_k(N)` iff `|A| = k`, A is independent in N, AND `E \ A` is independent in N.
- By matroid duality, "`E \ A` independent in `N`" is equivalent to "`A` spans `N*`" (= `A` contains a basis of the dual matroid `N*`).
- Thus `X_k(N)` is the set of `k`-element subsets that are simultaneously **independent in `N` and spanning in `N*`** — a "doubled" matroid condition.

By complementation `A ↔ E \ A`, the cardinalities are palindromic: `|X_j(N)| = |X_{n'-j}(N)|` for all `j`. So the X-vector is invariant under `j \mapsto n' - j` and is unimodal-conjecturally with peak at `n'/2`.

The X-vector and its bipartite incidence are not directly addressed by Mason / AHK / Brändén–Huh / ALOGV in the existing literature. **Theorem 4' is a new statement in matroid theory**, requiring a proof that engages with the "doubled" structure (= matroid intersection of `N` and `N*`).

## 7. Proof of Theorem 1 modulo Theorem 4'

*Proof.* Let `v \in S_{-d}(M)` with `L(v) = 0` and `d \geq 2`. Decompose `v = \sum_{(C, U)} v_{C, U}` along the orbit decomposition of §4. Since `L` preserves each orbit (Lemma 1), `L(v_{C, U}) = 0` for each `(C, U)`. By Proposition 3, `L|_{k\langle X_k(N(C,U)) \rangle}` is identified with the operator of Theorem 4', and by that theorem is injective. Hence `v_{C, U} = 0` for each `(C, U)`, and `v = 0`. ∎

## 8. Examples and computational verification

We checked Theorem 1 directly (via mod-`p` Gaussian elimination on `L` for `p = 10007` and `p = 100003`) for:

- All uniform matroids `U_{r, n}` with `r \leq 10`, `n \leq 12`.
- All graphic matroids `M(K_n)` for `n \leq 6`.
- Fano `F_7`, non-Fano `F_7^-`, Pappus, non-Pappus, Vamos `V_8` (non-realizable), `AG(3, 2)`.

In each case, `L` was confirmed injective at every `d \geq 2`. The data is consistent with the cleaner statement: the smallest nonzero eigenvalue of `L^T L` is a positive integer, with multiplicities encoding the Lefschetz-decomposition primitive classes. For example, for `M(K_5)` at the bigrade `(m, d) = (2, 2)`, the smallest eigenvalue is `1` with multiplicity `180` — exactly equal to the cokernel dimension of the (non-injective) `L^2 : S_{-2} \to S_2` map on the same block.

### 8.1 Per-orbit verification of Theorem 4' (the central lemma)

In addition we verified at the *orbit* level, on every orbit of `M(K_n)` for `n \leq 6`, Vámos, AG(3,2), Fano, Pappus, NonPappus, at every bigrade with `d \geq 2`:

(i) The orbit-size formula `|\widehat{O}_{C,U}| = |X_{m - |C|}(N(C, U))|` (Lemma 2's bijection): 100% match.

(ii) `|X_k(N)| \leq |X_{k+1}(N)|` (the dim-consistency input to Theorem 4'): **0 violations** across more than `2 \times 10^5` orbits.

(iii) The classical inequality `f_k(N) \leq f_{k+1}(N)` (Mason-style): holds for the vast majority of orbits, **but fails on 2820 of 107445 orbits at `M(K_6), (m, d) = (3, 2)`**. The failing orbits all carry parallel-pair structure in `N(C, U)`. On the failing orbits the X-restriction (ii) nonetheless holds with comfortable slack.

This separates Theorem 4' from a direct corollary of Mason's theorem: it is a strictly stronger statement, and the parallel-rich case (§6.1) is where the X-restriction does real work.

## 9. Discussion

### 9.1 The Aut(M)-equivariance is automatic

`L` is `\text{Aut}(M)`-equivariant by construction (it is the canonical diagonal Casimir element). Theorem 1 gives a strict-injection of `\text{Aut}(M)`-representations, so its cokernel `[f_{m+1}]^2 - [f_m] \cdot [f_{m+2}]` is automatically an effective representation. No "equivariant Hodge–Riemann" or "equivariant Lorentzian" theory is needed.

### 9.2 What about `d = 1`?

For `d = 1`, Theorem 1's statement holds for uniform matroids (and direct sums thereof) but fails for matroids with rank-2 lines of size ≥ 3 (e.g., M(K_4)). The failure is structural: at `d = 1` the orbit decomposition has `n' = 2k + 1`, and the level `k` and `k+1` cross the f-vector peak. So the matroid-level operator can fail to be injective. The ELC consequence at `d = 1` is trivial (`[f_{m+1}] \cdot [f_m] \geq [f_{m+1}] \cdot [f_m]`), so this case is not needed.

### 9.3 The `L^2` and higher Lefschetz powers

The map `L^d : S_{-d} \to S_d` is *not* in general an isomorphism (we verified this computationally; first counterexample is M(K_5) at `d = 2`, with a 180-dimensional cokernel). So a strict "hard Lefschetz package" is absent. Nonetheless, our injectivity-only Theorem 1 is sufficient for ELC.

### 9.4 Related work

The ALOGV / Brändén–Huh framework was developed for very different applications (matroid bases-exchange mixing, Mason's conjecture, Mihail–Vazirani). Our contribution is the *orbit-reduction* of an `\text{Aut}(M)`-equivariant tensor Lefschetz statement to a per-orbit matroid level-walk statement. The reduction is essentially a (covariant–contravariant) Künneth-with-constraint observation; once made, the proof is a direct invocation of classical matroid incidence theory.

## 10. Open questions

1. **Quantitative version.** Theorem 1 gives `L^T L \succ 0`. Computational evidence (eigenvalue 1 always present with controlled multiplicity) suggests `L^T L \succeq I` with explicit "primitive class" eigenspaces. Can one give a clean description of these primitive classes as matroid invariants?

2. **Hard Lefschetz on a sub-quotient.** The 180-dim primitive class for M(K_5) at `(2, 2)` is an `\text{Aut}(M(K_5)) = S_5` representation. What is its irrep decomposition? More generally, are these primitive classes a new family of natural matroid invariants?

3. **Strong / induced ELC.** Following Gao–Li–Xie–Yang–Zhang, can one prove the *strong* ELC `\text{Ind}_{S_{2m+2}}^{S_m \times S_{m+2}} ([f_m] \otimes [f_{m+2}]) \leq \text{Ind}_{S_{2m+2}}^{S_{m+1} \times S_{m+1}} [f_{m+1}]^2` from our setup? This would refine Theorem 1.

## References

- D. Anari, K. Liu, S. Oveis Gharan, C. Vinzant, *Log-concave polynomials, II,III,IV*, FOCS 2019 / Annals 2024.
- P. Brändén, J. Huh, *Lorentzian polynomials*, Ann. of Math. 192 (2020).
- K. Adiprasito, J. Huh, E. Katz, *Hodge theory for combinatorial geometries*, Ann. of Math. 188 (2018).
- T. Karn, M. Wakefield, *Equivariant Kazhdan–Lusztig theory of paving matroids*, Alg. Comb. (2024).
- J. Matherne, D. Miyata, N. Proudfoot, E. Ramos, *Equivariant log concavity and representation stability*, IMRN (2023).

## Acknowledgements

[…]
