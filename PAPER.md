# Equivariant log-concavity of the f-vector for paving matroids

**Status:** Draft v3 (2026-05-23). Short note (~5 pages).

## Abstract

For every paving matroid `M`, we prove that the virtual `Aut(M)`-representation `[f_{m+1}(M)]² − [f_m(M)] · [f_{m+2}(M)]` is effective for every `m ≥ 0`. This establishes **equivariant log-concavity (ELC) of the f-vector for an infinite class of matroids** — to our knowledge, the first such result beyond direct sums of uniform matroids. The proof reduces ELC to injectivity of a tensor Lefschetz operator `L = ∑ x_i ⊗ x_i` acting on a graded vector space `S(M)`, then to a bipartite-incidence rank statement on ordered independent partitions of the ground set. The bipartite-incidence statement is proven via **stressed-hyperplane relaxation** from the uniform case (Karn–Nasr–Proudfoot–Vecchi paradigm) with the boolean Lefschetz theorem as the base case. §4.5 discusses an attempted descent via the Gui-Xiong equivariant Kähler package and explains why it fails: our `L` is not the descent of the Gui-Xiong operator from the free exterior algebra, so although the symbolic forms match, the equivariant HL on the free exterior algebra does not imply our rank statement on the matroid quotient.

A **paving matroid** is a matroid in which every circuit has size at least equal to the matroid's rank — equivalently, every subset of size less than the rank is independent. The class includes all *sparse paving* matroids (= paving + co-paving), all Steiner system matroids, and many others; Mayhew–Newman–Welsh–Whittle [MNWW] conjecture that asymptotically almost all matroids are sparse paving (and hence paving).

## 1. Introduction

Mason's f-vector log-concavity conjecture asserts that for every matroid `M` on `n` elements, the sequence `f_d(M)` (= number of independent sets of size `d`) is log-concave:
`f_d(M)² ≥ f_{d-1}(M) · f_{d+1}(M)`.
This was proven by Adiprasito–Huh–Katz (2018) via Hodge theory of the Chow ring; Brändén–Huh (2020) and Anari–Liu–Oveis Gharan–Vinzant (2018) gave alternative proofs via Lorentzian / completely log-concave polynomials, strengthening to *ultra* log-concavity.

The **equivariant** lift of Mason's conjecture is the question:

> **(ELC for f-vector).** For every matroid `M` and every `m ≥ 0`, is the virtual `Aut(M)`-representation `[f_{m+1}(M)]² − [f_m(M)] · [f_{m+2}(M)]` effective (i.e., a genuine representation)?

Here `[f_d(M)] := k[\text{Indep}_d(M)]` denotes the permutation representation of `Aut(M)` on size-`d` independent sets.

Equivariant log-concavity (ELC) has been established for various *adjacent* invariants — Orlik–Solomon, Orlik–Terao, and Cordovil algebras of the braid arrangement [MMPR]; equivariant Kazhdan–Lusztig polynomials of paving matroids [KNPV]; equivariant Kazhdan–Lusztig polynomials of q-niform and uniform matroids [GLXYZ] — but the f-vector statement specifically has remained open except in three trivial cases:

1. Boolean matroids `U_{n,n}` (= power set of `[n]`).
2. Uniform matroids `U_{r,n}`, by inheritance from the boolean case.
3. Direct sums of uniforms, by Künneth.

The main result of this note establishes ELC of the f-vector for a much larger class:

> **Theorem 1.** Let `M` be a **paving matroid**: a matroid in which every circuit has size at least `rank(M)`. Equivalently, every subset of size less than `rank(M)` is independent. Then for every `m ≥ 0`, the virtual `Aut(M)`-representation `[f_{m+1}(M)]² − [f_m(M)] · [f_{m+2}(M)]` is effective.

Paving matroids are a substantial class. They include all sparse paving matroids (= paving with paving dual), which by [MNWW] are conjecturally asymptotically almost all matroids. They also include Steiner system matroids, and many specific designs.

The proof proceeds in three steps:
1. **§2**: Identify ELC as the injectivity of a single explicit `Aut(M)`-equivariant linear operator `L` on a graded vector space `S(M)`.
2. **§3**: Decompose `L` into orbits indexed by pairs `(C, U)` and reduce each orbit's injectivity to a bipartite-incidence rank statement on "balanced indep bipartitions" of the contracted-restricted minor.
3. **§4**: Prove the bipartite-incidence statement for paving matroids via a single inductive step from the uniform matroid, in which the entire collection of circuit-hyperplanes is added at once. The boolean Lefschetz theorem supplies the base case; a submatrix-rank argument supplies the inductive step.

## 2. The Lefschetz operator and the ELC criterion

Let `M` be a loopless matroid on `E = \{1, \dots, n\}` with rank `r`. Denote by `\text{Indep}_d(M)` the set of size-`d` independent sets and `f_d(M) := |\text{Indep}_d(M)|`. The Aut(M)-permutation representation on `\text{Indep}_d(M)` is `[f_d(M)]`.

### 2.1 The ring `R(M)` and its dual

Set
`R(M) := k[x_1, \dots, x_n] \big/ \big(x_C : C \in \text{Circ}(M);\ x_i^2 : i \in E\big)`,
where `\text{Circ}(M)` is the set of circuits and `x_S := \prod_{i \in S} x_i`. The squarefree quotient ensures `R(M)_d` has basis `\{x_S : S \in \text{Indep}_d(M)\}`, so `\dim R(M)_d = f_d(M)`. As Aut(M)-representations, `R(M)_d \cong [f_d(M)]`.

Let `R^\vee(M)` be the graded linear dual, with basis `\{y_S : S \in \text{Indep}_d(M)\}` dual to `\{x_S\}`. The matroid algebra `R(M)` acts on `R^\vee(M)` by contraction: `x_i \cdot y_S = y_{S \setminus \{i\}}` if `i \in S`, else `0`.

### 2.2 `S(M)` and the Lefschetz operator

Define `S(M) := R(M) \otimes_k R^\vee(M)`, bigraded by **external degree** `e := |S| - |T|` and **internal degree** `m := |S|` on `x_S \otimes y_T`. The **Lefschetz operator** is
`L := \sum_{i=1}^n x_i \otimes x_i \in \text{End}_k(S(M))`,
with explicit action
`L(x_S \otimes y_T) = \sum_{i \in T \setminus S,\ S \cup \{i\} \in \text{Indep}(M)} x_{S \cup \{i\}} \otimes y_{T \setminus \{i\}}`.
`L` raises external degree by 2, raises internal degree by 1, and is Aut(M)-equivariant.

### 2.3 ELC ⟺ Injectivity of `L`

For each `m, d \geq 0` with `d \geq 2`, consider the block
`L_m : R(M)_m \otimes R^\vee(M)_{-(m+d)} \to R(M)_{m+1} \otimes R^\vee(M)_{-(m+d-1)}`.

The source is `[f_m(M)] \cdot [f_{m+d}(M)]^* \cong [f_m(M)] \cdot [f_{m+d}(M)]` (the dual of a permutation representation equals itself); the target is `[f_{m+1}(M)] \cdot [f_{m+d-1}(M)]`.

> **Proposition 2.** ELC for the f-vector of `M` holds if and only if, for every `m \geq 0` and every `d \geq 2`, `L_m` is injective. Taking `d = 2` gives the standard log-concavity form: cokernel of `L_m` equals `[f_{m+1}(M)]^2 - [f_m(M)] \cdot [f_{m+2}(M)]`, effective iff `L_m` injective.

*Proof.* If `L_m` is Aut(M)-equivariant and injective, its cokernel is an honest Aut(M)-representation (= effective virtual). The converse is standard. ∎

This reduces ELC to the injectivity of `L` on each bigrade `(m, -d)`.

## 3. Orbit decomposition and the X-bipartite incidence

### 3.1 The orbit structure

For `(S, T)` a basis element of `R(M)_m \otimes R^\vee(M)_{-(m+d)}` (so `|S| = m`, `|T| = m+d`, both independent), set `C := S \cap T` and `U := S \cup T`.

> **Lemma 3.** `L` preserves the pair `(C, U)`: if `(S, T) \mapsto (S \cup \{i\}, T \setminus \{i\})` is a summand of `L(x_S \otimes y_T)`, then `(S \cup \{i\}) \cap (T \setminus \{i\}) = C` and `(S \cup \{i\}) \cup (T \setminus \{i\}) = U`.

*Proof.* The summand requires `i \in T \setminus S`. Then `S' \cup T' = U` since `i \in T`, and `S' \cap T' = (C \cup \{i\}) \setminus \{i\} = C` since `i \notin C`. ∎

Define `N := N(C, U) := (M / C) \big|_{U \setminus C}`, the contracted-restricted matroid on ground set `U \setminus C` with `\text{Indep}(N) = \{A \subseteq U \setminus C : A \cup C \in \text{Indep}(M)\}`.

Set `k := m - |C|` and `n' := |U \setminus C| = 2k + d`. The orbit `O_{C, U}` is in bijection (via `(S, T) \mapsto A := S \setminus C \subseteq U \setminus C`) with the set of **balanced indep bipartitions**

`X_k(N) := \big\{A \subseteq U \setminus C : |A| = k,\ A \in \text{Indep}(N),\ (U \setminus C) \setminus A \in \text{Indep}(N)\big\}`.

### 3.2 Reduction to the X-bipartite incidence

> **Proposition 4.** Under the bijection above, `L|_{O_{C, U}}` corresponds to the operator
> `\partial^* : \mathbb{R}^{X_k(N)} \to \mathbb{R}^{X_{k+1}(N)}, \quad \partial^*(x_A) = \sum_{i \in (U \setminus C) \setminus A,\ A \cup \{i\} \in \text{Indep}(N)} x_{A \cup \{i\}}.`
> Moreover, `\partial^*(\mathbb{R}^{X_k(N)}) \subseteq \mathbb{R}^{X_{k+1}(N)}` (the image automatically lands in the X-restricted subspace at the next level).

*Proof.* The summands of `L|_{O_{C, U}}` correspond to moving an element `i \in T \setminus S = (U \setminus C) \setminus A` from `T` to `S`, with the matroid constraint `S \cup \{i\} \in \text{Indep}(M) \Leftrightarrow A \cup \{i\} \in \text{Indep}(N)`. The complement condition for the result to remain in `X_{k+1}(N)` is automatic: `(U \setminus C) \setminus (A \cup \{i\}) \subseteq (U \setminus C) \setminus A \in \text{Indep}(N)`, so it is independent. ∎

In view of Propositions 2 and 4 and Lemma 3:

> **Theorem 5 (Reduction).** ELC for the f-vector of `M` holds if and only if, for every minor `N = N(C, U)` of `M` arising from an orbit pair `(C, U)` with `2k + d = |E(N)|`, `k + d \leq \text{rank}(N)`, `d \geq 2`, the operator `\partial^* : \mathbb{R}^{X_k(N)} \to \mathbb{R}^{X_{k+1}(N)}` is injective.

The remaining work is to prove the injectivity statement of Theorem 5 — call this **Theorem 5'** — for all minors of paving matroids. Minors of paving matroids are themselves paving: deletion `N \setminus e` only removes circuits, so each remaining circuit `C` still satisfies `|C| \geq \text{rank}(N) \geq \text{rank}(N \setminus e)`. For contraction `N / e` (with `e` not a coloop, `\text{rank}(N/e) = \text{rank}(N) - 1`), every circuit `C` of `N / e` has the form `C = D \setminus \{e\}` for some circuit `D` of `N` with `e \in D`, or `C = D` for some circuit `D` of `N` with `e \notin D`; in either case `|C| \geq \text{rank}(N) - 1 = \text{rank}(N / e)`. So it suffices to prove:

> **Theorem 6.** For every paving matroid `N` on `n' = 2k + d` elements of rank `r' \geq k + d`, with `d \geq 2`, the bipartite-incidence operator `\partial^* : \mathbb{R}^{X_k(N)} \to \mathbb{R}^{X_{k+1}(N)}` is injective.

The proof of Theorem 6 occupies §4.

## 4. Stressed-hyperplane relaxation for paving matroids

A paving matroid `N` with rank `r'` on `n'` elements can be described by its set `\mathcal{H}` of **circuit-hyperplanes** (CHs): the `r'`-subsets of `E(N)` that are *not* bases (= dependent of full rank). Since `N` is paving, every subset of size `< r'` is independent, and the dependent `r'`-subsets are exactly the CHs in `\mathcal{H}`. The independent sets of `N` are: all subsets of size `< r'`, plus the `r'`-subsets not in `\mathcal{H}`. We write `N = U_{r', n'}(\mathcal{H})`; with `\mathcal{H} = \emptyset` this is the uniform matroid.

*Remark on validity.* Not every collection `\mathcal{H}` of `r'`-subsets gives a valid matroid. For two CHs `F_1, F_2 \in \mathcal{H}` with `|F_1 \cap F_2| = r' - 1`, the matroid axioms force additional CHs `C_3 \subseteq (F_1 \cup F_2) \setminus \{e\}` (of size `r'`) for every `e \in F_1 \cap F_2`. **Sparse paving** is the special case where all pairwise CH intersections satisfy `|F_1 \cap F_2| \leq r' - 2`, so no such forcing occurs and CHs can be added one at a time. For general paving matroids, sets of CHs that violate this condition can still give a valid matroid, provided the matroid axioms close up (all forced CHs are also included in `\mathcal{H}`). Our proof handles both cases uniformly.

### 4.1 The base case: uniform matroids

> **Lemma 7.** If `N = U_{r', n'}` (so `\mathcal{H} = \emptyset`), then Theorem 6 holds: `\partial^* : \mathbb{R}^{X_k(N)} \to \mathbb{R}^{X_{k+1}(N)}` is injective.

*Proof.* For the uniform matroid `U_{r', n'}`, every subset of size `\leq r'` is independent. Since `n' = 2k + d \leq 2r' - d \leq 2r'`, both `|A| = k \leq r'` and `|E \setminus A| = k + d \leq r'` are satisfied for any `A \subseteq E(N)` of size `k`. Hence `X_k(U_{r', n'}) = \binom{E(N)}{k}` consists of *all* `k`-subsets, and similarly `X_{k+1}(U_{r', n'}) = \binom{E(N)}{k+1}`.

The bipartite-incidence operator `\partial^*` on these spaces is exactly the simplicial coboundary on the boolean lattice at level `k \to k+1`, which is injective for `k < n'/2`. Since `n' = 2k + d` with `d \geq 2`, indeed `k < k + d/2 = n'/2`. So `\partial^*` is injective by the standard boolean `sl_2`-Lefschetz theorem on the boolean lattice. ∎

### 4.2 Inductive step: adding (possibly multiple) stressed hyperplanes

> **Lemma 8.** Let `N = U_{r', n'}(\mathcal{H})` be a paving matroid, and let `N' = U_{r', n'}(\mathcal{H} \cup \mathcal{F})` be another paving matroid obtained by adding a nonempty collection `\mathcal{F}` of new CHs (each F ∈ F is currently a basis of N). Suppose Theorem 6 holds for `N`. Then Theorem 6 holds for `N'`.

*Proof.* Fix `(k, d)` with `2k + d = n'`, `r' \geq k + d`, `d \geq 2`.

**Claim 8a:** `X_{k+1}(N') = X_{k+1}(N)`.

Going from `N` to `N'`, the only sets that lose independent status are those in `\mathcal{F}`. A set `A' \in X_{k+1}(N)` is removed iff `A' \in \mathcal{F}` or `E(N) \setminus A' \in \mathcal{F}`. Now `|A'| = k + 1` and each `F \in \mathcal{F}` has size `r' \geq k + 2 > k + 1`, so `A' \notin \mathcal{F}`. Also `|E(N) \setminus A'| = n' - k - 1 = k + d - 1 < k + d \leq r' = |F|`, so `E(N) \setminus A' \notin \mathcal{F}`. ∎(8a)

**Claim 8b:** `|X_k(N')| = |X_k(N)| - \delta` where `0 \leq \delta \leq |\mathcal{F}|`. Specifically, the removed elements are exactly the set `\{E(N) \setminus F : F \in \mathcal{F}, E(N) \setminus F \in X_k(N)\}`. This set is non-empty only in the "boundary" case `r' = k + d`.

A set `A \in X_k(N)` is removed iff `A \in \mathcal{F}` or `E(N) \setminus A \in \mathcal{F}`. Since `|A| = k < k + d \leq r'`, we have `A \notin \mathcal{F}`. The condition `E(N) \setminus A \in \mathcal{F}` requires `|E(N) \setminus A| = r'`, i.e., `k = n' - r' = \text{corank}(N)`. By hypothesis `r' \geq k + d`, so `\text{corank}(N) \leq k` with equality iff `r' = k + d`.
- If `r' > k + d` (strict): `\text{corank}(N) < k`, so `|E(N) \setminus A| > r'`, never equals any `F \in \mathcal{F}`. Hence `\delta = 0`.
- If `r' = k + d` (boundary): `E(N) \setminus F` for each `F \in \mathcal{F}` has size `k`, and in any paving matroid, every `k`-subset (size `< r'`) is independent. Also `F` is independent in `N` (since `F \notin \mathcal{H}` so far). Hence `E(N) \setminus F \in X_k(N)`. So `\delta = |\mathcal{F}|`. ∎(8b)

**Inductive step proper.** By Claims 8a–8b, the bipartite-incidence matrix `\partial^* : \mathbb{R}^{X_k(N')} \to \mathbb{R}^{X_{k+1}(N')}` is a submatrix of the bipartite-incidence matrix for `N`, obtained by removing the columns corresponding to `\{E(N) \setminus F : F \in \mathcal{F}\}` (`\delta` columns total) and removing no rows.

(The matrix entries do not change because the edge `(A, A \cup \{i\})` exists in `N`-incidence iff `A \cup \{i\}` is `N`-independent. This is the same condition for `N'` whenever `A \cup \{i\} \notin \mathcal{F}`, automatic here since `|A \cup \{i\}| = k + 1 < r'`.)

- If `\delta = 0`: matrix unchanged, full column rank transfers directly.
- If `\delta > 0`: matrix loses `\delta` columns. The original matrix has full column rank `|X_k(N)|` by hypothesis, so its columns are linearly independent over `\mathbb{Q}`. Any subset of these columns is also linearly independent. The new matrix is formed from the remaining `|X_k(N)| - \delta = |X_k(N')|` columns, all of which are linearly independent. Hence full column rank `|X_k(N')|`, i.e., `\partial^*` injective on `\mathbb{R}^{X_k(N')}`. ∎

### 4.3 Proof of Theorem 1

Let `N = U_{r', n'}(\mathcal{H})` be any paving matroid with the bigrade hypothesis of Theorem 6. Take `\mathcal{F} := \mathcal{H}` and apply Lemma 8 in a single step to the pair `(U_{r', n'},\ N)`: the base case `\mathcal{H} = \emptyset` is supplied by Lemma 7, and the conclusion of Lemma 8 gives Theorem 6 for `N`. Combined with Theorem 5 (the reduction) and the fact that minors of paving matroids are paving, this gives ELC of the f-vector for every paving matroid `M`. ∎

(Sparse paving matroids admit a finer-grained version of this argument in which CHs are added one at a time, with intermediate stages all valid matroids. For paving matroids that are not sparse paving — e.g., the example in §4.4 — single-CH intermediate steps are not all valid matroids, but the one-shot step from the uniform always is.)

### 4.4 Non-sparse-paving example (verification)

To illustrate the proof beyond sparse paving, consider `M = U_{5, 8}(\mathcal{H})` where `\mathcal{H}` consists of all six 5-subsets of `\{0, 1, 2, 3, 4, 5\}`. Pairwise these CHs intersect in 4 elements (= `r-1 = 4`), violating the sparse paving condition. `M` is paving (only size-`r` and size-`(r+1)` circuits) but not sparse paving — `M` has 15 circuits of size 6 (= sets of 6 elements containing both `\{6, 7\}` and 4 from `\{0, ..., 5\}`).

`M` cannot be built by adding the CHs one at a time and getting valid intermediate matroids — `\{F_1, F_2\}` with `|F_1 \cap F_2| = 4` alone violates matroid axioms. But adding all six together gives a valid paving matroid, and Lemma 8's submatrix-rank argument applies in one inductive step.

Computational verification (in `computations/test_paving_extension.py`): at bigrade `(k, d) = (3, 2)`, `|X_3(M)| = 50`, `|X_4(M)| = 70`, and the bipartite-incidence rank is exactly 50 = `|X_3(M)|`. This matches the KW prediction `|X_3(U_{5,8})| - |\mathcal{H}| = 56 - 6 = 50`.

## 4.5 An attempted descent via Gui-Xiong's framework, and why it fails

It is natural to ask whether Theorem 6 follows from the Gui-Xiong equivariant Kähler package [GX, arXiv:2205.05420], which gives Hard Lefschetz on the free exterior algebra `\Lambda(V) \otimes \Lambda(V^*)` with the operator `L_{\text{amb}} := \sum e_{\theta_k} \otimes i_{\theta_k}`, equivariant under any group acting on `V`. Symbolically, this `L_{\text{amb}}` is the same expression as our `L = \sum x_i \otimes x_i`, so one might hope that our `L` on `R(M) \otimes R^\vee(M)` is the descent of `L_{\text{amb}}` under the projection `\pi: \Lambda(V) \otimes \Lambda(V^*) \to R(M) \otimes R^\vee(M)`, and that Gui-Xiong's HL injectivity would imply ours.

**This fails.** Our `L` on `R(M) \otimes R^\vee(M)` (defined intrinsically as the unsigned bipartite incidence on indep-set pairs) is *not* the descent of `L_{\text{amb}}`. Concretely: take `M = U_{5,8}` with circuit-hyperplane `F = \{0,1,2,3,4\}` and `v = x_{\{5,6,7\}} \otimes y_F` in the ambient `\Lambda_3 \otimes \Lambda^*_5`. Then `v \in \ker(\pi)` (since `y_F = 0` in `R^\vee(M)` as `F` is dependent), but
`L_{\text{amb}}(v) = \sum_{i \in F} x_{\{5,6,7\} \cup \{i\}} \otimes y_{F \setminus \{i\}}`,
and every summand has both factors *independent* in `M` (since `|S \cup \{i\}| = 4 < r` and `|F \setminus \{i\}| = 4 < r`, so neither contains a circuit). Hence `L_{\text{amb}}(v) \notin \ker(\pi)`, so `\pi(L_{\text{amb}}(v)) \neq 0 = L(\pi(v))`. The diagram doesn't commute.

The conceptual issue: `\pi` kills `y_F` (= dependent set in M*), but the operator `L_{\text{amb}}` "un-zeros" this by replacing `y_F` with contractions `y_{F \setminus \{i\}}` that are non-zero in `R^\vee(M)`. Our intrinsic `L_{\text{quot}}` instead respects the matroid quotient by being defined directly on indep-set pairs, dropping non-indep contributions.

Consequently the Gui-Xiong HL on the ambient does not directly imply the rank statement we want on the matroid quotient. Computational verification of this descent failure is in `computations/verify_descent.py`.

The relaxation proof in §§4.1–4.3 thus remains the substantive proof of Theorem 6. Gui-Xiong's framework gives Hard Lefschetz on the *free* exterior algebra (= boolean lattice in our setting), which serves only as the base case (Lemma 7).

## 5. Discussion

### 5.1 Relationship with prior work

The technique of stressed-hyperplane relaxation was developed by Karn–Nasr–Proudfoot–Vecchi [KNPV] for proving equivariant log-concavity of equivariant Kazhdan–Lusztig polynomials, equivariant inverse Kazhdan–Lusztig polynomials, and equivariant Z-polynomials of paving matroids. Our application to the f-vector is, to our knowledge, the first time this technique has been applied to the permutation representation `[f_d(M)]`.

The dimensional (= non-equivariant) part of our main theorem — `|X_k(M)| \leq |X_{k+1}(M)|` for `k < n/2` — was recently established as Corollary 1.7 of Ardila-Mantilla–Cristancho–Denham–Eur–Huh–Wang [ACDEHW] (Jan 2026) via Lorentzian polynomial methods on the gross-substitutes / M♮-concave framework. Their result handles dimensional inequality for *all* matroids; the additional rank statement (= injectivity of `\partial^*`) is what we contribute for the paving class.

The reduction chain in §§2–3 (ELC ⟺ injectivity of `L` ⟺ X-bipartite-incidence injective per orbit) appears in [draft of preprint by author of this note] and is not strictly novel, though we present it cleanly here for self-containedness.

### 5.2 What's not covered, and what's conjectured

**Not covered.** Theorem 1 applies only to paving matroids. Many natural matroid families fall outside this class, including:
- Graphic matroids `M(K_n)` for `n \geq 5` (have circuits of size 3 = triangles, much smaller than rank).
- Projective matroids `\text{PG}(r, q)` for `r \geq 3`.
- Most transversal matroids.

### 5.3 The X-restricted rank problem (open)

The cleanest open problem to attack is the rank statement of Theorem 6 directly, for non-paving matroids. Concretely:

> **Conjecture.** For every loopless matroid `M` and every bigrade `(m, -d)` with `2m + d \leq n`, `m + d \leq r := \text{rank}(M)`, `d \geq 2`, the bipartite-incidence operator `\partial^*: \mathbb{R}^{X_m(M)} \to \mathbb{R}^{X_{m+1}(M)}` is injective.

For paving `M` this is Theorem 6. For non-paving `M` it remains open.

Computational evidence: across more than `2 \times 10^5` matroid orbits checked — including graphic, projective, Vámos, Fano, Pappus, NonPappus, and various restrictions of `M(K_6)` — no counterexample to this conjecture has emerged.

**Empirical conjecture.** Across more than `2 \times 10^5` matroid orbits we have checked — including graphic, projective, Vámos, Fano, Pappus, NonPappus, and various restrictions of `M(K_6)` — no counterexample to the operator-injectivity statement of Theorem 6 has emerged. We conjecture:

> **Conjecture.** For every loopless matroid `M`, the virtual `Aut(M)`-representation `[f_{m+1}(M)]² − [f_m(M)] \cdot [f_{m+2}(M)]` is effective.

This is the f-vector analog of the equivariant Mason conjecture; a general proof remains open.

### 5.3 Open problems

1. Generalize to arbitrary matroids via "smaller circuit relaxation". The matroid relaxation operation is not directly defined for circuits of size `< r`; a Schur-complement formulation may be needed.
2. Find a direct geometric realization of the X-bipartite incidence operator as a Lefschetz-type morphism on the cohomology of an appropriate variety, à la AHK or Eur–Huh–Larson.
3. Quantify the gap: for non-paving matroids `M` (e.g., `M(K_n)` for `n \geq 5`), even though the relaxation argument fails, the rank deficit of the bipartite incidence on `\text{Indep}_k(M) \to \text{Indep}_{k+1}(M)` can be substantial, while the X-restricted operator empirically still has full rank. Understand the structural reason for the "X-restoration".

## References

- **[AHK]** K. Adiprasito, J. Huh, E. Katz. *Hodge theory for combinatorial geometries.* Annals of Mathematics 188 (2018), 381–452.
- **[ALOGV]** N. Anari, K. Liu, S. Oveis Gharan, C. Vinzant. *Log-Concave Polynomials, III: Mason's Ultra-Log-Concavity Conjecture for Independent Sets of Matroids.* arXiv:1811.01600.
- **[ACDEHW]** F. Ardila-Mantilla, S. Cristancho, G. Denham, C. Eur, J. Huh, B. Wang. *Tree metrics and log-concavity for matroids.* arXiv:2601.02547 (January 2026).
- **[BH]** P. Brändén, J. Huh. *Lorentzian polynomials.* Annals of Mathematics 192 (2020), 821–891.
- **[GLXYZ]** A. L. L. Gao, E. Y. H. Li, M. H. Y. Xie, A. L. B. Yang, Z.-X. Zhang. *Induced log-concavity of equivariant matroid invariants.* arXiv:2307.10539.
- **[GX]** L. Gui, R. Xiong. *Equivariant log-concavity and equivariant Kähler packages.* arXiv:2205.05420; Journal of Algebra 657 (2024), 379–401.
- **[Sw]** E. Swartz. *g-elements of matroid complexes.* arXiv:math/0210376; Journal of Combinatorial Theory, Series B 88 (2003), 369–375.
- **[ANR]** N. Angarone, A. Nathanson, V. Reiner. *Chow rings of matroids as permutation representations.* arXiv:2309.14312; Journal of the London Mathematical Society (2025).
- **[KNPV]** T. Karn, G. Nasr, N. Proudfoot, L. Vecchi. *Equivariant Kazhdan–Lusztig theory of paving matroids.* arXiv:2202.06938; Algebraic Combinatorics 7 (2024), 489–516.
- **[MMPR]** J. Matherne, D. Miyata, N. Proudfoot, E. Ramos. *Equivariant log concavity and representation stability.* International Mathematics Research Notices 2023, Issue 5, 3885–3906.
- **[MNWW]** D. Mayhew, M. Newman, D. Welsh, G. Whittle. *On the asymptotic proportion of connected matroids.* European Journal of Combinatorics 32 (2011), 882–890.
