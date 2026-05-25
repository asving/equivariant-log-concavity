"""
Match L^T L to the ALOGV down-up Markov chain on (S, T) pairs.

ALOGV's down-up walk on size-k indep sets:
  Given S of size k, "down" to S' = S \ {i} for random i; "up" to S' \cup {j} for random j s.t. result indep.

For our pair walk on (m, m+2)-bigrade:
  state = (S, T) with |S|=m, |T|=m+2, S,T indep.
  step: choose i ∈ T with S∪{i} indep, move to (S∪{i}, T\{i}).

Define:
  L : pair_(m, m+2) -> pair_(m+1, m+1) bipartite adjacency (matrix entries are 1 if swap valid).

Then L^T L on source has entries:
  (L^T L)_{(S,T), (S',T')} = # ways to "go forward and come back": exists i, j with
       (S∪i, T\i) = (S∪j) ... etc.
  Equivalently: (S, T) and (S', T') share a common "next" pair (S∪i, T\i).
  = # i ∈ T ∩ T' with S∪i indep AND S∪i = S'∪j for some j, but I'll just compute directly.

Compare to the "matroid-link" walk Laplacian Anari et al. analyze.
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
import numpy as np
from sparse_rank import Matroid, M_Kn
from diag_lorentzian import L_block_matrix


def LtL_explicit(M, m):
    """Return L^T L as a dense matrix on source basis (S, T), |S|=m, |T|=m+2."""
    A, src, tgt = L_block_matrix(M, m, d=2)
    return A.T @ A, src, tgt


def diagonal_LtL(M, m):
    """Compute (L^T L)_{(S,T), (S,T)} for each (S,T) source.
    = # i in T with i not in S and S∪i indep AND for some j... actually:

    (L^T L)_{(S,T), (S,T)} = sum_i [i ∈ T, i ∉ S, S∪i indep]  (the # valid forward moves)
    """
    src = [(S, T) for S in M.by_size.get(m, []) for T in M.by_size.get(m+2, [])]
    out = []
    for S, T in src:
        cnt = sum(1 for i in T if i not in S and M.is_indep(S | {i}))
        out.append(cnt)
    return out, src


def explain_spectrum(M, label, m):
    """For one (m, M), compute L^T L spectrum AND the diagonal counts."""
    LtL, src, tgt = LtL_explicit(M, m)
    eigs = np.linalg.eigvalsh(LtL)
    eigs_int = [int(round(e)) for e in eigs]
    print(f"\n[{label}, m={m}]  L^T L: {len(src)}x{len(src)}")
    print(f"  eigenvalues (sorted): {sorted(set(eigs_int))}")
    # Print histogram
    from collections import Counter
    hist = Counter(eigs_int)
    print(f"  eigenvalue multiplicities: {dict(sorted(hist.items()))}")

    diag, _ = diagonal_LtL(M, m)
    diag_hist = Counter(diag)
    print(f"  diagonal entry distribution: {dict(sorted(diag_hist.items()))}")
    print(f"  (= # valid forward moves per (S,T) source)")
    print(f"  trace of L^T L = sum of diag = {sum(diag)} = sum of eigs = {sum(eigs_int)}")


if __name__ == "__main__":
    print("=== L^T L structure analysis ===")
    for fn, label, ms in [
        (lambda: M_Kn(4), "M(K_4)", [0, 1]),
        (lambda: M_Kn(5), "M(K_5)", [0, 1, 2]),
        (lambda: M_Kn(6), "M(K_6)", [0, 1]),
    ]:
        M = fn()
        print(f"\n--- {label}  f={M.f} ---")
        for m in ms:
            if m + 2 > M.rank: continue
            explain_spectrum(M, label, m)
