"""Test CONJ-A' (hybrid INJ): for M_1 >= M_2 (M_2 quotient of M_1),
L: R(M_1) \otimes R^v(M_2) ... INJ on degree blocks."""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from sparse_rank import Matroid, sparse_rank_modp, M_Kn

P = 10007


def hybrid_basis(M1, M2, e):
    """Pairs (S, T) with S indep in M1, T indep in M2, all in {0..n-1}.
       e = external degree |S| - |T| (in the convention we use).  Actually let's parametrize differently:
       (S, T) with |S| = m, |T| = m - e.  S in M1, T in M2."""
    out = []
    for m in range(M1.rank + 1):
        sT = m - e
        if sT < 0 or sT > M2.rank: continue
        for S in M1.by_size.get(m, []):
            for T in M2.by_size.get(sT, []):
                out.append((S, T))
    return out


def L_hybrid_entries(M1, M2, e, p, P):
    """Build L^p : (R(M_1) \otimes R^v(M_2))_e -> _{e+2p}.
    Action: same as before — mult-on-left in M_1, contract-on-right.  But the indep
    constraint on the LEFT uses M_1 (since x_i lives in R(M_1)), and the indep
    constraint on the RIGHT uses M_2.
    L^p(x_S \otimes y_T) = p! sum_{X subset T, |X|=p, S \cup X indep in M_1} x_{S \cup X} \otimes y_{T \setminus X}.
    For this to land in target, we also need T \ X indep in M_2 (which is automatic since T indep in M_2 and T \ X subset).
    """
    src = hybrid_basis(M1, M2, e)
    tgt = hybrid_basis(M1, M2, e + 2*p)
    tgt_idx = {st: i for i, st in enumerate(tgt)}
    rows, cols, vals = [], [], []
    factp = 1
    for k in range(1, p+1): factp *= k
    factp %= P

    for j, (S, T) in enumerate(src):
        T_list = list(T)
        for X_tup in combinations(T_list, p):
            X = frozenset(X_tup)
            if X & S: continue
            Snew = S | X
            if not M1.is_indep(Snew): continue
            Tnew = T - X
            i = tgt_idx[(frozenset(Snew), frozenset(Tnew))]
            rows.append(i); cols.append(j); vals.append(factp)
    return rows, cols, vals, len(src), len(tgt)


def make_quotient(M, e):
    """Compute M\e and M/e.  M\e indep: subsets S of [n]\{e} with S indep in M.
       M/e indep: subsets S of [n]\{e} with S U {e} indep in M.
       Both as matroids on the original ground set [n]\{e}.
    For our purposes we'll keep ground set [n] (with e treated as 'missing') and let
    R(M_1), R(M_2) generate from the right element set."""
    indep1 = []   # M\e
    indep2 = []   # M/e
    n = M.n
    for S in M.indep:
        if e in S: continue
        indep1.append(S)
        # S U {e} indep in M?
        if M.is_indep(S | {e}):
            indep2.append(S)
    M1 = Matroid(n, indep1)  # ground set still [n] but e is loop-like (no indep set contains it)
    M2 = Matroid(n, indep2)
    return M1, M2


def test_hybrid_inj(M_orig, e, label):
    M1, M2 = make_quotient(M_orig, e)
    print(f"\n[{label}]  M_orig f={M_orig.f}  e={e}", flush=True)
    print(f"  M\\e: f={M1.f} rank={M1.rank}    M/e: f={M2.f} rank={M2.rank}", flush=True)
    rkmin = min(M1.rank, M2.rank)
    rkmax = max(M1.rank, M2.rank)
    for d in range(1, rkmax + 1):
        # L (single step) - INJ check
        rows, cols, vals, ds, dt = L_hybrid_entries(M1, M2, -d, 1, P)
        if ds == 0 or dt == 0:
            print(f"  d={d} hybrid INJ: trivial (one piece empty)", flush=True)
            continue
        rk = sparse_rank_modp(rows, cols, vals, dt, ds, P, verbose=False)
        inj = (rk == ds)
        print(f"  d={d} hybrid L: S_-{d}({ds}) -> S_-{d-2}({dt}) rank={rk} "
              f"{'INJ ✓' if inj else f'ker={ds-rk} *FAIL*'}", flush=True)


if __name__ == "__main__":
    # Test hybrid CONJ-A' on M = M(K_5), various edges
    M = M_Kn(5)
    for e in [0, 1, 2]:  # try a few edges (they're all equivalent under Aut)
        test_hybrid_inj(M, e, f"K5_edge_{e}")
    # And on Fano
    lines = [frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
    bases = [b for b in combinations(range(7), 3) if frozenset(b) not in lines]
    Fano = Matroid.from_bases(7, bases)
    test_hybrid_inj(Fano, 0, "Fano_pt0")
