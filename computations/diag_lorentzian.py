"""
Diagonal-Lorentzian test:
  For each test matroid M and each internal m, compute the matrix L of
    L : R_m \otimes R^v_{-(m+2)}  ->  R_{m+1} \otimes R^v_{-(m+1)}
  Then form L^T L (symmetric, positive-semidefinite by construction).
  Compute eigenvalues over R using numpy. Report smallest, largest, condition number,
  and whether L^T L is positive-definite (= L injective over R).

Note: we already know L is INJ over F_10007 for our test matroids; this test verifies
positive-definiteness over R (which is automatic but the spectrum is informative —
shows how "robust" the injectivity is).
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
import numpy as np
from sparse_rank import Matroid, M_Kn

def L_block_matrix(M, m, d=2):
    """Build the dense L^d matrix restricted to internal-degree-m block:
    (R_m \otimes R^v_{-(m+d)}) -> (R_{m+d} \otimes R^v_{-m}).
    For d=1 this is the L: S_-1 -> S_+1 block in user's INJ direction; here we use d=2
    by default but the function generalizes.
    Actually we want L itself (not L^d) for the INJ test, so use d=1 step but operate
    on (m, -d_ext) -> (m+1, -d_ext+2).  Specifically: source block is the (m, -2) piece
    of S_{-2}, which is R_m \otimes R^v_{-(m+2)}.
    L sends this to R_{m+1} \otimes R^v_{-(m+1)}.
    """
    # Source basis: (S, T) with S indep |S|=m, T indep |T|=m+d
    src = [(S, T) for S in M.by_size.get(m, []) for T in M.by_size.get(m+d, [])]
    # Target basis: (S', T') with |S'|=m+1, |T'|=m+d-1
    tgt = [(S, T) for S in M.by_size.get(m+1, []) for T in M.by_size.get(m+d-1, [])]
    tgt_idx = {st: i for i, st in enumerate(tgt)}
    A = np.zeros((len(tgt), len(src)), dtype=np.float64)
    for j, (S, T) in enumerate(src):
        for i in T:
            if i in S: continue
            Snew = S | {i}
            if not M.is_indep(Snew): continue
            Tnew = T - {i}
            row = tgt_idx[(frozenset(Snew), frozenset(Tnew))]
            A[row, j] += 1.0
    return A, src, tgt


def test_matroid(M, label):
    rk = M.rank
    print(f"\n=== {label}  f={M.f} rank={rk} ===", flush=True)
    for m in range(0, rk):  # need m+2 <= rk for the block to be non-trivial
        if m + 2 > rk: break
        if M.f[m] == 0 or M.f[m+2] == 0: continue
        # Build L
        A, src, tgt = L_block_matrix(M, m, d=2)
        src_dim = len(src)
        tgt_dim = len(tgt)
        if src_dim == 0:
            continue
        # Compute L^T L (source-side Gram matrix)
        LtL = A.T @ A
        # Compute eigenvalues (LtL is symmetric pos-semidef)
        eigs = np.linalg.eigvalsh(LtL)
        eigs_sorted = np.sort(eigs)
        smin = eigs_sorted[0]
        smax = eigs_sorted[-1]
        n_zero = int(np.sum(eigs_sorted < 1e-8))
        cond = smax / smin if smin > 1e-12 else float('inf')
        # Also dim source vs target
        rank_estimate = src_dim - n_zero
        inj = (n_zero == 0)
        print(f"  m={m}: src({src_dim})->tgt({tgt_dim})  L^T L spectrum: "
              f"min={smin:.3g} max={smax:.3g} cond={cond:.3g} "
              f"#~zero={n_zero}  "
              f"{'POS-DEF (INJ ✓)' if inj else f'kernel dim {n_zero}'}",
              flush=True)


if __name__ == "__main__":
    matroids = [
        (M_Kn(4), "M(K_4)"),
        (M_Kn(5), "M(K_5)"),
    ]
    # M(K_6) is too big for dense (683k × 683k floats = 3.7TB); skip or do block-by-block per m.
    for M, label in matroids:
        test_matroid(M, label)
    # M(K_6) per-m: each m-block is much smaller. Largest block: m=3, f_3 f_5 = 435*1296 = 563760, target same. Dense matrix would be 564k × 564k = 2.5TB floats. Too big.
    # m=2 block: f_2 f_4 = 105*1080 = 113400, target 435*15 = 6525. Dense L: 6525 × 113400 -> 600 MB float64.
    # L^T L: 113400 × 113400 -> 100 GB. Doable on GPU but slow.
    # m=1 block: f_1 f_3 = 15*435 = 6525, target f_2 f_2 = 11025. Dense L: 11025 × 6525 = 70 MB. L^T L: 6525×6525 = 340 MB. Easy.
    # m=0 block: f_0 f_2 = 105. Trivial.
    K6 = M_Kn(6)
    print(f"\n=== M(K_6)  f={K6.f} (per-m, smaller blocks) ===", flush=True)
    for m in [0, 1]:
        if m + 2 > K6.rank: break
        A, src, tgt = L_block_matrix(K6, m, d=2)
        if A.shape[1] == 0: continue
        LtL = A.T @ A
        eigs = np.linalg.eigvalsh(LtL)
        smin = float(eigs.min()); smax = float(eigs.max())
        n_zero = int(np.sum(eigs < 1e-8))
        cond = smax / smin if smin > 1e-12 else float('inf')
        inj = (n_zero == 0)
        print(f"  m={m}: src({A.shape[1]})->tgt({A.shape[0]})  "
              f"L^T L: min={smin:.3g} max={smax:.3g} cond={cond:.3g} "
              f"#~zero={n_zero}  "
              f"{'POS-DEF (INJ ✓)' if inj else f'kernel dim {n_zero}'}",
              flush=True)
