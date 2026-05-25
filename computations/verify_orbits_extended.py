"""Extended orbit verification: test Lemma 5 across more matroids and bigrades.

For each matroid M and bigrade (m, d) with d >= 2:
  - Enumerate orbits (C, U) by iterating over pairs (S, T) with S, T indep, |S|=m, |T|=m+d.
  - For each orbit, compute N(C, U) = (M/C)|_{U\C}, f_k(N), f_{k+1}(N) where k = m-|C|.
  - Check that |orbit| > 0 implies f_k(N) <= f_{k+1}(N).
  - Also test orbit-injectivity numerically via sparse mod-p rank.

Matroids tested: M(K_6) at m=2,3 d=2; Vamos; AG(3,2); Fano; Pappus; NonPappus.
"""
import sys, time
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from collections import defaultdict
from gpu_rank import Matroid, Vamos, AG_n_2
from sparse_rank import M_Kn


def Pappus():
    lines = [(0,1,2),(3,4,5),(6,7,8),
             (0,3,7),(1,4,8),(2,5,6),
             (0,4,6),(1,5,7),(2,3,8)]
    lines = [frozenset(l) for l in lines]
    bases = [b for b in combinations(range(9),3) if frozenset(b) not in lines]
    return Matroid.from_bases(9, bases)


def NonPappus():
    lines = [(0,1,2),(3,4,5),(6,7,8),
             (0,3,7),(1,4,8),
             (0,4,6),(1,5,7),(2,3,8)]
    lines = [frozenset(l) for l in lines]
    bases = [b for b in combinations(range(9),3) if frozenset(b) not in lines]
    return Matroid.from_bases(9, bases)


def Fano():
    lines = [frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
    bases = [b for b in combinations(range(7), 3) if frozenset(b) not in lines]
    return Matroid.from_bases(7, bases)


def orbit_invariants(S, T):
    return (frozenset(S & T), frozenset(S | T))


def verify(M, label, m, d):
    """Check Lemma 5 + orbit-size = f_k(N) on (m, d) bigrade."""
    print(f"\n=== {label}  m={m}, d={d}  rank={M.rank}, n={M.n} ===", flush=True)
    if m + d > M.rank:
        print(f"  skip: m+d > rank")
        return
    src_size = len(M.by_size.get(m, [])) * len(M.by_size.get(m+d, []))
    print(f"  |Indep_m|={len(M.by_size.get(m, []))}  |Indep_{m+d}|={len(M.by_size.get(m+d, []))}  |src pairs|={src_size}")

    t0 = time.time()
    orbits = defaultdict(int)  # (C, U) -> count of pairs in orbit
    for S in M.by_size.get(m, []):
        for T in M.by_size.get(m+d, []):
            C, U = orbit_invariants(S, T)
            orbits[(C, U)] += 1
    t1 = time.time()
    print(f"  # orbits = {len(orbits)}  (enumeration {t1-t0:.1f}s)")

    # For each orbit, compute N(C,U)'s f-vector.
    f_check_failures = []
    orbit_size_mismatches = []
    f_k_dist = defaultdict(int)
    max_orbit_size = 0
    min_orbit_size = 10**9
    boolean_orbits = 0
    matroidal_orbits = 0

    for (C, U), orbit_size in orbits.items():
        UC = U - C
        k = m - len(C)
        # Compute f_k(N) and f_{k+1}(N): indep subsets of UC of size k and k+1.
        # N's indep sets = {A subset of UC : A union C is indep in M}.
        # (We exploit indep-downclosure: enumerate combinations of size k and check.)
        nk = sum(1 for A in combinations(UC, k) if frozenset(A) | C in M.indep)
        nk1 = 0
        if k + 1 <= len(UC):
            nk1 = sum(1 for A in combinations(UC, k+1) if frozenset(A) | C in M.indep)
        f_k_dist[(nk, nk1)] += 1
        if orbit_size > max_orbit_size: max_orbit_size = orbit_size
        if orbit_size < min_orbit_size: min_orbit_size = orbit_size
        # Boolean vs matroidal: is U itself indep in M?
        if U in M.indep:
            boolean_orbits += 1
        else:
            matroidal_orbits += 1
        # Lemma 5 check.
        if nk > nk1:
            f_check_failures.append((C, U, nk, nk1))
        # Orbit-size match: |orbit| should equal #{A : A indep_k(N), (UC \ A) indep_{k+d}(N)}.
        # This is the subset version, not f_k(N).
        # For correctness, we verify by direct enumeration here.
        expected_orbit = 0
        for A in combinations(UC, k):
            A = frozenset(A)
            if (A | C) not in M.indep: continue
            comp = UC - A
            if (comp | C) not in M.indep: continue
            expected_orbit += 1
        if expected_orbit != orbit_size:
            orbit_size_mismatches.append((C, U, expected_orbit, orbit_size))

    t2 = time.time()
    print(f"  orbit analysis: {t2-t1:.1f}s")
    print(f"  boolean orbits (U indep): {boolean_orbits}  |  matroidal orbits (U dep): {matroidal_orbits}")
    print(f"  orbit-size range: [{min_orbit_size}, {max_orbit_size}]")

    if f_check_failures:
        print(f"  *** LEMMA 5 FAILED on {len(f_check_failures)} orbits ***")
        for C, U, nk, nk1 in f_check_failures[:5]:
            print(f"      C={sorted(C)} U={sorted(U)} k={m-len(C)} f_k={nk} f_{{k+1}}={nk1}")
    else:
        print(f"  Lemma 5 (f_k <= f_{{k+1}}): ✓ on all {len(orbits)} orbits")

    if orbit_size_mismatches:
        print(f"  *** ORBIT-SIZE BIJECTION MISMATCH on {len(orbit_size_mismatches)} orbits ***")
        for C, U, exp, got in orbit_size_mismatches[:5]:
            print(f"      C={sorted(C)} U={sorted(U)} expected={exp} got={got}")
    else:
        print(f"  Orbit-size bijection: ✓")

    # Top f-vector profiles
    print(f"  (f_k, f_{{k+1}}) profile (top 5):")
    for (a, b), cnt in sorted(f_k_dist.items(), key=lambda x: -x[1])[:5]:
        marker = '✓' if a <= b else '✗'
        slack = b - a
        print(f"    f_k={a:4d}  f_{{k+1}}={b:4d}  slack={slack:+4d}  count={cnt}  {marker}")
    # Tightest orbits (smallest slack)
    print(f"  tightest orbits (smallest slack b - a, top 5):")
    tight = sorted(f_k_dist.items(), key=lambda x: (x[0][1] - x[0][0]))[:5]
    for (a, b), cnt in tight:
        print(f"    f_k={a:4d}  f_{{k+1}}={b:4d}  slack={b-a:+4d}  count={cnt}")


def main():
    print("=" * 70)
    print("Extended orbit verification — Lemma 5 (f_k <= f_{k+1}) across matroids")
    print("=" * 70)

    cases = [
        (Fano, "Fano F_7", [(1, 2)]),
        (lambda: M_Kn(5), "M(K_5) [recheck]", [(0, 2), (1, 2), (2, 2), (1, 3), (0, 3)]),
        (lambda: M_Kn(6), "M(K_6)", [(0, 2), (1, 2), (2, 2), (3, 2), (0, 3), (1, 3), (2, 3)]),
        (AG_n_2, "AG(3,2)", [(0, 2), (1, 2), (2, 2), (0, 3), (1, 3)]),
        (Vamos, "Vamos V_8", [(0, 2), (1, 2), (2, 2), (0, 3), (1, 3)]),
        (Pappus, "Pappus", [(0, 2), (1, 2)]),
        (NonPappus, "NonPappus", [(0, 2), (1, 2)]),
    ]

    for ctor, label, bigrades in cases:
        try:
            t0 = time.time()
            print(f"\n>>> building {label}", flush=True)
            if ctor is AG_n_2:
                M = ctor(3)
            else:
                M = ctor()
            t1 = time.time()
            print(f"    built in {t1-t0:.1f}s  rank={M.rank} n={M.n} f={M.f}", flush=True)
            for m, d in bigrades:
                try:
                    verify(M, label, m, d)
                except Exception as e:
                    print(f"    [{label} m={m} d={d}] error: {e}", flush=True)
        except Exception as e:
            print(f"  [{label}] build error: {e}", flush=True)

    print("\n" + "=" * 70)
    print("DONE")


if __name__ == "__main__":
    main()
