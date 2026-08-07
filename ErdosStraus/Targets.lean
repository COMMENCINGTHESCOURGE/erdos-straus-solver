import Mathlib
import ErdosStraus.Basic

namespace ErdosStraus

/-!
# Formal proof obligations

Every `sorry` below is an open obligation; filling one is a real theorem.
The comments state the classical results expected and the known gap.
-/

/-- Classical: every multiple of 4 decomposes, triple `(3k, 3k, 3k)`. -/
theorem identity4 (k : Nat) (hk : 0 < k) : HasDecomposition (4 * k) := by
  sorry

/-- Classical: every multiple of 3 decomposes, triple `(2k, 2k, 3k)`. -/
theorem identity3 (k : Nat) (hk : 0 < k) : HasDecomposition (3 * k) := by
  sorry

/-- Corridor: `24 | n` implies decomposable, via `identity4`. -/
theorem corridor (n : Nat) (hn24 : 24 ∣ n) (hn : 0 < n) :
    HasDecomposition n := by
  sorry

/-!
The open slot targeted by this project: the residue class
`1 (mod 840)`, the one class that classical identities do not close and
that the community status tables (see CONJECTURE.md in the repo) leave
open. The statement is deliberately `sorry`; proving it end-to-end is the
project's goal, and the Tier-1/Tier-2 families below are the seed
candidates.
-/

theorem one_mod_840 (n : Nat) (hmod : n % 840 = 1) (hn : 0 < n) :
    HasDecomposition n := by
  sorry

/-- Tier-1 seed: `p ≡ 3 (mod 4)` implies `p²` decomposes (A = p in the
    repo's construction). -/
theorem tier1_prime_square (k : Nat) : HasDecomposition ((4 * k + 3) ^ 2) := by
  sorry

/-- Tier-2 seed: `p ≡ 1 (mod 4)` with `(p+3)/4` having a prime divisor
    `≡ 2 (mod 3)` gives `p²` decomposable (A = 3p). -/
theorem tier2_prime_square (p : Nat) : HasDecomposition (p ^ 2) := by
  sorry

end ErdosStraus