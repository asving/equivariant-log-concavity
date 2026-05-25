# Testing if the Aut-orbit Hall reformulation is genuine progress

**Date: 2026-05-22 (final session of the day).**

The methodological test: take a concrete matroid where step 5 (Aut-orbit Hall) is provable, and see if it's actually easier to prove than step 2 (Theorem 1 directly).

## Test case: M(K_{2,3})

The complete bipartite graph `K_{2,3}` has parts `{a, b}` and `{c, d, e}`, so 6 edges total. Rank of `M(K_{2,3})` = 4 (5 vertices, connected). Satisfies our hypothesis at `(k, d) = (2, 2)`: `n = 6 = 2k+d`, `r = 4 = k+d`, `d = 2 ≥ 2`. So the orbit decomposition picks up a non-trivial `X_2 → X_3` bipartite incidence.

## Direct computation of X_2 and X_3

**Cycles in `K_{2,3}`:** all of length 4, of the form `{(a,x), (a,y), (b,x), (b,y)}` for `x ≠ y ∈ {c, d, e}`. Three 4-cycles: indexed by pairs `(x, y) ∈ {cd, ce, de}`.

**`X_2(K_{2,3})`:** 2-edge subsets `A` with `A` independent (forest, automatic — no parallel edges) and `E \ A` independent (= 4-edge forest, i.e., no 4-cycle ⊂ `E \ A`). So `X_2` is 2-edge subsets that "break" every 4-cycle.

The bad 2-edge subsets (= those whose 4-edge complement still contains a cycle): the 3 "co-cycles" `{(a, e), (b, e)}`, `{(a, d), (b, d)}`, `{(a, c), (b, c)}` (each consisting of the two edges incident to a single "outer" vertex).

So `|X_2| = C(6, 2) - 3 = 12`.

**`X_3(K_{2,3})`:** All 3-edge subsets are forests (no 3-cycle in bipartite graph). Same for complements (also 3-edge). So `|X_3| = C(6, 3) = 20`.

By Ardila et al. Corollary 1.7: ratio ≥ `(n-k)/(k+1) = 4/3`. Indeed `20/12 = 5/3 ≥ 4/3` ✓.

## Aut(M(K_{2,3}))

`Aut(K_{2,3}) = S_2 × S_3` (swap parts {a, b}, permute outer {c, d, e}), so the graph automorphism group has order 12. However, **Whitney's matroid automorphism theorem** says that for graphs with 2-vertex separators (= not 3-connected), the matroid automorphism group can be strictly larger than the graph automorphism group, due to *Whitney twists* — independently flipping each "outer subgraph" at the separator.

For `K_{2,3}`: the separator `{a, b}` splits each outer vertex `c, d, e` into its own "subgraph" of two edges. Each such subgraph can be independently "twisted" (= swap `(a, x) ↔ (b, x)`). This gives `2^3 = 8` Whitney twists, combined with the 12-element graph automorphism group, yielding **|Aut(M(K_{2,3}))| = 48** (modulo the overlap, which a direct computation confirms).

## Aut-orbits in X_2(K_{2,3})

By computer verification (see `computations/verify_k23.py`):

> **`Aut(M(K_{2,3}))` acts transitively on `X_2(K_{2,3})`** — i.e., there is exactly ONE orbit of size 12.

This is the *entire* `X_2`. So Aut-orbit Hall reduces to a single inequality to verify.

The 12 elements of `X_2` are listed as:
```
{(a,c), (a,d)},  {(a,c), (a,e)},  {(a,c), (b,d)},  {(a,c), (b,e)},
{(a,d), (a,e)},  {(a,d), (b,c)},  {(a,d), (b,e)},  {(a,e), (b,c)},
{(a,e), (b,d)},  {(b,c), (b,d)},  {(b,c), (b,e)},  {(b,d), (b,e)}
```

(Notice: the missing 3 from `C(6,2) = 15` are exactly `{(a,x), (b,x)}` for `x ∈ {c, d, e}` — the three "co-cycles" that fail to break all 4-cycles, as predicted.)

## Aut-orbit Hall: one-line proof

The single Aut-orbit `O = X_2(K_{2,3})` has neighborhood `N(O) ⊆ X_3(K_{2,3}) = (all 3-edge subsets)`. We need `|N(O)| ≥ |O| = 12`.

For any `A' ∈ X_3` (a 3-edge subset), pick any `j ∈ A'`. Then `A' \ {j}` is a 2-edge subset. There are 3 candidate `A' \ {j}`'s as `j` ranges over `A'`. At least one of these 3 candidate 2-edge subsets is in `X_2` (= breaks all 4-cycles); equivalently, at least one of `A' \ {j}` is *not* one of the 3 bad "co-cycle" pairs.

(Why? Each bad pair `{(a,x), (b,x)}` is determined by its outer vertex `x ∈ {c, d, e}`. The 3 candidate `A' \ {j}`'s can contain at most one bad pair (else `A'` would have 4 elements). Two of the three candidates are always good — i.e., in `X_2`.)

So every `A' ∈ X_3` has a predecessor in `O`, i.e., `N(O) = X_3`, of size `20 ≥ 12`. ✓ ∎

## Conclusion: Aut-orbit Hall proved for `M(K_{2,3})`

The proof is *complete*, *elementary*, and *literally one paragraph*. No deep matroid theory, no Lorentzian polynomials, no Cohen-Macaulayness invoked. ∎

This gives a direct proof of Theorem 4'-II (and hence the user's INJ, and hence ELC for the f-vector of `K_{2,3}`).

## Is this "easier" than direct approaches?

### Direct approach to Theorem 4'-II on `M(K_{2,3})`

Build the `20 × 12` bipartite incidence matrix and check rank = 12. Doable computationally; not particularly illuminating combinatorially.

### Direct approach to the user's INJ (Theorem 1)

Build `L` as a matrix on `S(M(K_{2,3}))` and check `L: S_{-d} → S_{-d+2}` is injective for each `d ≥ 2`. This is what our verification scripts do.

### Aut-orbit Hall

Identify Aut-orbits, compute `|N(O)|` for each, check `≥ |O|`. **For `K_{2,3}` this collapsed to ONE LINE per orbit.**

For matroids with rich symmetry (e.g., `K_{2, n}`, `K_{m, n}`, uniforms, projective spaces, Steiner systems, etc.), this approach reduces an `O(2^{|X_k|})` brute force to an `O(# orbits)` per-orbit check.

### Verdict

**Yes, the Aut-orbit Hall reformulation is genuine progress** — for matroids with non-trivial automorphism groups, it gives a per-orbit check that's combinatorially clean.

**No, it doesn't immediately give a proof for ALL matroids** — matroids with trivial `Aut` have orbits all of size 1, and Aut-orbit Hall reduces to "every singleton has degree ≥ 1", which is trivial. The interesting content is in non-singleton orbits, and there the orbits' sizes depend on the matroid.

For our project's *original* goal (Aut(M)-equivariant log-concavity), this reformulation is structurally on-target: we've reduced the proof to an equivariant statement, which is what ELC fundamentally is.

## Next concrete generalizations to try

1. **`M(K_{m, n})`** for various m, n. The symmetry group is `S_m × S_n × S_2`, very rich. Likely follows the same pattern as `K_{2, 3}`.
2. **Uniform `U_{r, n}`** with our hypothesis. Aut = `S_n`, very rich. Likely 1 orbit, trivially Hall.
3. **Paving matroids** (where the failing Lemma 5 originally lived). Aut group can be smaller; more orbits.
4. **General graphic matroid `M(G)`**: the proof for `K_{2,3}` should generalize to bipartite graphs, then to all graphs via some recursive structure.

A reasonable next research step is to prove **Aut-orbit Hall for all simple matroids of rank `≤ r`** for small `r` (say `r ≤ 5`), establishing the conjecture for an infinite family. The pattern from `K_{2,3}` suggests:

- Each Aut-orbit corresponds to a structural "type" of size-`k` indep set.
- Extensions of an Aut-orbit fan out into multiple structural types of size-`k+1` indep sets.
- The fan-out is "wide" enough to satisfy `|N(O)| ≥ |O|`.

The general proof of Aut-orbit Hall remains open for matroids without large `Aut` (e.g., generic random matroids, matroids representing generic point configurations). For these, all `Aut`-orbits are singletons, and the original Hall condition is recovered — back to square one. So the Aut-orbit reduction is only a substantive simplification for matroids with non-trivial symmetry.
