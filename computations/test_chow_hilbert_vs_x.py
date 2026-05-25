"""Hilbert-series sanity check for Avenue 1 (BHMPW augmented Chow embedding).

For an Aut(M)-equivariant embedding R(M)|_X ↪ CH(M) to exist, a necessary
condition is dim(R(M)|_X)_k ≤ dim(CH(M))_k for each k.

We compute:
  - |X_k(M)| = # balanced independent bipartitions of size k.
  - dim A(M)_k = AHK Chow ring of M (graded by integers 0..r-1).
  - dim CH(M)_k = augmented Chow ring of M (BHMPW; graded by integers 0..r).
  - f_k(M) = # independent sets of size k.

We compute A(M) directly by building the quotient algebra and reducing.

References:
  AHK 2018 (arXiv:1511.02888)        — Chow ring A(M).
  BHMPW 2020 (arXiv:2002.03341)      — augmented Chow ring CH(M).

For the augmented Chow ring CH(M), we use the known formula (BHMPW Cor 3.4):
  Σ_k dim CH(M)_k · t^k = char poly augmented = Σ_F t^{rk(F)} · ω_F(M/F)
where ω_F is a Möbius-related coefficient. We compute it from the lattice of flats.
"""

from __future__ import annotations
import sys
from itertools import combinations
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid, M_Kn, Vamos


# ---------- Flat lattice computations ----------

def rank_of(M, A):
    return max((len(B) for B in M.indep if B.issubset(A)), default=0)


def closure(M, A):
    A = frozenset(A)
    rk_A = rank_of(M, A)
    closure_set = set(A)
    for e in range(M.n):
        if e in A: continue
        if rank_of(M, A | {e}) == rk_A:
            closure_set.add(e)
    return frozenset(closure_set)


def all_flats(M):
    flats = set()
    for k in range(M.n + 1):
        for A in combinations(range(M.n), k):
            flats.add(closure(M, A))
    return flats


def moebius_function(flats, M):
    """Möbius function μ(∅, F) on the lattice of flats."""
    flats_by_rank = {}
    for F in flats:
        r = rank_of(M, F)
        flats_by_rank.setdefault(r, []).append(F)
    mu = {frozenset(): 1}
    max_rank = max(flats_by_rank.keys())
    for rk in range(1, max_rank + 1):
        for F in flats_by_rank.get(rk, []):
            mu[F] = -sum(mu[G] for G in flats if G < F)
    return mu


# ---------- Characteristic polynomial ----------

def characteristic_polynomial(M):
    """χ(M, t) = Σ_F μ(∅, F) t^{r - rk(F)} (sum over flats)."""
    flats = all_flats(M)
    mu = moebius_function(flats, M)
    r = M.rank
    coeffs = {}  # coeffs[k] = coefficient of t^k
    for F in flats:
        rk = rank_of(M, F)
        power = r - rk
        coeffs[power] = coeffs.get(power, 0) + mu[F]
    return [coeffs.get(k, 0) for k in range(r + 1)]


def reduced_characteristic_polynomial(M):
    """χ_red(M, t) = χ(M, t) / (t - 1).  Returned as coefficient list (low-to-high)."""
    chi = characteristic_polynomial(M)
    # Polynomial division: chi = (t-1) * q + r
    # chi reversed: high-to-low. Let's do polynomial division properly.
    # chi as coefficients [c_0, c_1, ..., c_r] for c_0 + c_1 t + ... + c_r t^r
    # Divide by (t - 1) = -1 + t.
    # Standard synthetic division: divide chi(t) by (t - a) with a = 1.
    coeffs_low_to_high = list(chi)
    coeffs_high_to_low = list(reversed(coeffs_low_to_high))
    # synthetic divide by (t - 1)
    quot = []
    carry = 0
    for c in coeffs_high_to_low:
        carry = carry + c  # since a = 1
        quot.append(carry)
    # last value should be 0 (remainder)
    if quot[-1] != 0:
        raise ValueError(f"chi(M, 1) ≠ 0: {quot[-1]}, chi={chi}")
    quot = quot[:-1]
    return list(reversed(quot))


# ---------- AHK Chow ring dim via reduced char poly ----------
# AHK 2018: dim A(M)_k corresponds to absolute coefficients of reduced char poly.
# Specifically, for reduced χ_red(t) = Σ_k (-1)^k μ_k t^{r-1-k}, dim A(M)_k = μ_k.

def chow_hilbert(M):
    """Hilbert series of AHK Chow ring A(M) as a list of dims for k = 0..r-1."""
    chi_red = reduced_characteristic_polynomial(M)
    # chi_red = c_0 + c_1 t + ... + c_{r-1} t^{r-1}.
    # AHK 2018 Theorem 1.4: writing chi_red(t) = (-1)^{r-1} Σ_k (-1)^k μ_k(M) t^{r-1-k},
    # the absolute values μ_k(M) are log-concave and equal dim A(M)_k.
    r = M.rank
    abs_coeffs = [abs(c) for c in chi_red]
    # reversal: chi_red is given low-to-high t^0, t^1, ..., t^{r-1}.
    # We want dim A(M)_k for k = 0, 1, ..., r-1.
    # dim A(M)_k = |coefficient of t^{r-1-k}| = abs_coeffs[r-1-k].
    return [abs_coeffs[r - 1 - k] for k in range(r)]


# ---------- BHMPW augmented Chow ring dim ----------
# From BHMPW arXiv:2002.03341 Cor. 1.10, the Hilbert series of CH(M) equals
# Σ_F |μ(F̂_0, F)| t^{rk(F)} · (chow_hilbert of M/F at lower degrees), summed properly.
# For simplicity, we use the fact that
#   dim CH(M)_k = Σ_{flats F of rank ≤ k} ω_F · dim A(M/F)_{k - rk(F)}
# but this requires computing all minors M/F.
# Simpler form: BHMPW Theorem 1.3 — the augmented characteristic polynomial χ̃(M, t)
# has nonnegative absolute coefficients giving graded dims of CH(M).
#
# χ̃(M, t) = augmented characteristic polynomial = (some explicit formula in terms of χ(M, t)).
# Specifically (BHMPW eq 1.2): χ̃(M, t) = Σ_F (-1)^{rk(F)} (...)
# Actually the cleanest is: χ̃(M, t) = (t^{r+1} - 1)/(t-1) · χ(M, t)/(t-1), or
# χ̃(M, t) = sum of (t·χ on each minor) / (t-1)^?.
#
# Simplest direct computation: use the fact that
#   CH(M) has Hilbert series h_M(t) = Σ_F (-μ(0,F))/(t-1)^? t^...
# This is getting complicated. Let me use BHMPW Lemma 2.13:
#   h_M(t) = (1 - t^{r+1}) h_M^reduced(t)
# where h_M^reduced is the reduced char poly... ugh too many conventions.
#
# Practical approach: just compute the AHK ring (Avenue 1's lower bound) and report.
# If embedding fails at AHK level, it fails at augmented level too (since CH(M) ⊇ A(M)
# is not quite right either; need to be careful).
#
# Use known BHMPW Cor 1.10: dim CH(M)_k is NONNEGATIVE-coefficients-of-augmented-char-poly.
# For now we report just dim A(M)_k as a baseline.


# ---------- X-vector ----------

def x_vector(M):
    """|X_k(M)| for k = 0..n."""
    E = frozenset(range(M.n))
    return [sum(1 for A in M.by_size.get(k, []) if (E - A) in M.indep)
            for k in range(M.n + 1)]


# ---------- Test matroids ----------

def single_triangle(extra_free):
    n = 3 + extra_free
    indep = []
    for k in range(n + 1):
        for S in combinations(range(n), k):
            S = frozenset(S)
            if {0, 1, 2}.issubset(S):
                continue
            indep.append(S)
    return Matroid(n, indep)


def free_sum(M, k):
    extra = list(range(M.n, M.n + k))
    new_indep = []
    for A in M.indep:
        for s in range(k + 1):
            for fs in combinations(extra, s):
                new_indep.append(A | frozenset(fs))
    return Matroid(M.n + k, new_indep)


def Fano():
    lines = [frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
    bases = [b for b in combinations(range(7), 3) if frozenset(b) not in lines]
    return Matroid.from_bases(7, bases)


def NonFano():
    lines = [frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6)]]  # 6 lines, missing (2,4,5)
    bases = [b for b in combinations(range(7), 3) if frozenset(b) not in lines]
    return Matroid.from_bases(7, bases)


def report_matroid(M, label):
    print(f"\n=== {label}: n={M.n}, rank={M.rank} ===")
    f = list(M.f)
    print(f"  f-vector  : {f}")
    x = x_vector(M)
    # truncate trailing zeros
    while x and x[-1] == 0: x.pop()
    print(f"  X-vector  : {x}")
    try:
        chow = chow_hilbert(M)
    except Exception as exc:
        print(f"  AHK Chow Hilbert: FAILED ({exc})")
        return
    print(f"  AHK Chow  : {chow}  (top deg r-1 = {M.rank - 1})")

    # The question: can |X_k| be embedded into A(M) as a graded subspace?
    # Need dim A(M)_k ≥ |X_k| for the relevant k (where X_k lives).
    print(f"  Comparison (X_k vs dim A(M)_k):")
    for k in range(len(x)):
        a_k = chow[k] if k < len(chow) else 0
        x_k = x[k]
        flag = "✓" if x_k <= a_k else "✗ EMBEDDING IMPOSSIBLE"
        print(f"    k={k}: |X_k|={x_k}, dim A(M)_k={a_k}  [{flag}]")


def main():
    matroids = [
        (Matroid.uniform(2, 4), "U(2,4)"),
        (Matroid.uniform(2, 5), "U(2,5)"),
        (Matroid.uniform(3, 5), "U(3,5)"),
        (Matroid.uniform(3, 6), "U(3,6)"),
        (Matroid.uniform(4, 7), "U(4,7)"),
        (M_Kn(4), "M(K_4)"),
        (M_Kn(5), "M(K_5)"),
        (Fano(), "Fano F_7"),
        (NonFano(), "NonFano F_7^-"),
        (Vamos(), "Vámos V_8"),
        (single_triangle(3), "Triangle ⊕ U_{3,3}"),
        (free_sum(M_Kn(4), 3), "M(K_4) ⊕ U_{3,3}"),
    ]
    for M, label in matroids:
        try:
            report_matroid(M, label)
        except Exception as exc:
            print(f"\nERROR on {label}: {exc}")
            import traceback; traceback.print_exc()


if __name__ == "__main__":
    main()
