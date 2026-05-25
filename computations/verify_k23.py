"""Verify the Aut-orbit Hall proof for M(K_{2,3}) computationally."""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations, permutations
from gpu_rank import Matroid


def K23():
    """K_{2,3}: parts {a=0, b=1} and {c=2, d=3, e=4}. 6 edges:
    edge 0: (a, c), 1: (a, d), 2: (a, e), 3: (b, c), 4: (b, d), 5: (b, e)."""
    edges = [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)]
    n = 6
    n_verts = 5
    # bases = spanning trees = 4-edge subsets forming a tree
    def is_tree(B):
        if len(B) != n_verts - 1: return False
        # Union-find
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
    bases = [b for b in combinations(range(n), n_verts-1) if is_tree(b)]
    return Matroid.from_bases(n, bases)


def X_k_set(N, k):
    E = frozenset(range(N.n))
    out = []
    for A in combinations(range(N.n), k):
        A = frozenset(A)
        if A not in N.indep: continue
        if (E - A) not in N.indep: continue
        out.append(A)
    return out


def main():
    M = K23()
    print(f"M(K_{{2,3}}): n={M.n}, rank={M.rank}, f-vector={M.f}")

    X2 = X_k_set(M, 2)
    X3 = X_k_set(M, 3)
    print(f"|X_2| = {len(X2)}")
    print(f"|X_3| = {len(X3)}")

    # Compute Aut(M(K_{2,3})) brute force
    aut = []
    for sigma in permutations(range(M.n)):
        ok = all(frozenset(sigma[i] for i in S) in M.indep for S in M.indep)
        if ok: aut.append(sigma)
    print(f"|Aut(M)| = {len(aut)}")

    # Compute orbits in X_2
    seen = set()
    orbits = []
    X2_set = set(X2)
    for A in X2:
        if A in seen: continue
        orbit = {A}
        frontier = [A]
        while frontier:
            curr = frontier.pop()
            for sigma in aut:
                B = frozenset(sigma[i] for i in curr)
                if B in X2_set and B not in orbit:
                    orbit.add(B); frontier.append(B)
        orbits.append(orbit)
        seen.update(orbit)

    print(f"\n# Aut-orbits in X_2: {len(orbits)}")
    print(f"Orbit sizes: {[len(o) for o in orbits]}")

    edges_label = ['(a,c)', '(a,d)', '(a,e)', '(b,c)', '(b,d)', '(b,e)']
    for i, orbit in enumerate(orbits):
        print(f"\nOrbit {i} (size {len(orbit)}):")
        for A in sorted(orbit, key=sorted):
            print(f"  {{{', '.join(edges_label[i] for i in sorted(A))}}}")

    # Compute N(orbit) for each
    X3_set = set(X3)
    adj = {}
    for A in X2:
        adj[A] = []
        for i in range(M.n):
            if i in A: continue
            Ap = A | frozenset([i])
            if Ap in X3_set:
                adj[A].append(Ap)

    for i, orbit in enumerate(orbits):
        nbhd = set()
        for A in orbit:
            nbhd.update(adj[A])
        print(f"\n|N(Orbit {i})| = {len(nbhd)}, |Orbit {i}| = {len(orbit)}, ratio = {len(nbhd)/len(orbit):.3f}")
        print(f"  Hall check: {'✓ (margin ' + str(len(nbhd) - len(orbit)) + ')' if len(nbhd) >= len(orbit) else '✗'}")


if __name__ == "__main__":
    main()
