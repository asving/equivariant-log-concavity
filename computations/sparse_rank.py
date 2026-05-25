"""
Sparse mod-p Gaussian elimination for big sparse matrices.

Approach: process columns left-to-right. Maintain rows as dicts {col->val}.
For each col c:
  - Find a row r (not yet pivoted) with nonzero entry in c.
  - Normalize the row (multiply by inv of pivot).
  - Eliminate: for every OTHER row r' with nonzero in c, do r' -= r'[c] * r.

This is O(rank * avg_fill * avg_row_size).  For our matrices the fill-in is moderate.

For column-pivoted GE we ALSO maintain col->rows index for fast lookup.
"""
from __future__ import annotations
from itertools import combinations
import sys, time
from collections import defaultdict
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from gpu_rank import Matroid, basis_in_external_degree, Lpow_sparse_entries


def sparse_rank_modp(rows, cols, vals, nrows, ncols, P, verbose=True):
    """Compute rank mod P. rows, cols, vals: triplet lists. Return rank."""
    if not rows:
        return 0
    # Build: row_data[r] = dict {c: v mod P}, col_index[c] = set of rows with c
    t0 = time.time()
    row_data = [dict() for _ in range(nrows)]
    for r, c, v in zip(rows, cols, vals):
        v = int(v) % P
        if v == 0: continue
        row_data[r][c] = (row_data[r].get(c, 0) + v) % P
    # remove zero entries
    for r in range(nrows):
        row_data[r] = {c: v for c, v in row_data[r].items() if v % P != 0}
    col_index = defaultdict(set)
    for r in range(nrows):
        for c in row_data[r]:
            col_index[c].add(r)
    t1 = time.time()
    if verbose: print(f"  sparse build: {t1-t0:.1f}s  rows={nrows} cols={ncols} nnz_init={sum(len(d) for d in row_data)}", flush=True)

    pivoted_rows = set()
    pivot_for_col = {}  # col -> row
    rank = 0
    Pp = int(P)

    last_print = time.time()
    for c in range(ncols):
        if c in pivot_for_col: continue
        cands = [r for r in col_index.get(c, ()) if r not in pivoted_rows]
        if not cands: continue
        # pick row with fewest entries (Markowitz pivoting)
        pivot_row = min(cands, key=lambda r: len(row_data[r]))
        pivoted_rows.add(pivot_row)
        pivot_for_col[c] = pivot_row
        # normalize
        pv = row_data[pivot_row][c]
        inv = pow(pv, Pp - 2, Pp)
        if inv != 1:
            new_d = {cc: (vv * inv) % Pp for cc, vv in row_data[pivot_row].items()}
            row_data[pivot_row] = new_d
        # eliminate from other rows containing c
        others = [r for r in col_index[c] if r != pivot_row]
        pivot_d = row_data[pivot_row]
        for r in others:
            factor = row_data[r].pop(c, 0)
            if factor == 0:
                col_index[c].discard(r)
                continue
            col_index[c].discard(r)
            # subtract factor * pivot_d from row_data[r]
            for cc, vv in pivot_d.items():
                if cc == c:  # already removed
                    continue
                new_v = (row_data[r].get(cc, 0) - factor * vv) % Pp
                if new_v == 0:
                    if cc in row_data[r]:
                        del row_data[r][cc]
                        col_index[cc].discard(r)
                else:
                    if cc not in row_data[r]:
                        col_index[cc].add(r)
                    row_data[r][cc] = new_v
        rank += 1
        # progress print every 5s
        now = time.time()
        if verbose and now - last_print > 5:
            tot_nnz = sum(len(d) for d in row_data)
            print(f"   col {c}/{ncols}  rank={rank} pivoted={len(pivoted_rows)} nnz={tot_nnz}  t={now-t0:.1f}s", flush=True)
            last_print = now
    t2 = time.time()
    if verbose: print(f"  sparse-GE done: rank={rank} total {t2-t0:.1f}s", flush=True)
    return rank


def test_inj(M, label, d):
    """Test if L : S_-d -> S_-d+2 is injective.  Returns (src, tgt, rank, INJ)."""
    P = 10007
    rows, cols, vals, src_dim, tgt_dim = Lpow_sparse_entries(M, -d, 1, P)
    print(f"\n{label}  d={d}:  L: S_-{d}({src_dim}) -> S_-{d-2}({tgt_dim})  nnz={len(rows)}", flush=True)
    r = sparse_rank_modp(rows, cols, vals, tgt_dim, src_dim, P)
    inj = (r == src_dim)
    print(f"  rank={r}  {'INJ ✓ (consistent with user-conjecture & ELC at d={})'.format(d) if inj else 'NOT INJ — kernel dim {} → ELC IMPLICATION FAILS HERE'.format(src_dim-r)}", flush=True)
    return src_dim, tgt_dim, r, inj


def M_Kn(n_verts):
    edges = list(combinations(range(n_verts), 2))
    n = len(edges)
    def is_ST(B):
        if len(B) != n_verts - 1: return False
        p = list(range(n_verts))
        def f(x):
            while p[x] != x: p[x] = p[p[x]]; x = p[x]
            return x
        for ei in B:
            u, v = edges[ei]
            ru, rv = f(u), f(v)
            if ru == rv: return False
            p[ru] = rv
        return True
    bases = [b for b in combinations(range(n), n_verts-1) if is_ST(b)]
    return Matroid.from_bases(n, bases)


if __name__ == "__main__":
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else "K5"
    if arg == "K5":
        # sanity: K_5 d=2 INJ already known
        M = M_Kn(5)
        test_inj(M, "M(K_5)", 2)
        test_inj(M, "M(K_5)", 3)
    elif arg == "K6":
        M = M_Kn(6)
        print(f"M(K_6): f = {M.f}", flush=True)
        test_inj(M, "M(K_6)", 2)
    elif arg == "K6_d3":
        M = M_Kn(6)
        print(f"M(K_6): f = {M.f}", flush=True)
        test_inj(M, "M(K_6)", 3)
    elif arg == "K7":
        M = M_Kn(7)
        print(f"M(K_7): f = {M.f}", flush=True)
        test_inj(M, "M(K_7)", 2)
    else:
        print("usage: K5 | K6 | K7")
