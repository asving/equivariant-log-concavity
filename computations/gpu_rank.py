"""
GPU-accelerated mod-p rank computation for big sparse matrices.

Strategy:
  - Build L^d as a sparse matrix over Z mod p.
  - Convert to dense torch tensor on GPU for moderate sizes (up to ~50k x 50k single GPU).
  - For larger sizes, use sparse GE (TODO if needed).
  - All arithmetic mod a fixed prime P (default 10007).

API:
  rank_modp_gpu(rows, cols, indices, values, P, device) -> int
"""
from __future__ import annotations
from itertools import combinations
import time
import torch
import numpy as np


# ---------------- Matroid ----------------

class Matroid:
    def __init__(self, n, independents):
        self.n = n
        self.indep = set(frozenset(s) for s in independents)
        self.by_size = {}
        for S in self.indep:
            self.by_size.setdefault(len(S), []).append(S)
        for d in self.by_size:
            self.by_size[d].sort(key=lambda s: sorted(s))
        self.rank = max(self.by_size) if self.by_size else 0
        self.f = tuple(len(self.by_size.get(d, [])) for d in range(self.rank + 1))

    def is_indep(self, S):
        return frozenset(S) in self.indep

    @classmethod
    def uniform(cls, r, n):
        return cls(n, [frozenset(c) for k in range(r + 1) for c in combinations(range(n), k)])

    @classmethod
    def from_bases(cls, n, bases):
        indep = set()
        for B in bases:
            for k in range(len(B) + 1):
                for c in combinations(B, k):
                    indep.add(frozenset(c))
        return cls(n, indep)


# ---------------- Basis & L^d entry generation ----------------

def basis_in_external_degree(M: Matroid, e: int):
    out = []
    for m in range(M.rank + 1):
        sT = m - e
        if sT < 0 or sT > M.rank:
            continue
        for S in M.by_size.get(m, []):
            for T in M.by_size.get(sT, []):
                out.append((S, T))
    return out


def Lpow_sparse_entries(M: Matroid, e: int, p: int, P: int):
    """Build sparse entries of L^p : S_e -> S_{e + 2p}.
    L^p (x_S \otimes y_T) = p! * sum_{X \subseteq T, |X|=p, S\cup X indep} x_{S \cup X} \otimes y_{T \setminus X}.
    Returns (rows, cols, vals, src_dim, tgt_dim).
    """
    src = basis_in_external_degree(M, e)
    tgt = basis_in_external_degree(M, e + 2 * p)
    tgt_idx = {st: i for i, st in enumerate(tgt)}

    rows_out, cols_out, vals_out = [], [], []
    factp = 1
    for k in range(1, p + 1):
        factp *= k
    factp %= P

    for j, (S, T) in enumerate(src):
        # iterate all p-subsets X of T (as set)
        T_list = list(T)
        for X_tup in combinations(T_list, p):
            X = frozenset(X_tup)
            if X & S:
                continue
            Snew = S | X
            if not M.is_indep(Snew):
                continue
            Tnew = T - X
            i = tgt_idx[(frozenset(Snew), frozenset(Tnew))]
            rows_out.append(i)
            cols_out.append(j)
            vals_out.append(factp)
    return (rows_out, cols_out, vals_out, len(src), len(tgt))


def L_sparse_entries(M, e, P):
    """L : S_e -> S_{e+2}.   Single-step L."""
    return Lpow_sparse_entries(M, e, 1, P)


# ---------------- GPU mod-p Gaussian elimination ----------------

def to_dense_gpu(rows, cols, vals, m, n, device, P):
    """Build a dense int64 mod-P matrix on GPU."""
    A = torch.zeros((m, n), dtype=torch.int64, device=device)
    if not rows:
        return A
    ri = torch.tensor(rows, dtype=torch.long, device=device)
    ci = torch.tensor(cols, dtype=torch.long, device=device)
    vi = torch.tensor(vals, dtype=torch.int64, device=device)
    A.index_put_((ri, ci), vi, accumulate=True)
    return A % P


def gpu_rank_modp(A, P):
    """In-place Gaussian elimination on int64 tensor A mod P. Returns rank."""
    A = A.contiguous()
    m, n = A.shape
    r = 0
    P_t = int(P)
    for c in range(n):
        if r >= m:
            break
        # find a row >= r with nonzero entry in col c
        col = A[r:, c]
        nz = (col % P_t).nonzero(as_tuple=False)
        if nz.numel() == 0:
            continue
        pivot_offset = int(nz[0].item())
        pivot_row = r + pivot_offset
        if pivot_row != r:
            tmp = A[r].clone()
            A[r] = A[pivot_row]
            A[pivot_row] = tmp
        # invert pivot
        inv = pow(int(A[r, c].item()) % P_t, P_t - 2, P_t)
        A[r] = (A[r] * inv) % P_t
        # eliminate other rows (skip r) — in parallel across rows
        factors = A[:, c].clone()
        factors[r] = 0
        # subtract factors[k] * A[r] from A[k] for k != r
        # A -= factors.unsqueeze(1) * A[r].unsqueeze(0)
        A -= factors.unsqueeze(1) * A[r].unsqueeze(0)
        A %= P_t
        r += 1
    return r


def rank_Lpow(M, e, p, device='cuda:0', P=10007, verbose=False):
    t0 = time.time()
    rows, cols, vals, src_dim, tgt_dim = Lpow_sparse_entries(M, e, p, P)
    t1 = time.time()
    if verbose:
        print(f"    build sparse: src={src_dim} tgt={tgt_dim} nnz={len(rows)}  {t1-t0:.1f}s", flush=True)
    A = to_dense_gpu(rows, cols, vals, tgt_dim, src_dim, device, P)
    t2 = time.time()
    if verbose:
        print(f"    to dense GPU: shape={tuple(A.shape)} memGB={A.element_size()*A.numel()/1e9:.2f}  {t2-t1:.1f}s", flush=True)
    r = gpu_rank_modp(A, P)
    del A
    torch.cuda.empty_cache()
    t3 = time.time()
    if verbose:
        print(f"    rank: {r}  {t3-t2:.1f}s", flush=True)
    return r, src_dim, tgt_dim


# ---------------- Reporting ----------------

def test_matroid(M, label, max_d=None, device='cuda:0', P=10007, only_d2=False):
    rk = M.rank
    if max_d is None:
        max_d = rk
    total_dim = sum(M.f)
    print(f"\n=== {label}  n={M.n} rank={rk} f={M.f} total_indep={total_dim} ===", flush=True)
    if only_d2:
        ds = [2] if 2 <= max_d else []
    else:
        ds = list(range(1, max_d + 1))
    for d in ds:
        e = -d
        # L : S_-d -> S_-d+2
        r1, ds1, dt1 = rank_Lpow(M, e, 1, device, P)
        print(f"  d={d}: L: {ds1}->{dt1} rank={r1}  "
              f"{'INJ' if r1==ds1 else f'ker={ds1-r1}'} "
              f"{'SURJ' if r1==dt1 else f'coker={dt1-r1}'}", flush=True)
        # L^d : S_-d -> S_d (hard Lefschetz)
        rp, dsp, dtp = rank_Lpow(M, e, d, device, P)
        iso = (rp == dsp == dtp)
        print(f"        L^{d}: {dsp}->{dtp} rank={rp} "
              f"{'ISO ✓' if iso else 'NOT-ISO ✗'}", flush=True)


# ---------------- Specific matroids ----------------

def M_Kn(n_verts):
    """Cycle matroid of K_n. Elements = edges. Bases = spanning trees."""
    edges = list(combinations(range(n_verts), 2))
    n = len(edges)

    def is_ST(B):
        if len(B) != n_verts - 1:
            return False
        p = list(range(n_verts))
        def f(x):
            while p[x] != x:
                p[x] = p[p[x]]
                x = p[x]
            return x
        for ei in B:
            u, v = edges[ei]
            ru, rv = f(u), f(v)
            if ru == rv:
                return False
            p[ru] = rv
        return True
    bases = [b for b in combinations(range(n), n_verts - 1) if is_ST(b)]
    return Matroid.from_bases(n, bases)


def AG_n_2(n_pow):
    """AG(n, 2) = affine space F_2^n.  Bases = affine independent (n+1)-tuples ...
    Actually for the matroid: ground set is F_2^n (2^n elements), rank n+1.
    A (k+1)-subset {p_0,...,p_k} is independent iff their differences span k-dim subspace
    iff p_0..p_k are affinely independent.
    Equivalently, a subset S is dependent iff some subset of size 4 (or smaller) is on an affine flat (which for F_2 means sum = 0 if we treat as vectors).
    For n_pow=3: AG(3,2) — 8 points, rank 4."""
    N = 1 << n_pow
    pts = list(range(N))
    rk = n_pow + 1
    # Bases: affinely independent (n+1)-subsets.
    def affinely_indep(B):
        # B = list of vectors in F_2^n. Affinely indep iff differences {p - p_0 : p in B \ {p_0}} are linearly indep.
        if len(B) != rk:
            return False
        p0 = B[0]
        diffs = [p ^ p0 for p in B[1:]]
        # Check rank n in F_2.
        mat = list(diffs)
        # Gaussian elimination over F_2
        r = 0
        bits = n_pow
        for c in range(bits):
            mask = 1 << c
            piv = -1
            for k in range(r, len(mat)):
                if mat[k] & mask:
                    piv = k; break
            if piv < 0:
                continue
            mat[r], mat[piv] = mat[piv], mat[r]
            for k in range(len(mat)):
                if k != r and (mat[k] & mask):
                    mat[k] ^= mat[r]
            r += 1
        return r == n_pow
    bases = [tuple(B) for B in combinations(pts, rk) if affinely_indep(list(B))]
    return Matroid.from_bases(N, bases)


def Vamos():
    CH = [frozenset(c) for c in [(0,1,2,3),(0,1,4,5),(2,3,4,5),(2,3,6,7),(4,5,6,7)]]
    bases = [b for b in combinations(range(8),4) if frozenset(b) not in CH]
    return Matroid.from_bases(8, bases)


if __name__ == "__main__":
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else "warmup"
    P = 10007
    device = 'cuda:0'

    if arg == "warmup":
        # Quick test to verify GPU + correctness on Fano (where ker(L,d=1)=21).
        from itertools import combinations
        lines = [frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
        bases = [b for b in combinations(range(7), 3) if frozenset(b) not in lines]
        M = Matroid.from_bases(7, bases)
        test_matroid(M, "Fano [warmup]", device=device, P=P)

    elif arg == "scaleup":
        # Uniform U_{r,n} for r=5..10 with increasing n
        targets = [
            ('U_{5,8}',  Matroid.uniform(5, 8)),
            ('U_{5,10}', Matroid.uniform(5, 10)),
            ('U_{6,10}', Matroid.uniform(6, 10)),
            ('U_{6,12}', Matroid.uniform(6, 12)),
            ('U_{7,11}', Matroid.uniform(7, 11)),
            ('U_{7,12}', Matroid.uniform(7, 12)),
            ('U_{8,12}', Matroid.uniform(8, 12)),
            ('U_{9,12}', Matroid.uniform(9, 12)),
            ('U_{10,11}', Matroid.uniform(10, 11)),
            ('U_{10,12}', Matroid.uniform(10, 12)),
        ]
        for label, M in targets:
            try:
                test_matroid(M, label, device=device, P=P, only_d2=True)
            except torch.cuda.OutOfMemoryError as e:
                print(f"  OOM on {label}: {e}", flush=True)
                torch.cuda.empty_cache()

    elif arg == "graphic":
        for k in [5, 6, 7]:
            try:
                test_matroid(M_Kn(k), f"M(K_{k})", device=device, P=P, only_d2=True)
            except torch.cuda.OutOfMemoryError as e:
                print(f"  OOM: {e}", flush=True)
                torch.cuda.empty_cache()

    elif arg == "agseries":
        for npow in [3, 4]:
            try:
                test_matroid(AG_n_2(npow), f"AG({npow},2)", device=device, P=P, only_d2=True)
            except torch.cuda.OutOfMemoryError as e:
                print(f"  OOM: {e}", flush=True)
                torch.cuda.empty_cache()

    elif arg == "vamos":
        test_matroid(Vamos(), "Vamos", device=device, P=P)
    else:
        print("usage: warmup | scaleup | graphic | agseries | vamos")
