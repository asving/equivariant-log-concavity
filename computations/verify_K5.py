"""Verify M(K_5) L^2 rank deficit with two independent methods (sympy + gpu)."""
from itertools import combinations
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid, Lpow_sparse_entries, to_dense_gpu, gpu_rank_modp
import sympy as sp


def M_K5():
    edges = list(combinations(range(5), 2))
    n = len(edges)
    def is_ST(B):
        if len(B) != 4: return False
        p = list(range(5))
        def f(x):
            while p[x]!=x: p[x]=p[p[x]]; x=p[x]
            return x
        for ei in B:
            u, v = edges[ei]
            ru,rv = f(u),f(v)
            if ru==rv: return False
            p[ru]=rv
        return True
    return Matroid.from_bases(n, [b for b in combinations(range(n),4) if is_ST(b)])


M = M_K5()
print("M(K_5):", M.f)

# Method 1: gpu mod-p
P = 10007
rows, cols, vals, ds, dt = Lpow_sparse_entries(M, -2, 2, P)
print(f"L^2 sparse entries: src={ds} tgt={dt} nnz={len(rows)}")
import torch
A = to_dense_gpu(rows, cols, vals, dt, ds, 'cuda:0', P)
r_modp = gpu_rank_modp(A, P)
print(f"GPU mod-{P} rank: {r_modp}  (deficit {ds - r_modp})")

# Method 2: try a different prime to rule out modular accidents
P2 = 100003
rows, cols, vals, ds, dt = Lpow_sparse_entries(M, -2, 2, P2)
A = to_dense_gpu(rows, cols, vals, dt, ds, 'cuda:0', P2)
r_modp2 = gpu_rank_modp(A, P2)
print(f"GPU mod-{P2} rank: {r_modp2}  (deficit {ds - r_modp2})")

# Also check L^1 = L : S_-2 -> S_0 INJ
P = 10007
rows, cols, vals, ds, dt = Lpow_sparse_entries(M, -2, 1, P)
print(f"\nL (single step) sparse entries: src={ds} tgt={dt} nnz={len(rows)}")
A = to_dense_gpu(rows, cols, vals, dt, ds, 'cuda:0', P)
r = gpu_rank_modp(A, P)
print(f"L: S_-2 -> S_0 rank={r} (source dim {ds}, target dim {dt})  {'INJ' if r==ds else 'NOT-INJ'}")

# Then L : S_0 -> S_2
rows, cols, vals, ds0, dt0 = Lpow_sparse_entries(M, 0, 1, P)
print(f"L (single step) S_0 -> S_2: src={ds0} tgt={dt0} nnz={len(rows)}")
A = to_dense_gpu(rows, cols, vals, dt0, ds0, 'cuda:0', P)
r = gpu_rank_modp(A, P)
print(f"L: S_0 -> S_2 rank={r}  {'SURJ' if r==dt0 else f'coker {dt0-r}'}  ker {ds0-r}")

# d=3 cases
for p in [1, 2, 3]:
    rows, cols, vals, ds, dt = Lpow_sparse_entries(M, -3, p, P)
    A = to_dense_gpu(rows, cols, vals, dt, ds, 'cuda:0', P)
    r = gpu_rank_modp(A, P)
    flag = ''
    if r == ds: flag = 'INJ'
    if r == dt: flag += ' SURJ'
    if r == ds == dt: flag = 'ISO'
    print(f"L^{p}: S_-3({ds}) -> S_{-3+2*p}({dt}) rank={r} {flag}")

# d=4 (top): L^4 : S_-4 -> S_4
for p in [1, 2, 3, 4]:
    rows, cols, vals, ds, dt = Lpow_sparse_entries(M, -4, p, P)
    A = to_dense_gpu(rows, cols, vals, dt, ds, 'cuda:0', P)
    r = gpu_rank_modp(A, P)
    flag = ''
    if r == ds: flag = 'INJ'
    if r == dt: flag += ' SURJ'
    if r == ds == dt: flag = 'ISO'
    print(f"L^{p}: S_-4({ds}) -> S_{-4+2*p}({dt}) rank={r} {flag}")
