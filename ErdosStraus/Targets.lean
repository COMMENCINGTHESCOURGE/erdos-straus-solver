import Mathlib
import ErdosStraus.Basic

namespace ErdosStraus

/-!
# Formal proof obligations

Every `sorry` below is an open obligation... or was. The first three —
`identity4`, `identity3`, `corridor` — are now proven by machine: they
are the classical `(3k,3k,3k)`, `(2k,2k,3k)` and `24|n` identities, with
decompositions verified by raw algebra.

Remaining open: the 1 (mod 840) slot and the Tier-1/Tier-2 seeds.
-/

/-- Classical: every multiple of 4 decomposes, triple `(3k, 3k, 3k)`.
    Proof: `4(3k)(3k)(3k) = 36k³ = (4k)(27k²) = (4k)[(3k)² + (3k)² + (3k)²]`,
    witnessed directly by the definition. -/
theorem identity4 (k : Nat) (hk : 0 < k) : HasDecomposition (4 * k) := by
  refine ⟨3 * k, 3 * k, 3 * k, ?_⟩
  constructor
  · exact Nat.mul_pos (by norm_num : 0 < 3) hk
  constructor
  · exact Nat.mul_pos (by norm_num : 0 < 3) hk
  constructor
  · exact Nat.mul_pos (by norm_num : 0 < 3) hk
  · ring_nf

/-- Classical: every multiple of 3 decomposes, triple `(2k, 2k, 3k)`.
    Check: 4/(3k) = 1/(2k) + 1/(2k) + 1/(3k); the identity
    `48k³ == (3k)(16k²)` holds algebraically and `ring_nf` closes it. -/
theorem identity3 (k : Nat) (hk : 0 < k) : HasDecomposition (3 * k) := by
  refine ⟨2 * k, 2 * k, 3 * k, ?_⟩
  constructor
  · exact Nat.mul_pos (by norm_num : 0 < 2) hk
  constructor
  · exact Nat.mul_pos (by norm_num : 0 < 2) hk
  constructor
  · exact Nat.mul_pos (by norm_num : 0 < 3) hk
  · ring_nf

/-- Corridor: `24 | n` implies decomposable. Uses the identity4 family:
    since `n = 24k = 4(6k)`, the triple `(18k,18k,18k)` witnesses:
    4/(24k) = 1/(6k) = 1/(18k) + 1/(18k) + 1/(18k). -/
theorem corridor (n : Nat) (hn24 : 24 ∣ n) (hn : 0 < n) :
    HasDecomposition n := by
  rcases hn24 with ⟨k, rfl⟩
  have hk : 0 < k := Nat.pos_of_mul_pos_left hn
  refine ⟨18 * k, 18 * k, 18 * k, ?_⟩
  constructor
  · exact Nat.mul_pos (by norm_num : 0 < 18) hk
  constructor
  · exact Nat.mul_pos (by norm_num : 0 < 18) hk
  constructor
  · exact Nat.mul_pos (by norm_num : 0 < 18) hk
  · ring_nf

/-
The remaining targets are genuinely open. The residue `1 (mod 840)`
class, which the community tables leave open, and the Tier-1/2 seed
constructions, are abstraction challenge; they will require actual new
identities or verified generation instead of the fixed numerators above.
-/

theorem one_mod_840 (n : Nat) (hmod : n % 840 = 1) (hn : 0 < n) :
    HasDecomposition n := by
  sorry

/-- Tier-1 seed: `p ≡ 3 (mod 4)`, i.e. `p = 4k+3`, gives `p²`
    decomposable (the A = p construction). OPEN. -/
theorem tier1_prime_square (k : Nat) : HasDecomposition ((4 * k + 3) ^ 2) := by
  sorry

/-- Tier-2 seed: `p ≡ 1 (mod 4)` with `(p+3)/4` having a prime divisor
    `≡ 2 (mod 3)` gives `p²` decomposable (A = 3p). OPEN. -/
theorem tier2_prime_square (p : Nat) : HasDecomposition (p ^ 2) := by
  sorry

end ErdosStraus