"""Test the empirical hypothesis: R(M)|_X = H*(compactified hyperplane arrangement
complement) for U(r, r+1) family matroids.

For U(r, r+1): n = r+1 elements, rank r. The matroid hyperplane arrangement
is (r+1) hyperplanes in general position in C^r. Complement U has
H*(U) = OS(M) = (1, ?, ?, ...).

Hypothesis: a specific compactification U ⊂ Ȳ adds a top class but kills the
constant class, so H*(Ȳ) = (drop OS deg 0, add 1 at top) = R(M)|_X graded.

The simplest such compactification is the ONE-POINT COMPACTIFICATION U^+ = U ⊔ {∞},
which has H̃*(U^+) = H̃*(U) but the reduced cohomology has the same structure.
A more useful compactification is a PROJECTIVE one.

For Triangle U(2,3): C² \ 3 lines. A natural compactification:
  • CP² \ 3 lines (= projective complement). Has different cohomology.
  • Blow-up of P² at the 3 intersection points and remove proper transforms of lines.
  • The wonderful compactification.

Let me compute and compare. The key test: does H* of some natural compactification of
the matroid hyperplane complement equal R(M)|_X graded for U(r, r+1)?

For Triangle U(2,3), R(M)|_X = (3, 3) at grades 1, 2.

CANDIDATE: blow up of P² at 3 points minus proper transforms of 3 lines.
The blow-up of P² at 3 points is a smooth proj surface S. Its cohomology:
  H^0(S) = Q, H^2(S) = Q^4 (= 1 from P² + 3 exceptional), H^4(S) = Q.

If we further remove a divisor D = proper transforms of 3 lines, we get an open S \ D
with cohomology described by Goresky-MacPherson.
"""

# This is a thought experiment with combinatorial checks. The full computation would
# require algebraic geometry software; here we just verify the Hilbert series
# prediction against the BLOW-UP cohomology computation we can do by hand.


def main():
    # Triangle: U(2, 3) representable as 3 lines in general position in C^2.
    # Hyperplane arrangement complement U = C^2 \ (3 lines).
    # H*(U) = OS(U(2,3)) = (1, 3, 2).  (Real cohomology degrees 0, 1, 2.)
    print("=" * 60)
    print("Triangle U(2,3): hyperplane arrangement = 3 lines in C^2")
    print("=" * 60)
    print(f"  H*(U) = OS = (1, 3, 2)  at real degrees 0, 1, 2")
    print(f"  R(M)|_X = (3, 3) at grades 1, 2")
    print()
    print("Hypothesis: R(M)|_X graded matches H*(Ȳ) for some compactification Ȳ.")
    print(f"  Drop deg 0 from OS, add 1 at top: (3, 2) → (3, 2) + 1@top = (3, 3) ✓")
    print()
    print("Candidate compactification Ȳ_Triangle:")
    print("  Blow-up of P^2 at the 3 intersection points of the 3 lines,")
    print("  then take the OPEN COMPLEMENT of the proper transforms of the 3 lines.")
    print("  This is a smooth open surface.")
    print()
    print("Let me compute its cohomology:")
    print()
    print("  Step 1: P^2 has H* = (1, 0, 1, 0, 1) — total dim 3, degrees 0, 2, 4.")
    print()
    print("  Step 2: Blow up P^2 at 3 points. Each blow-up adds 1 to H^2 (exceptional divisor).")
    print("           Result: H* = (1, 0, 4, 0, 1) — total dim 6, with H^2 = 4.")
    print()
    print("  Step 3: Remove proper transforms of 3 lines.")
    print("           Each line's proper transform is a (-1)-curve (since each line passes")
    print("           through 2 of the 3 blow-up points, lowering self-intersection by 2).")
    print("           Wait, in P^2, each line has self-intersection 1 (intersection with another line).")
    print("           After blowing up 2 points on a line, its self-intersection drops to 1-2 = -1.")
    print("           So proper transforms of the 3 lines are 3 disjoint (-1)-curves.")
    print()
    print("  Step 4: The open complement (blow-up minus proper transforms of 3 lines)")
    print("           Cohomology by Gysin:")
    print("           H^*(open) = H^*(blow-up) modded out by classes of the 3 removed divisors.")
    print("           H^* (blow-up) = (1, 0, 4, 0, 1).")
    print("           Remove 3 divisor classes from H^2 (codim 1, real codim 2, complex codim 1).")
    print("           Resulting H^2 = 4 - 3 = 1?")
    print()
    print("  Actual Gysin sequence: for X smooth proj and Z = smooth divisor (codim 1 = real codim 2),")
    print("  ... → H^{k-2}(Z) → H^k(X) → H^k(X \\ Z) → H^{k-1}(Z) → ...")
    print("  For Z = 3 disjoint divisors, H^*(Z) = 3 × H^*(point) = (3, 0, 3, ...) at degs 0, 2.")
    print("  ")
    print("  For k=2: H^0(Z)=3 → H^2(X)=4 → H^2(X\\Z) → H^1(Z)=0.")
    print("           The map H^0(Z) → H^2(X) is the Gysin pushforward = sending each [pt of Z]")
    print("           to the class [Z_i] of the corresponding divisor.")
    print("           If 3 disjoint (-1)-curves have linearly independent classes in H^2(X),")
    print("           map is injective. Then H^2(X\\Z) = 4 - 3 = 1.")
    print()
    print("  For k=4: H^2(Z)=3 → H^4(X)=1 → H^4(X\\Z) → H^3(Z)=0.")
    print("           H^2(Z) = top classes of 3 disjoint (-1)-curves. Each maps to its own [Z_i]·[pt]")
    print("           = -1 (self-intersection times point class) = some class in H^4(X) = Q.")
    print("           If non-zero, map is surjective with kernel of dim 2. Cokernel = 0.")
    print("           H^4(X\\Z) = 0.")
    print()
    print("  For k=3: H^1(Z)=0 → H^3(X)=0 → H^3(X\\Z) → H^2(Z)=3.")
    print("           H^3(X\\Z) = ker(H^2(Z) → H^4(X)).")
    print("           If map H^2(Z) → H^4(X) is surjective with kernel dim 2:")
    print("           H^3(X\\Z) = 2.")
    print()
    print("  Summary: H*(X \\ Z) = (1, 0, 1, 2, 0). Total dim 4. At real degrees 0, 1, 2, 3, 4.")
    print()
    print("  R(M)|_X = (3, 3) at grades 1, 2 (or doubled at degs 2, 4). Total 6.")
    print()
    print("  Open complement of (-1)-curves in blow-up has dim 4, NOT 6.")
    print("  So this is NOT the right compactification.")
    print()
    print("CONCLUSION:")
    print("  The simple compactification (blow-up minus proper transforms) doesn't")
    print("  give R(M)|_X graded. The 'drop deg 0, add 1 at top' transformation isn't")
    print("  realized by this geometric operation.")
    print()
    print("  The empirical (OS-no-deg-0) + (top) match is real but NOT realized by the")
    print("  most obvious compactification. Either:")
    print("  (a) The right compactification is more exotic.")
    print("  (b) The total-dim coincidence is misleading and there's no clean geometric story.")
    print("  (c) Some OTHER cohomology theory (intersection cohomology, twisted, etc.) gives R(M)|_X.")


if __name__ == "__main__":
    main()
