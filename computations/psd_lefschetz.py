"""Test L_Q = sum_{i,j} q_{ij} x_i \otimes x_j for various Q (positive-semidefinite)."""
from __future__ import annotations
from itertools import combinations
import numpy as np
import random

P = 10007

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
    def is_indep(self, S): return frozenset(S) in self.indep
    @classmethod
    def from_bases(cls, n, bases):
        indep = set()
        for B in bases:
            for k in range(len(B)+1):
                for c in combinations(B, k): indep.add(frozenset(c))
        return cls(n, indep)

def M_K4():
    edges = {0:(1,2),1:(1,3),2:(1,4),3:(2,3),4:(2,4),5:(3,4)}
    def is_ST(B):
        if len(B)!=3: return False
        p={v:v for v in range(1,5)}
        def f(x):
            while p[x]!=x: p[x]=p[p[x]]; x=p[x]
            return x
        for e in B:
            u,v=edges[e]; ru,rv=f(u),f(v)
            if ru==rv: return False
            p[ru]=rv
        return True
    return Matroid.from_bases(6, [b for b in combinations(range(6),3) if is_ST(b)])

def Fano():
    lines = [frozenset(l) for l in [(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]]
    return Matroid.from_bases(7, [b for b in combinations(range(7),3) if frozenset(b) not in lines])

def basis_in_external_degree(M, e):
    out = []
    for m in range(M.rank+1):
        sT = m - e
        if sT < 0 or sT > M.rank: continue
        for S in M.by_size.get(m, []):
            for T in M.by_size.get(sT, []):
                out.append((S, T))
    return out

def LQ_matrix(M, e, Q):
    """L_Q = sum_{i,j} Q[i,j] x_i \otimes x_j on S; on x_S \otimes y_T,
    L_Q(x_S \otimes y_T) = sum_{i not in S, S+i indep} sum_{j in T} Q[i,j] x_{S+i} \otimes y_{T\j}.
    """
    src = basis_in_external_degree(M, e)
    tgt = basis_in_external_degree(M, e+2)
    tgt_idx = {st: i for i, st in enumerate(tgt)}
    A = np.zeros((len(tgt), len(src)), dtype=np.int64)
    n = M.n
    for col, (S, T) in enumerate(src):
        for i in range(n):
            if i in S: continue
            Snew = S | {i}
            if not M.is_indep(Snew): continue
            for j in T:
                qij = int(Q[i, j]) % P
                if qij == 0: continue
                Tnew = T - {j}
                row = tgt_idx[(frozenset(Snew), frozenset(Tnew))]
                A[row, col] = (A[row, col] + qij) % P
    return A

def modp_rank(A):
    A = A.copy()
    rows, cols = A.shape
    r = 0
    for c in range(cols):
        if r >= rows: break
        pivot = -1
        for k in range(r, rows):
            if A[k, c] % P != 0: pivot = k; break
        if pivot < 0: continue
        if pivot != r: A[[r,pivot]] = A[[pivot,r]]
        inv = pow(int(A[r,c]) % P, P-2, P)
        A[r] = (A[r] * inv) % P
        for k in range(rows):
            if k == r: continue
            if A[k,c] % P != 0:
                A[k] = (A[k] - A[k,c] * A[r]) % P
        r += 1
    return r

def matmul_modp(A, B):
    return np.dot(A, B) % P

def check_LQ(M, Q, label, max_d=None):
    rk = M.rank
    if max_d is None: max_d = rk
    print(f"  {label}:")
    for d in range(2, max_d + 1):
        A = LQ_matrix(M, -d, Q)
        for k in range(1, d):
            B = LQ_matrix(M, -d + 2*k, Q)
            A = matmul_modp(B, A)
        r = modp_rank(A.copy())
        iso = r == A.shape[0] == A.shape[1]
        print(f"    L^{d}: {A.shape[1]}->{A.shape[0]} rank={r} {'ISO' if iso else 'NOT-ISO'}")

if __name__ == "__main__":
    rng = random.Random(2026)
    for fn, name in [(M_K4, "M(K_4)"), (Fano, "Fano")]:
        M = fn()
        n = M.n
        print(f"\n=== {name} (n={n}) ===")
        # 1. diagonal identity
        check_LQ(M, np.eye(n, dtype=np.int64), "Q = I (diagonal)")
        # 2. random PSD with rank n (Q = M^T M with M random invertible)
        for trial in range(2):
            Mat = np.array([[rng.randint(1, 20) for _ in range(n)] for _ in range(n)], dtype=np.int64)
            Q = (Mat.T @ Mat) % P
            check_LQ(M, Q, f"Q = M^T M rank-{n} (trial {trial})")
        # 3. PSD rank 2: Q = u u^T + v v^T
        for trial in range(2):
            u = np.array([rng.randint(1, 20) for _ in range(n)], dtype=np.int64)
            v = np.array([rng.randint(1, 20) for _ in range(n)], dtype=np.int64)
            Q = (np.outer(u, u) + np.outer(v, v)) % P
            check_LQ(M, Q, f"Q = uu^T + vv^T (rank 2, trial {trial})")
        # 4. rank 1: Q = u u^T
        u = np.array([rng.randint(1, 20) for _ in range(n)], dtype=np.int64)
        Q = np.outer(u, u) % P
        check_LQ(M, Q, f"Q = uu^T (rank 1)")
        # 5. rank n positive but NOT diagonal: random sym matrix that happens to be PSD-like
        Mat = np.array([[rng.randint(1, 20) for _ in range(n)] for _ in range(n)], dtype=np.int64)
        Q = (Mat + Mat.T) % P
        check_LQ(M, Q, f"Q = M + M^T (symmetric but not nec. PSD)")
