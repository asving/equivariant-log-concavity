"""Hunt for small representable matroids whose R(M)|_X structure matches
the cohomology of some hyperkähler-related space.

Quantities computed per matroid M (loopless, rank r, n elements):
  - f-vector  (= dim R(M))
  - h-vector  (Hilbert function of k[IN(M)]/Θ generic = H*(X^HK_M) by Hausel-Sturmfels)
  - X-vector  (= dim R(M)|_X)
  - Total dims and ratios.

Candidate identifications:
  (a) R(M)|_X = H*(X^HK_M)            — single hyperkähler.
  (b) R(M)|_X = H*(Z(X^HK_M))         — twistor space (= S²-fibration over X^HK).
      By Leray: H*(Z) ≅ H*(S²) ⊗ H*(X^HK)  (when fibration is cohomologically trivial,
      which holds for toric hyperkähler). Total dim = 2 × |h-vector|.
  (c) R(M)|_X = H*(X^HK_M × X^HK_M)   — square of single. Total dim = |h|².

For each matroid, we check which (if any) total dim matches |X-vector|.
We also check whether the GRADED structure of (b) (= H*(Z) ≅ (1+t²) · h-poly)
matches the X-polynomial of M (after some shift / rescaling).

Hauseel-Sturmfels (arXiv:math/0203096): for representable M of rank r on n elements,
the toric hyperkähler X^HK_M has complex dim 2r, real dim 4r, and
H*(X^HK_M; Q) ≅ Q[IN(M)]/Θ as graded rings, where Θ is a generic lsop.
The graded Hilbert function = h-vector of IN(M).
"""

from __future__ import annotations
import sys
from itertools import combinations
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid, M_Kn, Vamos
from test_hard_lefschetz_x import x_sets, free_sum, single_triangle


def h_vector(M):
    """h-vector of IN(M).

    Matroid convention: M.f[i] = # indep sets of size i, so M.f[0] = 1 (empty).
    Simplicial convention: f_{i-1}(IN(M)) = # faces of dim i-1 = # indep sets of size i = M.f[i].
    So f_{j-1}(IN) = M.f[j] for j = 0, 1, ..., rank.

    h_k = Σ_{j=0..k} (-1)^{k-j} C(d-j, k-j) f_{j-1}(IN) = Σ_j (-1)^{k-j} C(d-j, k-j) M.f[j].
    """
    d = M.rank
    f = list(M.f)  # f[j] = # indep size j (with f[0] = 1)
    from math import comb
    h = []
    for k in range(d + 1):
        hk = 0
        for j in range(k + 1):
            if j < len(f):
                hk += (-1)**(k - j) * comb(d - j, k - j) * f[j]
        h.append(hk)
    return h


def x_vector(M):
    n = M.n
    return [len(x_sets(M, k)) for k in range(n + 1)]


def poly_product(p, q):
    """Polynomial product."""
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def trim_trailing(p):
    while p and p[-1] == 0:
        p.pop()
    return p


def analyze(M, label):
    print(f"\n{'='*72}")
    print(f"  {label}: n={M.n}, rank={M.rank}")
    print(f"{'='*72}")
    fv = list(M.f)
    hv = h_vector(M)
    xv = x_vector(M)
    while xv and xv[-1] == 0: xv.pop()
    if xv and xv[0] == 0:
        # show as support window
        x_supp_start = next(i for i, v in enumerate(xv) if v > 0)
        x_supp = xv[x_supp_start:]
    else:
        x_supp_start, x_supp = 0, xv
    if not x_supp:
        print("  X-vector empty. Skip.")
        return

    print(f"  f-vector:  {fv}            (total {sum(fv)})")
    print(f"  h-vector:  {hv}            (total {sum(hv)})")
    print(f"  X-support [{x_supp_start},{x_supp_start + len(x_supp) - 1}]: {x_supp}  (total {sum(x_supp)})")

    # Candidate (a): single H*(X^HK)
    print(f"\n  Match candidates:")
    print(f"    (a) R(M)|_X = H*(X^HK_M)?  ", end="")
    if sum(x_supp) == sum(hv):
        print(f"total dim match: {sum(hv)} ✓")
        # also check graded match
        if x_supp == hv:
            print(f"        graded match: {x_supp} = {hv} ✓✓")
    else:
        print(f"total dim {sum(x_supp)} vs h-total {sum(hv)} — no match")

    # Candidate (b): H*(Z(X^HK)) = (1+t²) · h-poly (cohomologically) via Leray
    #   Total dim = 2 · |h-vector|.
    twistor_total = 2 * sum(hv)
    twistor_poly = poly_product(hv, [1, 1])  # convolve with (1, 1) representing (1+t)
    # (We use (1+t) at the polynomial level for matching cohomology grading concision.)
    print(f"    (b) R(M)|_X = H*(twistor Z)? total dim {twistor_total}", end="")
    if sum(x_supp) == twistor_total:
        print(f" matches |X| = {sum(x_supp)} ✓")
        # Check the polynomial match
        if x_supp == twistor_poly:
            print(f"        graded match: {x_supp} = {twistor_poly} ✓✓")
        else:
            # Try shifts
            for shift in range(-3, 4):
                if shift > 0:
                    shifted = [0]*shift + list(twistor_poly)
                else:
                    shifted = twistor_poly[-shift:]
                if shifted == list(xv):
                    print(f"        graded match with shift {shift}: ✓✓")
                    break
            else:
                print(f"        graded structure differs: X = {x_supp} vs twistor = {twistor_poly}")
    else:
        print(f" (= 2·|h| = {twistor_total}) vs |X| = {sum(x_supp)} — no match")

    # Candidate (c): tensor square of X^HK
    sq_total = sum(hv) ** 2
    print(f"    (c) R(M)|_X = H*(X^HK × X^HK)?  total dim {sq_total}", end="")
    if sum(x_supp) == sq_total:
        print(f" matches |X| = {sum(x_supp)} ✓")
    else:
        print(f" — no match")

    # Candidate (d): X-vector matches h-vector convolved with itself? (= H*(X^HK)² as a vector space)
    h_squared_conv = poly_product(hv, hv)
    print(f"    (d) X-poly = h-poly × h-poly? (= Künneth tensor structure)")
    print(f"        h² = {h_squared_conv}  vs  X = {xv if len(xv) <= 10 else xv[:5] + ['...']}")


def main():
    matroids = [
        # Uniform — known representable
        (Matroid.uniform(2, 3), "U(2,3)  Triangle"),
        (Matroid.uniform(3, 4), "U(3,4)"),
        (Matroid.uniform(3, 5), "U(3,5)"),
        (Matroid.uniform(3, 6), "U(3,6)"),
        (Matroid.uniform(4, 5), "U(4,5)"),
        (Matroid.uniform(4, 6), "U(4,6)"),
        (Matroid.uniform(5, 8), "U(5,8)"),
        # Non-uniform graphic — representable
        (M_Kn(4), "M(K_4)"),
        # Direct sums with free elements
        (single_triangle(2), "U(2,3) ⊕ U(2,2)"),
        (single_triangle(3), "U(2,3) ⊕ U(3,3)"),
        (free_sum(M_Kn(4), 3), "M(K_4) ⊕ U(3,3)"),
    ]
    for M, label in matroids:
        try:
            analyze(M, label)
        except Exception as ex:
            print(f"\nERROR on {label}: {ex}")
            import traceback; traceback.print_exc()


if __name__ == "__main__":
    main()
