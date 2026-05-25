"""Test the Gui-Xiong-style dimension condition for INJ of L on R(M) ⊗ R^∨(M).

For Gui-Xiong's L on the ambient Λ(V) ⊗ Λ(V*), Hard Lefschetz gives L injective at
the relevant bigrades. On the matroid quotient R ⊗ R^∨ = (Λ/I_M) ⊗ (Λ*/I_M*), the
induced L has:
  ker(L_quot) = (L_amb)^{-1}(I_M^target) / I_M^source.

For L_quot injective: need (L_amb)^{-1}(I_M^target) ⊆ I_M^source.

Necessary dim condition: dim((L_amb)^{-1}(I_M^target)) ≤ dim(I_M^source).

Since L_amb is injective at our bigrade (by GX HL), image of L_amb has dim = dim source.
So:
  dim((L_amb)^{-1}(I_M^target)) = dim(I_M^target ∩ image(L_amb))
  ∈ [max(0, dim(I_M^target) + dim(image) - dim(target)), min(dim(I_M^target), dim(image))].

Compute this for our test matroids and see how tight things are.
"""
import sys
sys.path.insert(0, '/workspace-vast/asving/qlc/computations')
from itertools import combinations
from math import comb
from sparse_rank import M_Kn
from gpu_rank import Matroid, Vamos


def make_NC_U(M, C, U):
    UC = U - C
    UC_list = sorted(UC)
    idx = {e: i for i, e in enumerate(UC_list)}
    n_new = len(UC_list)
    indep = []
    for k_ in range(n_new + 1):
        for A in combinations(UC_list, k_):
            if (frozenset(A) | C) in M.indep:
                indep.append(frozenset(idx[e] for e in A))
    return Matroid(n_new, indep)


def analyze_gx_dimensions(N, label, k, d):
    """For matroid N at bigrade (m=k, -d), compute Gui-Xiong dimension data."""
    n = N.n
    f = N.f
    m = k
    if m + d >= len(f) or m + 1 >= len(f) or m + d - 1 >= len(f):
        print(f"  {label}: f-vector too short for ({k},{d}), skip")
        return
    fm = f[m]; fmd = f[m+d]; fm1 = f[m+1]; fmd1 = f[m+d-1]

    # Ambient dimensions (Λ ⊗ Λ*)
    amb_src = comb(n, m) * comb(n, m+d)
    amb_tgt = comb(n, m+1) * comb(n, m+d-1)

    # Matroid (R ⊗ R*) dimensions
    mat_src = fm * fmd
    mat_tgt = fm1 * fmd1

    # Ideal dimensions
    ideal_src = amb_src - mat_src
    ideal_tgt = amb_tgt - mat_tgt

    # By Gui-Xiong: L_amb injective if amb_src ≤ amb_tgt (= below middle)
    # Image of L_amb has dim = amb_src.
    img_dim = amb_src

    # dim((L_amb)^{-1}(I_M^target)) = dim(I_M^target ∩ image)
    # Bounds: max(0, ideal_tgt + img_dim - amb_tgt) ≤ dim ≤ min(ideal_tgt, img_dim).
    lower = max(0, ideal_tgt + img_dim - amb_tgt)
    upper = min(ideal_tgt, img_dim)

    # For L_quot inj: need dim((L_amb)^{-1}(I_M^target)) ≤ ideal_src.
    print(f"\n  {label} at (m={m}, d={d}):")
    print(f"    f = {f}")
    print(f"    Ambient: src={amb_src}, tgt={amb_tgt}, L_amb iso? {amb_src == amb_tgt}, L_amb INJ below middle? {amb_src <= amb_tgt}")
    print(f"    Matroid: src={mat_src}, tgt={mat_tgt}")
    print(f"    Ideal:   src={ideal_src}, tgt={ideal_tgt}")
    print(f"    dim((L_amb)^{{-1}}(I_M^tgt)) ∈ [{lower}, {upper}]")
    print(f"    Need ≤ ideal_src = {ideal_src} for INJ")
    if upper <= ideal_src:
        print(f"    ✓ Dim bound SUFFICIENT for INJ (upper {upper} ≤ {ideal_src})")
    elif lower > ideal_src:
        print(f"    ✗ Dim bound REFUTES INJ (lower {lower} > {ideal_src})")
    else:
        print(f"    ? Dim bound INCONCLUSIVE — depends on specific structure")


def main():
    print("="*70)
    print("Gui-Xiong dimension analysis for L on R(M) ⊗ R^∨(M)")
    print("="*70)

    # Paving cases — should give inj
    print("\n--- PAVING (known INJ) ---")
    # U_{5,8}
    analyze_gx_dimensions(Matroid.uniform(5, 8), "U_{5,8}", 3, 2)
    # U_{5,8} + 1 CH
    indep = []
    F = frozenset({0,1,2,3,4})
    for k_ in range(6):
        for S in combinations(range(8), k_):
            S = frozenset(S)
            if k_ == 5 and S == F: continue
            indep.append(S)
    M_one_ch = Matroid(8, indep)
    analyze_gx_dimensions(M_one_ch, "U_{5,8} + 1 CH", 3, 2)

    # Non-paving cases
    print("\n--- NON-PAVING (empirically INJ, proof open) ---")
    M6 = M_Kn(6)
    N1 = make_NC_U(M6, frozenset(), frozenset(range(8)))
    analyze_gx_dimensions(N1, "N1 = M(K_6)|_{0..7}", 3, 2)
    N2 = make_NC_U(M6, frozenset(), frozenset(list(range(7)) + [9]))
    analyze_gx_dimensions(N2, "N2 = M(K_6)|_{0..6,9}", 3, 2)


if __name__ == "__main__":
    main()
