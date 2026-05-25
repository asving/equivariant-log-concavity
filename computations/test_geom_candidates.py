"""Compare R(M)|_X against multiple candidate geometric Hilbert series.

For each small matroid M, compute:
  - X-vector |X_k(M)|              — R(M)|_X dimensions (target)
  - h-vector h_k(IN(M))             — H*(X^HK_M) by Hausel-Sturmfels
  - OS-vector |w_k(M)|              — H*(hyperplane arrangement complement) = Orlik-Solomon
  - twistor: 2·h-vector total       — H*(twistor space Z = X^HK × S²)
  - Möbius: Whitney 1st kind series — closely related to OS

The Orlik-Solomon algebra of M (when representable) is H* of the COMPLEMENT of
M's hyperplane arrangement in C^{rank}. Dim OS(M)_k = |w_k(M)| where w_k are
absolute values of coefficients of the characteristic polynomial χ(M, t).
This is a SMOOTH OPEN variety; OS(M) is the singular cohomology.

We look for ANY graded match: maybe R(M)|_X has the same Hilbert series as
one of these geometric Hilbert series under a shift, scaling, or graded sub-piece.
"""
from __future__ import annotations
import sys
from itertools import combinations
from math import comb
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid, M_Kn, Vamos
from test_hard_lefschetz_x import x_sets, free_sum, single_triangle
from test_twistor_matching import h_vector


def rank_in_M(M, A):
    return max((len(B) for B in M.indep if B.issubset(A)), default=0)


def closure(M, A):
    A = frozenset(A)
    rk = rank_in_M(M, A)
    out = set(A)
    for e in range(M.n):
        if e in A: continue
        if rank_in_M(M, A | {e}) == rk:
            out.add(e)
    return frozenset(out)


def all_flats(M):
    flats = set()
    for k in range(M.n + 1):
        for A in combinations(range(M.n), k):
            flats.add(closure(M, A))
    return flats


def moebius(M, flats):
    """μ(∅, F) on lattice of flats of M."""
    rk = {F: rank_in_M(M, F) for F in flats}
    by_rk = {}
    for F in flats:
        by_rk.setdefault(rk[F], []).append(F)
    mu = {frozenset(): 1}
    for r in sorted(by_rk):
        if r == 0: continue
        for F in by_rk[r]:
            mu[F] = -sum(mu[G] for G in flats if G < F)
    return mu


def char_polynomial_abs_coeffs(M):
    """Returns (c_0, c_1, ..., c_r) where χ(M, t) = Σ (-1)^k c_k t^{r-k} (alternating signs).
    The absolute values c_k are the Whitney 2nd-kind numbers; |w_k| =c_k = dim OS(M)_k."""
    flats = all_flats(M)
    mu = moebius(M, flats)
    r = M.rank
    coeffs = {}
    for F in flats:
        rkF = rank_in_M(M, F)
        power = r - rkF
        coeffs[power] = coeffs.get(power, 0) + mu[F]
    # χ(M, t) = Σ_k coeffs[k] t^k. For loopless M coeffs alternate sign:
    # coeffs[r-rk(F)] has sign (-1)^{rk(F)}.
    # |w_k| := |coeffs[r-k]| = dim OS(M)_k for k = 0, ..., r.
    abs_w = [abs(coeffs.get(r - k, 0)) for k in range(r + 1)]
    return abs_w


def x_vector(M):
    return [len(x_sets(M, k)) for k in range(M.n + 1)]


def trim(p):
    while p and p[-1] == 0: p.pop()
    return p


def analyze(M, label):
    print(f"\n{'='*72}")
    print(f"  {label}: n={M.n}, rank={M.rank}")
    print(f"{'='*72}")
    n, r = M.n, M.rank
    fv = list(M.f)
    hv = h_vector(M)
    osv = char_polynomial_abs_coeffs(M)
    xv = x_vector(M)
    while xv and xv[-1] == 0: xv.pop()
    # Find X-support
    x_supp_start = next((i for i, v in enumerate(xv) if v > 0), 0)
    x_supp = xv[x_supp_start:] if x_supp_start < len(xv) else []

    print(f"  f-vector :  {fv}                      sum {sum(fv)}")
    print(f"  h-vector :  {hv}                      sum {sum(hv)}    (= H*(X^HK) HS)")
    print(f"  OS-vector:  {osv}                      sum {sum(osv)}    (= H*(arrangement complement))")
    print(f"  X-vector :  {x_supp}  start={x_supp_start}  sum {sum(x_supp)}    (= R(M)|_X)")

    # Check matches
    print(f"\n  Matches against |X|:")
    matches = []
    candidates = [
        ('h-vector', hv),
        ('2·h-vector (twistor)', [2*x for x in hv]),
        ('OS', osv),
        ('OS shifted-up by 1', [0] + osv),
        ('OS without deg 0', osv[1:] if len(osv) > 1 else []),
    ]
    for name, vec in candidates:
        if sum(vec) == sum(x_supp):
            graded_match = (list(vec) == list(x_supp))
            shifted_match = False
            shift_amount = None
            for s in range(-3, 4):
                vec_shifted = [0]*s + list(vec) if s > 0 else (list(vec)[-s:] if s < 0 else list(vec))
                if vec_shifted == list(xv):
                    shifted_match = True
                    shift_amount = s
                    break
            flag = "EXACT ✓✓✓" if graded_match else ("shift " + str(shift_amount) if shifted_match else "total only")
            print(f"    {name:30s}: sum {sum(vec):4d} ✓  ({flag})")
            matches.append((name, vec, graded_match, shifted_match))
        else:
            print(f"    {name:30s}: sum {sum(vec):4d} (vs |X|={sum(x_supp)})")


def main():
    matroids = [
        (Matroid.uniform(2, 3), "U(2,3) Triangle"),
        (Matroid.uniform(3, 4), "U(3,4)"),
        (Matroid.uniform(3, 5), "U(3,5)"),
        (Matroid.uniform(3, 6), "U(3,6)"),
        (Matroid.uniform(4, 5), "U(4,5)"),
        (Matroid.uniform(4, 6), "U(4,6)"),
        (Matroid.uniform(5, 8), "U(5,8)"),
        (M_Kn(4), "M(K_4)"),
        (single_triangle(2), "U(2,3)⊕U(2,2)"),
        (single_triangle(3), "U(2,3)⊕U(3,3)"),
        (free_sum(M_Kn(4), 3), "M(K_4)⊕U(3,3)"),
    ]
    for M, label in matroids:
        try:
            analyze(M, label)
        except Exception as ex:
            print(f"\nERROR on {label}: {ex}")
            import traceback; traceback.print_exc()


if __name__ == "__main__":
    main()
