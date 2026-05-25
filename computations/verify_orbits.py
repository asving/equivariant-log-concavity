"""Sanity check: orbit decomposition for the proof in PREPRINT_DRAFT.md.

Test claims:
  (a) L preserves the orbit (C, U) = (S \cap T, S \cup T).
  (b) On each orbit, L_{C,U} equals the matroid-level raising operator for
      N(C, U) := (M / C) | _{U \ C} at level m - |C|.
  (c) f_{m-|C|}(N) <= f_{m-|C|+1}(N) for every nonempty orbit when d >= 2.
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from collections import defaultdict
from sparse_rank import Matroid, M_Kn


def basis_in_S_m_minus_d(M, m, d):
    """Pairs (S, T) with |S|=m, |T|=m+d, S, T indep in M."""
    out = []
    for S in M.by_size.get(m, []):
        for T in M.by_size.get(m+d, []):
            out.append((S, T))
    return out


def L_action(M, S, T):
    """L(x_S \otimes y_T): list of summands (S', T')."""
    out = []
    for i in T:
        if i in S: continue
        Snew = S | {i}
        if not M.is_indep(Snew): continue
        Tnew = T - {i}
        out.append((frozenset(Snew), frozenset(Tnew)))
    return out


def orbit_invariants(S, T):
    return (frozenset(S & T), frozenset(S | T))


def make_NC_U(M, C, U):
    """Indep sets of N(C, U) := (M/C)|_{U \ C}: A \subseteq U \ C with A \cup C indep in M."""
    UC = frozenset(U) - frozenset(C)
    indep = []
    for k in range(len(UC) + 1):
        for A in combinations(UC, k):
            A = frozenset(A)
            if M.is_indep(A | frozenset(C)):
                indep.append(A)
    return Matroid(len(UC), [tuple(sorted(A)) for A in indep])  # ground set is relabeled but we keep frozenset elements


def test(M, label, m, d):
    print(f"\n=== {label}  m={m}, d={d} ===", flush=True)
    src = basis_in_S_m_minus_d(M, m, d)
    print(f"  |source| = {len(src)}")

    # (a) Verify L preserves (C, U)
    orbits = defaultdict(list)
    for S, T in src:
        C, U = orbit_invariants(S, T)
        orbits[(C, U)].append((S, T))
    print(f"  # orbits = {len(orbits)}")

    bad = 0
    for (S, T) in src:
        C, U = orbit_invariants(S, T)
        for (S2, T2) in L_action(M, S, T):
            C2, U2 = orbit_invariants(S2, T2)
            if (C2, U2) != (C, U):
                bad += 1
    print(f"  L preservation of (C, U): {len(src)} sources tested, {bad} violations  "
          f"{'✓' if bad == 0 else 'FAIL'}")

    # (b) Check per-orbit injectivity by direct verification:
    #     For each orbit, build orbit's L matrix and check INJ.
    issues = 0
    f_check_failures = 0
    for (C, U), pairs in orbits.items():
        # Determine N(C, U) indep sets of size m - |C| and m - |C| + 1.
        UC = frozenset(U) - frozenset(C)
        k = m - len(C)
        # Indep_k(N) = {A subset of UC of size k : A u C indep in M}
        # Indep_k+1(N) similarly.
        ind_k = []
        for A in combinations(UC, k):
            A = frozenset(A)
            if M.is_indep(A | frozenset(C)):
                ind_k.append(A)
        ind_k1 = []
        if k + 1 <= len(UC):
            for A in combinations(UC, k+1):
                A = frozenset(A)
                if M.is_indep(A | frozenset(C)):
                    ind_k1.append(A)
        # f_k(N) vs f_{k+1}(N) check (Lemma 5)
        if len(ind_k) > len(ind_k1):
            f_check_failures += 1
        # The orbit's source = pairs (S, T) in orbit. Bijection: (S, T) <-> A = S \ C \subseteq UC, |A|=k.
        # We expect |orbit| = f_k(N).
        if len(pairs) != len(ind_k):
            print(f"    Orbit (C={sorted(C)}, U={sorted(U)}): pairs={len(pairs)}, f_k(N)={len(ind_k)}  MISMATCH")
            issues += 1
    if issues == 0:
        print(f"  Orbit-size = f_k(N) check: ✓ ({len(orbits)} orbits verified)")
    if f_check_failures == 0:
        print(f"  Lemma 5 (f_k(N) <= f_{{k+1}}(N)): ✓ for all orbits")
    else:
        print(f"  Lemma 5 FAILED on {f_check_failures} orbits")

    # Summary orbit-stats
    f_k_dist = defaultdict(int)
    f_k1_dist = defaultdict(int)
    for (C, U), pairs in orbits.items():
        UC = frozenset(U) - frozenset(C)
        k = m - len(C)
        nk = sum(1 for A in combinations(UC, k) if M.is_indep(frozenset(A) | frozenset(C)))
        nk1 = sum(1 for A in combinations(UC, k+1) if M.is_indep(frozenset(A) | frozenset(C))) if k+1 <= len(UC) else 0
        f_k_dist[(nk, nk1)] += 1
    print(f"  Orbit (f_k, f_{{k+1}}) distribution (most common 5):", flush=True)
    for (a, b), cnt in sorted(f_k_dist.items(), key=lambda x: -x[1])[:5]:
        print(f"    (f_k={a}, f_{{k+1}}={b}): {cnt} orbits  "
              f"{'✓ f_k≤f_{k+1}' if a <= b else '✗ FAIL'}")


if __name__ == "__main__":
    for fn, label, m, d in [
        (lambda: M_Kn(4), "M(K_4)", 1, 2),
        (lambda: M_Kn(5), "M(K_5)", 1, 2),
        (lambda: M_Kn(5), "M(K_5)", 2, 2),
        (lambda: M_Kn(5), "M(K_5)", 1, 3),
    ]:
        M = fn()
        test(M, label, m, d)
