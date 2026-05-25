"""Uniform U_{r,n} scaling test, up to rank 10. Test user's INJ + CONJ-A."""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from sparse_rank import Matroid, Lpow_sparse_entries, sparse_rank_modp

P = 10007

def test_uniform(r, n):
    M = Matroid.uniform(r, n)
    print(f"\n=== U_{{{r},{n}}}  f={M.f} ===", flush=True)
    # INJ tests at d=2 and the user's conjecture
    for d in range(2, min(r, 5) + 1):
        rows, cols, vals, ds, dt = Lpow_sparse_entries(M, -d, 1, P)
        rk = sparse_rank_modp(rows, cols, vals, dt, ds, P, verbose=False)
        inj = (rk == ds)
        print(f"  d={d}: L INJ check: src={ds} tgt={dt} rank={rk} "
              f"{'INJ ✓' if inj else f'ker={ds-rk} *FAIL*'}", flush=True)
        # CONJ-A
        rows, cols, vals, ds, dt = Lpow_sparse_entries(M, -d, d, P)
        rk = sparse_rank_modp(rows, cols, vals, dt, ds, P, verbose=False)
        if rk == ds == dt:
            print(f"        L^{d}: ISO ✓", flush=True)
        else:
            print(f"        L^{d}: rank={rk} (deficit {ds-rk})  *CONJ-A FAILS*", flush=True)

if __name__ == "__main__":
    # rank 5 through 10
    pairs = []
    pairs.append((5, 10))
    pairs.append((6, 10))
    pairs.append((7, 11))
    pairs.append((8, 11))
    pairs.append((9, 11))
    pairs.append((10, 11))
    pairs.append((10, 12))
    for r, n in pairs:
        try:
            test_uniform(r, n)
        except Exception as e:
            print(f"  ERROR U_{{{r},{n}}}: {e}", flush=True)
