"""Check L^d: S_-d -> S_d (hard Lefschetz) for various M, d. Uses sparse."""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from sparse_rank import Matroid, Lpow_sparse_entries, sparse_rank_modp, M_Kn

P = 10007

def check(M, label, d):
    rows, cols, vals, ds, dt = Lpow_sparse_entries(M, -d, d, P)
    print(f"\n{label}  L^{d}: S_-{d}({ds}) -> S_{d}({dt})  nnz={len(rows)}", flush=True)
    r = sparse_rank_modp(rows, cols, vals, dt, ds, P)
    if r == ds == dt:
        print(f"  rank={r} ISO ✓", flush=True)
    elif r == ds:
        print(f"  rank={r} INJ but coker={dt-r}", flush=True)
    elif r == dt:
        print(f"  rank={r} SURJ but ker={ds-r}", flush=True)
    else:
        print(f"  rank={r} ker={ds-r} coker={dt-r}  *** HARD LEFSCHETZ FAILS ***", flush=True)
    return r, ds, dt

if __name__ == "__main__":
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else "K5_L2"
    if arg == "K5_L2":
        check(M_Kn(5), "M(K_5)", 2)
    elif arg == "K6_L2":
        check(M_Kn(6), "M(K_6)", 2)
    elif arg == "K6_L3":
        check(M_Kn(6), "M(K_6)", 3)
    elif arg == "K6_all":
        M = M_Kn(6)
        check(M, "M(K_6)", 1)
        check(M, "M(K_6)", 2)
        check(M, "M(K_6)", 3)
        check(M, "M(K_6)", 4)
        check(M, "M(K_6)", 5)
    else:
        print("usage: K5_L2 | K6_L2 | K6_L3 | K6_all")
