"""Test the Simple-Lemma-5 conjecture across simple matroids.

Simple-Lemma-5: For a SIMPLE matroid N on n' = 2k+d elements with rank r' >= k+d
and d >= 2, we have f_k(N) <= f_{k+1}(N).

Tests:
  (1) Catalog simple matroids: uniforms U_{r',n'}, graphic M(K_n), graphic M(G) for
      small simple graphs G, Fano F_7, NonFano, Vamos, AG(3,2), Pappus, NonPappus.
  (2) For each, for each valid (k, d) with 2k+d=n', r' >= k+d, d >= 2, check f_k <= f_{k+1}.
  (3) Also enumerate ALL N(C, U) arising from the orbit decomposition of test matroids,
      filter to SIMPLE ones, and check.
  (4) Track the SMALLEST slack (= f_{k+1} - f_k) and the RATIO f_{k+1}/f_k.

Output:
  Per-matroid table of (n', r', k, d, f_k, f_{k+1}, slack, ratio).
  Aggregate: total tested, total violations, worst ratio.
"""
import sys, time
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from collections import defaultdict
from gpu_rank import Matroid, Vamos, AG_n_2
from sparse_rank import M_Kn


def Pappus():
    lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,7),(1,4,8),(2,5,6),(0,4,6),(1,5,7),(2,3,8)]
    lines = [frozenset(l) for l in lines]
    bases = [b for b in combinations(range(9),3) if frozenset(b) not in lines]
    return Matroid.from_bases(9, bases)


def NonPappus():
    lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,7),(1,4,8),(0,4,6),(1,5,7),(2,3,8)]
    lines = [frozenset(l) for l in lines]
    bases = [b for b in combinations(range(9),3) if frozenset(b) not in lines]
    return Matroid.from_bases(9, bases)


def Fano():
    lines = [frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
    bases = [b for b in combinations(range(7), 3) if frozenset(b) not in lines]
    return Matroid.from_bases(7, bases)


def NonFano():
    """NonFano: like Fano but remove one of the 7 lines."""
    lines = [frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6)]]
    # Removed (2,4,5).
    bases = [b for b in combinations(range(7), 3) if frozenset(b) not in lines]
    return Matroid.from_bases(7, bases)


def is_simple_matroid(M):
    """Simple: no loops (every singleton indep) and no parallel pairs."""
    for i in range(M.n):
        if frozenset([i]) not in M.indep:
            return False
    for i, j in combinations(range(M.n), 2):
        if frozenset([i, j]) not in M.indep:
            return False
    return True


def check_one(M, label, verbose=True):
    """For each valid (k, d) with 2k+d=n', r'>=k+d, d>=2, check f_k<=f_{k+1}."""
    n = M.n
    r = M.rank
    results = []
    for k in range(0, (n - 2) // 2 + 1):
        d = n - 2 * k
        if d < 2: continue
        if r < k + d: continue
        fk = len(M.by_size.get(k, []))
        fk1 = len(M.by_size.get(k + 1, []))
        slack = fk1 - fk
        ratio = fk1 / fk if fk > 0 else None
        ok = slack >= 0
        results.append((n, r, k, d, fk, fk1, slack, ratio, ok))
        if verbose:
            marker = '✓' if ok else '✗'
            print(f"  {label}  n'={n} r'={r} k={k} d={d}   f_k={fk:7d}  f_{{k+1}}={fk1:7d}  "
                  f"slack={slack:+6d}  ratio={ratio:.4f}  {marker}", flush=True)
    return results


def make_NC_U(M, C, U):
    """Build the matroid N(C, U) := (M/C) | _{U \\ C}.
    Indep sets: A subset of U\\C with A union C indep in M."""
    UC = U - C
    UC_list = sorted(UC)
    idx = {e: i for i, e in enumerate(UC_list)}
    n_new = len(UC_list)
    indep = []
    for k in range(n_new + 1):
        for A in combinations(UC_list, k):
            if (frozenset(A) | C) in M.indep:
                indep.append(frozenset(idx[e] for e in A))
    return Matroid(n_new, indep)


def harvest_NCU_simple(M, label, max_orbits=2000):
    """For each (m, d) bigrade, enumerate orbits and collect SIMPLE N(C,U)."""
    print(f"\n--- harvesting N(C,U) from {label} (rank {M.rank}) ---", flush=True)
    simple_NCU = []  # list of (n', r', N) where N is simple
    seen = set()  # to dedupe identical matroids by their indep set fingerprint
    for m in range(M.rank):
        for d in range(2, M.rank - m + 1):
            try_pairs = []
            for S in M.by_size.get(m, []):
                for T in M.by_size.get(m+d, []):
                    try_pairs.append((S, T))
                    if len(try_pairs) > max_orbits:
                        break
                if len(try_pairs) > max_orbits: break
            print(f"   m={m} d={d}: {len(try_pairs)} pairs", flush=True)
            orbits = {}
            for S, T in try_pairs:
                C, U = S & T, S | T
                orbits.setdefault((C, U), None)
            ncu_simple_count = 0
            for (C, U), _ in orbits.items():
                N = make_NC_U(M, C, U)
                if is_simple_matroid(N):
                    # Fingerprint by indep set tuple.
                    fp = (N.n, N.rank, tuple(sorted(N.f)))
                    if fp in seen: continue
                    seen.add(fp)
                    simple_NCU.append((N, label, m, d, C, U))
                    ncu_simple_count += 1
            print(f"     -> {len(orbits)} orbits, {ncu_simple_count} new SIMPLE N(C,U)", flush=True)
    return simple_NCU


def main():
    print("=" * 70)
    print("Simple-Lemma-5 conjecture test")
    print("=" * 70)

    # (A) Direct simple matroids — check the conjecture on them.
    direct = [
        ("U_{2,2}", Matroid.uniform(2, 2)),
        ("U_{3,3}", Matroid.uniform(3, 3)),
        ("U_{3,4}", Matroid.uniform(3, 4)),
        ("U_{3,5}", Matroid.uniform(3, 5)),
        ("U_{3,6}", Matroid.uniform(3, 6)),
        ("U_{4,4}", Matroid.uniform(4, 4)),
        ("U_{4,5}", Matroid.uniform(4, 5)),
        ("U_{4,6}", Matroid.uniform(4, 6)),
        ("U_{4,7}", Matroid.uniform(4, 7)),
        ("U_{4,8}", Matroid.uniform(4, 8)),
        ("U_{5,6}", Matroid.uniform(5, 6)),
        ("U_{5,7}", Matroid.uniform(5, 7)),
        ("U_{5,8}", Matroid.uniform(5, 8)),
        ("U_{5,10}", Matroid.uniform(5, 10)),
        ("U_{6,6}", Matroid.uniform(6, 6)),
        ("U_{6,8}", Matroid.uniform(6, 8)),
        ("U_{6,10}", Matroid.uniform(6, 10)),
        ("M(K_4)", M_Kn(4)),
        ("M(K_5)", M_Kn(5)),
        ("M(K_6)", M_Kn(6)),
        ("Fano F_7", Fano()),
        ("NonFano F_7^-", NonFano()),
        ("Pappus", Pappus()),
        ("NonPappus", NonPappus()),
        ("AG(3,2)", AG_n_2(3)),
        ("Vamos V_8", Vamos()),
    ]

    all_results = []
    violations = []
    for label, M in direct:
        if not is_simple_matroid(M):
            print(f"\n>>> {label}: NOT SIMPLE — skip", flush=True)
            continue
        print(f"\n>>> {label}  (simple, n={M.n}, rank={M.rank}, f={M.f})", flush=True)
        res = check_one(M, label, verbose=True)
        all_results.extend(res)
        for r in res:
            if not r[8]: violations.append((label, r))

    # (B) Harvest N(C, U) sub-matroids that happen to be SIMPLE, test on them.
    print("\n" + "=" * 70)
    print("PART (B): Simple N(C,U) sub-matroids from orbits")
    print("=" * 70)
    harvested = []
    for label, M in [("M(K_4)", M_Kn(4)), ("M(K_5)", M_Kn(5)), ("M(K_6)", M_Kn(6)),
                     ("AG(3,2)", AG_n_2(3)), ("Vamos V_8", Vamos()), ("Pappus", Pappus()),
                     ("Fano", Fano())]:
        try:
            ncu = harvest_NCU_simple(M, label, max_orbits=5000)
            harvested.extend(ncu)
        except Exception as e:
            print(f"  {label}: harvest failed — {e}", flush=True)

    print(f"\n>>> {len(harvested)} distinct SIMPLE N(C,U) found among harvested orbits")
    ncu_violations = []
    for N, src_label, m, d_orbit, C, U in harvested:
        # For each (k, d) bigrade of N, check.
        for k in range(0, (N.n - 2) // 2 + 1):
            d = N.n - 2 * k
            if d < 2: continue
            if N.rank < k + d: continue
            fk = len(N.by_size.get(k, []))
            fk1 = len(N.by_size.get(k + 1, []))
            slack = fk1 - fk
            if slack < 0:
                ncu_violations.append((src_label, m, d_orbit, sorted(C), sorted(U), N.n, N.rank, k, d, fk, fk1))
                print(f"  *** SIMPLE NCU VIOLATION ***  src={src_label} m={m} d={d_orbit} "
                      f"C={sorted(C)} U={sorted(U)} -> N n'={N.n} r'={N.rank} k={k} d={d}  "
                      f"f_k={fk} f_{{k+1}}={fk1}", flush=True)

    # Summary
    print("\n" + "=" * 70)
    print(f"PART (A) direct: {len(all_results)} (matroid, k, d) cases tested, {len(violations)} violations.")
    if violations:
        for label, r in violations:
            print(f"   *** {label}  n'={r[0]} r'={r[1]} k={r[2]} d={r[3]}  "
                  f"f_k={r[4]} f_{{k+1}}={r[5]} ratio={r[7]:.4f}")
    else:
        print("   No violations in (A).")
    print(f"PART (B) N(C,U) sub-matroids: {len(harvested)} simple Ns harvested, {len(ncu_violations)} violations.")
    if not ncu_violations:
        print("   No violations in (B).")

    # Worst-case ratios
    if all_results:
        worst = min((r for r in all_results if r[6] >= 0), key=lambda r: r[7])
        best = max(all_results, key=lambda r: r[7])
        print(f"\nTightest case (smallest ratio f_{{k+1}}/f_k): n'={worst[0]} r'={worst[1]} k={worst[2]} d={worst[3]} ratio={worst[7]:.4f}")


if __name__ == "__main__":
    main()
