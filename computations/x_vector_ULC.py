"""Test: does the X-vector |X_d(N)| satisfy Ultra Log-Concavity (ULC)?

If yes, combined with palindromicity |X_d| = |X_{n'-d}| (from complementation),
the X-vector is unimodal with peak at n'/2, giving |X_k| <= |X_{k+1}| for k < n'/2.

ULC: |X_d|^2 / C(n', d)^2 >= |X_{d-1}|/C(n', d-1) * |X_{d+1}|/C(n', d+1).

Equivalently, with a_d = |X_d|/C(n', d):  a_d^2 >= a_{d-1} a_{d+1}.

We test across many matroids, including: uniforms, M(K_n), Fano, Vamos, etc.,
AND each N(C, U) sub-matroid harvested from M(K_n).
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from math import comb
from collections import defaultdict
from sparse_rank import M_Kn
from gpu_rank import Matroid, Vamos, AG_n_2


def Fano():
    lines = [frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
    bases = [b for b in combinations(range(7), 3) if frozenset(b) not in lines]
    return Matroid.from_bases(7, bases)


def Pappus():
    lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,7),(1,4,8),(2,5,6),(0,4,6),(1,5,7),(2,3,8)]
    lines = [frozenset(l) for l in lines]
    bases = [b for b in combinations(range(9),3) if frozenset(b) not in lines]
    return Matroid.from_bases(9, bases)


def x_vector(N):
    """Compute |X_d| for d = 0, 1, ..., n'. X_d = {A : |A|=d, A indep, E\\A indep}."""
    E = frozenset(range(N.n))
    out = [0] * (N.n + 1)
    for d in range(N.n + 1):
        if d > N.rank: break
        if N.n - d > N.rank: continue
        cnt = 0
        for A in combinations(range(N.n), d):
            A = frozenset(A)
            if A not in N.indep: continue
            if (E - A) not in N.indep: continue
            cnt += 1
        out[d] = cnt
    return out


def check_ULC(xs, n, label):
    """Check |X_d|^2 / C(n,d)^2 >= |X_{d-1}|/C(n,d-1) * |X_{d+1}|/C(n,d+1) for d
    in the support of |X|.  Equivalently, (xs[d])^2 * C(n,d-1) C(n,d+1) >= C(n,d)^2 xs[d-1] xs[d+1]."""
    bad = []
    for d in range(1, len(xs) - 1):
        if xs[d] == 0 and (xs[d-1] != 0 or xs[d+1] != 0):
            # zero in middle of support — violates M-convexity
            if xs[d-1] != 0 and xs[d+1] != 0:
                bad.append((d, xs[d-1], xs[d], xs[d+1], "M-CONVEX FAIL"))
            continue
        if xs[d] == 0: continue
        # ULC inequality
        lhs = xs[d]**2 * comb(n, d-1) * comb(n, d+1)
        rhs = comb(n, d)**2 * xs[d-1] * xs[d+1]
        if lhs < rhs:
            bad.append((d, xs[d-1], xs[d], xs[d+1], f"ULC FAIL: lhs={lhs} < rhs={rhs}"))
    return bad


def make_NC_U(M, C, U):
    UC = U - C
    UC_list = sorted(UC)
    idx = {e: i for i, e in enumerate(UC_list)}
    n_new = len(UC_list)
    indep = []
    for k_ in range(n_new + 1):
        for A in combinations(UC_list, k_):
            if (frozenset(A) | C) in M.indep:
                indep.append(frozenset(idx[e] for e in A))
    return Matroid(n_new, indep)


def harvest_NCU(M, label, sample=1000):
    """Harvest distinct N(C, U) from orbits of M, returning a list of (N, label)."""
    seen = set()
    out = []
    for m_ in range(M.rank):
        for d_ in range(2, M.rank - m_ + 1):
            pairs = 0
            for S in M.by_size.get(m_, []):
                for T in M.by_size.get(m_+d_, []):
                    pairs += 1
                    if pairs > sample: break
                    C, U = S & T, S | T
                    fp_key = (frozenset(C), frozenset(U))
                    if fp_key in seen: continue
                    seen.add(fp_key)
                    N = make_NC_U(M, C, U)
                    out.append((N, f"{label} (m={m_}, d={d_}, |C|={len(C)})"))
                if pairs > sample: break
    return out


def main():
    direct_matroids = [
        ("U_{4,6}", Matroid.uniform(4, 6)),
        ("U_{5,8}", Matroid.uniform(5, 8)),
        ("U_{6,10}", Matroid.uniform(6, 10)),
        ("M(K_4)", M_Kn(4)),
        ("M(K_5)", M_Kn(5)),
        ("M(K_6)", M_Kn(6)),
        ("Fano", Fano()),
        ("AG(3,2)", AG_n_2(3)),
        ("Vamos", Vamos()),
        ("Pappus", Pappus()),
    ]
    total_tests = 0
    total_ULC_fails = 0

    print("=" * 70)
    print("Part A: X-ULC on the full matroids")
    print("=" * 70)
    for label, N in direct_matroids:
        xs = x_vector(N)
        print(f"  {label}  n={N.n}, rank={N.rank}  X-vector: {xs}")
        bad = check_ULC(xs, N.n, label)
        total_tests += 1
        if bad:
            total_ULC_fails += 1
            for d, prev, curr, nxt, msg in bad:
                print(f"    *** X-ULC FAIL at d={d}  X_{{d-1}}={prev}, X_d={curr}, X_{{d+1}}={nxt}: {msg}")

    print("\n" + "=" * 70)
    print("Part B: X-ULC on harvested N(C, U) sub-matroids")
    print("=" * 70)

    for label, M in direct_matroids:
        ncu_list = harvest_NCU(M, label, sample=300)
        # Sample up to 50 of them
        for N, sublabel in ncu_list[:50]:
            xs = x_vector(N)
            bad = check_ULC(xs, N.n, sublabel)
            total_tests += 1
            if bad:
                total_ULC_fails += 1
                print(f"  *** X-ULC FAIL in {sublabel}: n={N.n}, rank={N.rank}, X={xs}")
                for d, prev, curr, nxt, msg in bad:
                    print(f"      d={d}: {msg}")
        print(f"  {label}: tested {min(50, len(ncu_list))} sub-matroids")

    print("\n" + "=" * 70)
    print(f"TOTAL: {total_tests} matroids tested, {total_ULC_fails} X-ULC violations")
    if total_ULC_fails == 0:
        print("  X-vector ULC holds on all tested cases. Strategy III is viable.")


if __name__ == "__main__":
    main()
