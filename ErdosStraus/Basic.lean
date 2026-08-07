import Mathlib

namespace ErdosStraus

/-- A positive triple `(x, y, z)` is a decomposition for `n` in the
    Erdős-Straus equation. We avoid division by using the equivalent
    natural-number identity `4xyz = n(xz + xy + yz)`. -/
def IsDecomposition (n x y z : Nat) : Prop :=
  0 < x ∧ 0 < y ∧ 0 < z ∧ 4 * x * y * z = n * (x * y + x * z + y * z)

/-- `n` satisfies the Erdős-Straus property: some positive triple
    decomposes `4/n`. -/
def HasDecomposition (n : Nat) : Prop :=
  ∃ x y z : Nat, IsDecomposition n x y z

/-- The conjecture, stated formally. This is the widely open problem;
    the proof obligation is deliberately unfilled. -/
theorem erdosStrausConjecture : ∀ n : Nat, 2 ≤ n → HasDecomposition n := by
  sorry

/-- The conjecture restricted to primes; equivalent to the full one via
    compositeness reduction (unproved reduction, kept as a target). -/
theorem erdosStrausPrimeCase : ∀ p : Nat, Nat.Prime p → HasDecomposition p := by
  sorry

end ErdosStraus