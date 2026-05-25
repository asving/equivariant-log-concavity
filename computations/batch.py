"""Batch tests on graphic matroids — check user's conjecture (L INJ) at all d vs CONJ-A (L^d ISO)."""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from sparse_rank import Matroid, Lpow_sparse_entries, sparse_rank_modp, M_Kn

P = 10007

def test_one(M, label, d, p_for_Lpow=None):
    """If p_for_Lpow=p, check L^p: S_-d -> S_-d+2p.  Default p=1 (user's INJ check)."""
    p = p_for_Lpow if p_for_Lpow is not None else 1
    rows, cols, vals, ds, dt = Lpow_sparse_entries(M, -d, p, P)
    rk = sparse_rank_modp(rows, cols, vals, dt, ds, P, verbose=False)
    return ds, dt, rk

def run(M, label):
    print(f"\n=== {label}  f={M.f} rank={M.rank} ===", flush=True)
    for d in range(1, M.rank + 1):
        # user's INJ check (L: S_-d -> S_-d+2)
        ds, dt, rk = test_one(M, label, d, p_for_Lpow=1)
        inj = (rk == ds)
        print(f"  d={d}  L: S_-{d}({ds}) -> S_-{d-2}({dt})  rank={rk}  "
              f"{'INJ ✓' if inj else f'ker={ds-rk}  *FAIL INJ*'}", flush=True)
        # CONJ-A check at the same d (L^d : S_-d -> S_d)
        ds, dt, rk = test_one(M, label, d, p_for_Lpow=d)
        if ds == dt == rk:
            print(f"        L^{d}: S_-{d}->S_{d} ISO ✓", flush=True)
        elif rk == ds:
            print(f"        L^{d}: rank={rk}=src, coker={dt-rk}  (INJ-only)", flush=True)
        elif rk == dt:
            print(f"        L^{d}: rank={rk}=tgt, ker={ds-rk}  (SURJ-only)", flush=True)
        else:
            print(f"        L^{d}: rank={rk} ker={ds-rk} coker={dt-rk}  **FAIL CONJ-A**", flush=True)

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "K5"
    if arg == "K4": run(M_Kn(4), "M(K_4)")
    elif arg == "K5": run(M_Kn(5), "M(K_5)")
    elif arg == "K6": run(M_Kn(6), "M(K_6)")
    elif arg == "K7": run(M_Kn(7), "M(K_7)")
    else: print("usage: K4|K5|K6|K7")
