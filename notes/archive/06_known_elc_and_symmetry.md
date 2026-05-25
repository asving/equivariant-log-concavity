# 06. Known Equivariant Log-Concavity Results and Symmetric Matroids

Survey for the QLC project. The target conjecture is ELC for the
permutation rep `[f_k]` on size-k independent sets of M, i.e.
effectivity of `[f_{k+1}]^2 - [f_k][f_{k+2}]` as an Aut(M)-rep.

---

## Section 1 — Known equivariant log-concavity results

### 1.1 Matherne–Miyata–Proudfoot–Ramos (arXiv:2104.00715, IMRN 2023)
"Equivariant log concavity and representation stability."

- Conjectures equivariant log-concavity for three matroid/arrangement
  rings: the **Orlik–Solomon (OS) algebra** of any matroid, the
  **Cordovil algebra** of an oriented matroid, and the **Orlik–Terao
  (OT) algebra** of a (real or complex) hyperplane arrangement. These
  are the standard "no-broken-circuit" / "reciprocal plane" rings, NOT
  the f-vector of independent sets we study.
- Their notion of strong equivariant log-concavity (sELC): the virtual
  rep `[A_{k+1}]^2 − [A_k][A_{k+2}]` is effective for the graded
  components, and a refined "induced" version using
  `Ind^{S_{2k+2}}_{S_{k+1} x S_{k+1}}` etc.
- Main proven case (**Theorem 1.4**): the **Coxeter / braid
  arrangement of type A_{n−1}** (i.e. the matroid of the complete
  graph K_n, with S_n acting) satisfies their conjectures for OS, OT,
  and Cordovil. Proof uses **FI-module / representation stability**
  machinery (Sam–Snowden, Church–Ellenberg–Farb) plus a finite
  computer verification in low degree; stability propagates to all n.
- They do NOT settle other infinite families; the OS-conjecture for a
  general matroid is open.
- **Relevance to us:** the *machinery* (FI-modules + finite check)
  transfers to our setting in principle, but the *ring* is different.
  OS / OT are the "broken-circuit" complex world; ours is the full
  independence complex (f-vector). The non-equivariant log-concavity
  of OS is much more elementary than Mason's conjecture.

### 1.2 Equivariant KL polynomials (Gedeon–Proudfoot–Young, Proudfoot, et al.)

- **Gedeon–Proudfoot–Young (1605.01777, "Equivariant KL polynomial of
  a matroid", 2016):** define `P^G_M(t)` as a polynomial in the
  Grothendieck ring of virtual G-reps. Compute closed form for
  **uniform matroids U_{r,n} (G=S_n)** and small-rank braid matroids.
- **Proudfoot (1808.07855, "Equivariant KL polynomials of q-niform
  matroids", Alg. Comb. 2019):** for **U_{n,m}(q)** (the q-analog of
  uniform; the matroid of all hyperplanes in F_q^n), the equivariant
  KL polynomial under GL_n(F_q) is the unipotent q-analog of the
  uniform case. This is the natural projective-geometry analog.
- **Karn–Wakefield ("Equivariant KL theory of paving matroids",
  Algebraic Combinatorics, 10.5802/alco.281):** describes how
  equivariant KL polynomials transform under stressed-hyperplane
  relaxation, giving an inductive computation for **all paving
  matroids** equipped with their full symmetry. Reduces to sparse
  paving + uniform.
- **Ferroni–Larson (2303.02253, "KL polynomials of braid matroids"):**
  combinatorial formula via series-parallel networks; includes an
  **equivariant** version, settles the Elias–Proudfoot–Wakefield
  top-coefficient conjecture for braid matroids.
- **Gao–Li–Xie–Yang–Zhang (2307.10539, "Induced log-concavity of
  equivariant matroid invariants", 2023):** introduces a strengthened
  notion ("induced log-concavity": `[KL_{k+1}]^2` minus an *induction*
  of `[KL_k] ⊗ [KL_{k+2}]` is effective). Proves induced log-concavity
  of equivariant KL and inverse-KL polynomials for **uniform (S_n
  action) and q-niform (GL_n(F_q) action)** matroids. The argument
  reduces to **Schur positivity** of explicit symmetric functions.
- **Gao–Li–Xie (arXiv:2510.11322, 2025):** equivariant inverse KL for
  thagomizer matroids K_{1,1,n}; also proves classical log-concavity.
- **Caveat:** all of the above are for KL polynomials (intersection
  cohomology Betti numbers of the matroid Schubert variety), NOT the
  f-vector of the independence complex.

### 1.3 Equivariant log-concavity of *graph matchings* (Li 2202.08828)

Shiyue Li, "Equivariant log-concavity of graph matchings", Algebraic
Combinatorics 2022. The graded permutation rep of Aut(Γ) on
k-matchings of a graph Γ is **strongly equivariantly log-concave**.
Proof: explicit equivariant injection inspired by Krattenthaler's
combinatorial map, reducing to classical hard Lefschetz. **This is
the closest published analog of our target** — it lives on the
*matching matroid* of Γ (a transversal matroid), and `[m_k]` is the
permutation rep on k-matchings. The technique (combinatorial
injection + Lefschetz) is exactly the flavor we'd hope to find.

### 1.4 Equivariant top-heavy / Dowling–Wilson

- **Braden–Huh–Matherne–Proudfoot–Wang (2010.06088, "Singular Hodge
  theory for combinatorial geometries", Annals 2024):** introduces the
  intersection cohomology module `IH(M)`, proves Poincaré duality,
  hard Lefschetz, Hodge–Riemann for *all* matroids. Applications:
  Dowling–Wilson top-heavy and KL non-negativity.
- The construction is **manifestly Aut(M)-equivariant** (the IH module
  is a graded `Sym^* L`-module with Aut(M) action); HL is proved by
  semismall decomposition that respects the action. As a corollary
  the *equivariant* top-heavy injection and *equivariant unimodality*
  of equivariant KL coefficients hold (they are virtual reps with
  effective HL-step difference). Stated in the introduction and in
  the survey "What is the Dowling–Wilson conjecture?" (AMS Notices,
  Sep 2024). **This is an equivariant hard-Lefschetz result on a
  different module from ours.**

### 1.5 Equivariant Tutte / characteristic polynomial

- **Bauer–Doležálek–Mišinová–Słobodianiuk–Weigert (arXiv:2312.00913,
  DCG 2025), "Equivariant Tutte polynomial":** equivariant
  generalization of Tutte via equivariant cohomology of the
  permutohedral variety; defines an equivariant reduced
  characteristic polynomial. Provides the *framework* but does not
  appear to prove a new equivariant log-concavity statement for
  characteristic-polynomial coefficients.
- **Maglione–Voll** (Israel J. Math. 2024) and the motivic-zeta line:
  flag Hilbert–Poincaré series of arrangements; combinatorial
  identities but not a direct ELC result for our f-vector.

### 1.6 Summary of the gap

To my knowledge there is **no published ELC theorem for the f-vector
of independent sets of any infinite family of matroids beyond the
trivial cases** (boolean / direct sums of loops/coloops). Li's graph-
matching result is the only ELC theorem about a "size-k independent
set" type sequence with full automorphism action. The MMPR conjecture
covers OS / OT / Cordovil, not f-vectors. So our conjecture is
genuinely open and untested in the literature in our exact form.

---

## Section 2 — Matroid families with large symmetry, suitable for testing

For each: (a) group, (b) ELC status for f-vector, (c) decomposability.

### 2.1 Uniform U_{r,n}
- (a) Aut = S_n, order n!.
- (b) **ELC unknown** for f-vector. Note `f_k = C(n,k)` for k ≤ r and
  `[f_k]` is the permutation rep on k-subsets = `Ind^{S_n}_{S_k x
  S_{n-k}} 1`. By Pieri / Young this decomposes as
  `⊕_{j≤k} S^{(n-j, j)}` (k ≤ n/2). Decomposition is completely
  explicit; multiplicities are 0/1.
- (c) Maximally tractable. ELC for the f-vector reduces to a
  symmetric-function Schur positivity question completely analogous
  to Gao et al. 2307.10539, but for `e_k(1,...,1)` / `h_k(...)`. This
  is the obvious first test case.

### 2.2 Projective and affine geometries PG(n,q), AG(n,q)
- (a) PG(n,q): Aut = PΓL_{n+1}(q) ⊇ PGL_{n+1}(q), order ~q^{n(n+1)/2}
  · |GL|/|center|. AG(n,q): Aut = AΓL_n(q) = (F_q^n ⋊ ΓL_n(q)).
- (b) **ELC unknown.** Bases / independent sets are linearly
  independent k-tuples; permutation reps appear in Steinberg / Harish-
  Chandra decomposition (RSK / Hecke-algebra modules over GL_{n+1}(q)).
- (c) For q=2, F_2-realizable. Permutation rep `[f_k]` =
  `Ind^{GL_{n+1}(2)}_{P} 1` where P is the stabilizer of a k-flag;
  this is a sum of unipotent characters indexed by partitions of k.
  Decomposition known via Hecke algebra of type A_n. **Computable but
  not as clean as uniform.** Proudfoot's 1808.07855 already handled the
  q-niform analog for KL polynomials, so the apparatus exists.

### 2.3 Dowling geometries Q_n(G)
- (a) Aut contains G ≀ S_n = G^n ⋊ S_n (order |G|^n · n!), with extra
  field automorphisms if G is the multiplicative group of a field.
  For rank ≥ 3 the geometry determines G (Dowling).
- (b) **ELC unknown.** For G = {1}, Q_n is the braid matroid M(K_n).
- (c) Decomposition is wreath-product representation theory
  (Clifford theory): irreps of G ≀ S_n are indexed by `Irr(G)`-tuples
  of partitions of total size n. Permutation rep on independent sets
  is computable but combinatorially heavy.

### 2.4 Fano matroid F_7 = PG(2,2)
- (a) Aut = PGL_3(F_2) = GL_3(F_2) = PSL_2(F_7), simple, order 168.
- (b) **ELC unknown but completely computable by hand / GAP.** It's a
  single matroid; rank 3 on 7 elements. f_0=1, f_1=7, f_2=21, f_3=28.
  The Steinberg-style decomposition into the 1, 3, 3̄, 6, 7, 8
  irreps of order-168 is finite. **Excellent sanity check.**
- (c) Trivial — finite computation.

### 2.5 Cycle matroids of vertex-transitive graphs
- **M(K_n):** Aut = S_n (graphic = braid). f_k = #{spanning forests
  with n−k edges}, k ≤ n−1. Permutation rep on independent edge sets
  is a sum of Specht modules; FI-module setup of MMPR applies. Note
  Li's matching paper already gives sELC for *matchings* of any graph,
  including K_n, but matchings ≠ forests.
- **M(K_{n,m}):** Aut ⊇ S_n × S_m (× Z/2 if n=m).
- **M(Petersen):** Aut = S_5 (order 120), a single rank-5 matroid on
  15 edges; finite computation.
- **Cayley graphs Γ(G,S):** Aut ⊇ G (left regular). If S is a union
  of conjugacy classes, also a normalizer acts. Generally clean
  decomposition via Fourier / character theory of G.
- (b)/(c): all unknown ELC; decomposition is Specht-module theory for
  K_n / K_{n,m}, finite GAP-computable for Petersen and small Cayley.

### 2.6 Sparse paving matroids of high symmetry
- (a) Most sparse paving matroids have trivial Aut (Pendavingh–van der
  Pol), but the **exceptional ones** carry Mathieu groups: the matroid
  of the Steiner system S(5,8,24) carries M_24 (order 244,823,040);
  S(5,6,12) carries M_12; S(4,5,11) carries M_11; S(3,6,22) lifts to
  M_22.aut. The Vámos matroid has Aut = D_4 × D_4 (order 64).
- (b) **ELC unknown.**
- (c) For the Mathieu cases, the symmetric-group / Mathieu character
  tables are well-tabulated (in GAP). The relevant permutation reps
  decompose via the character of the natural action on k-subsets
  restricted to M_24 etc. Karn–Wakefield's relaxation machinery may
  give a structural attack.

### 2.7 Direct sums
- Aut(M_1 ⊕ M_2) ⊇ Aut(M_1) × Aut(M_2), with a Z/2 swap if
  M_1 ≅ M_2. f-vector is the convolution; permutation reps tensor.
  **ELC is NOT obviously preserved under direct sums** (this is
  exactly the subtle multiplicative-vs-additive question that
  Lorentzian polynomial theory handles non-equivariantly). For
  identical pieces, one gets an `S_k`-wreath symmetry — worth
  exploring as a "free" symmetry-rich family.

---

## Ranked test cases (most tractable first)
1. **U_{r,n}** — Schur positivity question, the obvious first proof.
2. **Fano F_7** — single 168-order check, must work.
3. **M(K_n)** — braid, FI-module setup available.
4. **PG(2,q), PG(3,2)** — Hecke-algebra decomposition.
5. **Petersen, small Cayley graphs** — small finite checks.
6. **Q_n(G) Dowling** — wreath product structure.
7. **Mathieu sporadic / Steiner-system paving** — finite, beautiful,
   character-table-driven.
