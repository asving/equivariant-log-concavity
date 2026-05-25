"""On orbits where Lemma 5 fails, verify the WEAKER statement that Theorem 4' needs:
   |O_hat_{C,U}|  <=  |O_hat'_{C,U}|.
Here  O_hat = {A in Indep_k(N) : (U\\C)\\A in Indep_{k+d}(N)} ,
      O_hat' = {A' in Indep_{k+1}(N) : (U\\C)\\A' in Indep_{k+d-1}(N)} .

If |O_hat| <= |O_hat'| holds even when f_k(N) > f_{k+1}(N), Theorem 4' is plausible.
"""
import sys, time
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from collections import defaultdict
from sparse_rank import M_Kn


def check_orbit_dims(M, label, m, d):
    print(f"\n=== {label}  m={m}, d={d} ===", flush=True)
    t0 = time.time()
    # Enumerate orbits.
    orbits = defaultdict(list)  # (C, U) -> [(S, T), ...]
    for S in M.by_size.get(m, []):
        for T in M.by_size.get(m+d, []):
            C = S & T
            U = S | T
            orbits[(C, U)].append((S, T))
    print(f"  # orbits = {len(orbits)}  (t={time.time()-t0:.1f}s)")

    total_orbits = 0
    lemma5_fails = 0
    dim_fails = 0
    fk_gt_fk1_examples = []
    strict_fails = []
    fk_dist = defaultdict(int)
    Ohat_dist = defaultdict(int)

    for (C, U), pairs in orbits.items():
        UC = U - C
        k = m - len(C)
        # f_k(N), f_{k+1}(N):
        fk = sum(1 for A in combinations(UC, k) if (frozenset(A) | C) in M.indep)
        fk1 = sum(1 for A in combinations(UC, k+1) if (frozenset(A) | C) in M.indep) if k+1 <= len(UC) else 0
        # |O_hat_{C,U}| and |O_hat'_{C,U}|:
        Ohat_k = 0
        for A in combinations(UC, k):
            A = frozenset(A)
            if (A | C) not in M.indep: continue
            comp = UC - A
            if (comp | C) not in M.indep: continue
            Ohat_k += 1
        Ohat_k1 = 0
        if k+1 <= len(UC):
            for A in combinations(UC, k+1):
                A = frozenset(A)
                if (A | C) not in M.indep: continue
                comp = UC - A
                if (comp | C) not in M.indep: continue
                Ohat_k1 += 1
        total_orbits += 1
        fk_dist[(fk, fk1)] += 1
        Ohat_dist[(Ohat_k, Ohat_k1)] += 1
        if fk > fk1:
            lemma5_fails += 1
            if len(fk_gt_fk1_examples) < 5:
                fk_gt_fk1_examples.append((C, U, k, fk, fk1, Ohat_k, Ohat_k1))
        if Ohat_k > Ohat_k1:
            dim_fails += 1
            if len(strict_fails) < 5:
                strict_fails.append((C, U, k, fk, fk1, Ohat_k, Ohat_k1))

    print(f"  Lemma 5 failures (f_k > f_{{k+1}}): {lemma5_fails} / {total_orbits}")
    print(f"  Theorem 4' dim failures (|O_hat_k| > |O_hat_{{k+1}}|): {dim_fails} / {total_orbits}")
    if fk_gt_fk1_examples:
        print(f"  Example Lemma-5-fail orbits (C, U, k, f_k, f_{{k+1}}, |Ohat_k|, |Ohat_{{k+1}}|):")
        for c, u, k, fk, fk1, oh, oh1 in fk_gt_fk1_examples:
            ok = "✓" if oh <= oh1 else "✗"
            print(f"    C={sorted(c)}  U={sorted(u)}  k={k}  f_k={fk}  f_{{k+1}}={fk1}  |Ohat_k|={oh}  |Ohat_{{k+1}}|={oh1}  {ok}")
    if strict_fails:
        print(f"  *** THEOREM 4' DIM FAILS ON {dim_fails} ORBITS ***")
        for c, u, k, fk, fk1, oh, oh1 in strict_fails:
            print(f"    C={sorted(c)}  U={sorted(u)}  k={k}  f_k={fk}  f_{{k+1}}={fk1}  |Ohat_k|={oh}  |Ohat_{{k+1}}|={oh1}")
    print(f"  Ohat (|Ohat_k|, |Ohat_{{k+1}}|) profile (top 5):")
    for (a, b), cnt in sorted(Ohat_dist.items(), key=lambda x: -x[1])[:5]:
        print(f"    |Ohat_k|={a:4d}  |Ohat_{{k+1}}|={b:4d}  slack={b-a:+4d}  count={cnt}")


if __name__ == "__main__":
    M = M_Kn(6)
    print(f"M(K_6): n={M.n}, rank={M.rank}, f={M.f}", flush=True)
    # Focus on the failing case.
    check_orbit_dims(M, "M(K_6)", 3, 2)
    # Also recheck M(K_6) m=2,3 d=3 and m=2 d=2 to compare:
    check_orbit_dims(M, "M(K_6)", 2, 2)
    check_orbit_dims(M, "M(K_6)", 2, 3)
