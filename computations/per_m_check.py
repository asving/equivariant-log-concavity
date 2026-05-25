"""Check L^d ranks restricted to fixed internal degree m (= |S|) for each m."""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from sparse_rank import Matroid, sparse_rank_modp, M_Kn

P = 10007

def basis_at_m_e(M, m, e):
    sT = m - e
    out = []
    if sT < 0 or sT > M.rank: return out
    for S in M.by_size.get(m, []):
        for T in M.by_size.get(sT, []):
            out.append((S, T))
    return out

def Lpow_per_m(M, m, d, p, P):
    """L^p on the m-block at external degree -d:
       (R_m \otimes R^v_-(m+d)) -> (R_{m+p} \otimes R^v_-(m+d-p)).
    """
    src = basis_at_m_e(M, m, -d)
    tgt = basis_at_m_e(M, m + p, -d + 2*p)
    tgt_idx = {st: i for i, st in enumerate(tgt)}
    rows, cols, vals = [], [], []
    factp = 1
    for k in range(1, p+1): factp *= k
    factp %= P
    for j, (S, T) in enumerate(src):
        for X_tup in combinations(T, p):
            X = frozenset(X_tup)
            if X & S: continue
            Snew = S | X
            if not M.is_indep(Snew): continue
            Tnew = T - X
            i = tgt_idx[(frozenset(Snew), frozenset(Tnew))]
            rows.append(i); cols.append(j); vals.append(factp)
    return rows, cols, vals, len(src), len(tgt)

def lc_defect(M, m):
    """f_m^2 - f_{m-1} f_{m+1}."""
    f = list(M.f) + [0]
    if m-1 < 0 or m+1 >= len(f): return None
    return f[m]**2 - f[m-1]*f[m+1]

def newton_defect(M, m, d):
    """f_{m+(d/2)}^2 - f_m * f_{m+d}? Generalize."""
    pass

def run(M, label):
    rk = M.rank
    print(f"\n=== {label} f={M.f} rank={rk} ===", flush=True)
    for d in range(2, rk + 1):
        print(f"\n d={d}  (L^{d}: -d -> d, hard Lefschetz)", flush=True)
        total_def = 0
        for m in range(rk + 1):
            rows, cols, vals, ds, dt = Lpow_per_m(M, m, d, d, P)
            if ds == 0: continue
            rkk = sparse_rank_modp(rows, cols, vals, dt, ds, P, verbose=False)
            iso = (rkk == ds == dt)
            defect = ds - rkk
            total_def += defect
            print(f"   m={m}: L^{d}: ({ds}->{dt}) rank={rkk} "
                  f"{'ISO ✓' if iso else f'deficit={defect}'}", flush=True)
        print(f"   total deficit at d={d}: {total_def}", flush=True)

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "K5"
    if arg == "K5": run(M_Kn(5), "M(K_5)")
    elif arg == "K6": run(M_Kn(6), "M(K_6)")
    elif arg == "K7": run(M_Kn(7), "M(K_7)")
    else: print("usage K5|K6|K7")
