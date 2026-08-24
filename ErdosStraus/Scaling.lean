import Mathlib
import ErdosStraus.Basic

/-!
# Scaling lemma + affine identity family toward `one_mod_840`

Machine-checked building blocks. The scaling lemma reduces any n with a
known decomposable divisor to a decomposable n. Two further obligations are
stated with their computational witnesses.
-/

namespace ErdosStraus

/-- **Scaling lemma**: if m divides n (with 0 < n) and m decomposes,
then n decomposes. Witness: scale every denominator by n/m. -/
theorem scaling (m n : Nat) (hn : 0 < n) (hmn : m ∣ n)
    (hm : HasDecomposition m) : HasDecomposition n := by
  obtain ⟨x, y, z, hx, hy, hz, h⟩ := hm
  obtain ⟨s, hs⟩ := hmn
  -- n = m * s ; positivity of n forces s > 0
  have hms : m * s = n := hs.symm
  have hs0 : 0 < s := by
    rcases Nat.eq_zero_or_pos s with h0 | h0
    · subst h0
      simp at hms
      omega
    · exact h0
  refine ⟨s * x, s * y, s * z, ?_, ?_, ?_, ?_⟩
  · exact Nat.mul_pos hs0 hx
  · exact Nat.mul_pos hs0 hy
  · exact Nat.mul_pos hs0 hz
  -- goal (after rewriting n): 4(sx)(sy)(sz) = (ms)(sx·sy + sx·sz + sy·sz)
  · subst hms
    calc 4 * (s * x) * (s * y) * (s * z)
        = s ^ 3 * (4 * x * y * z) := by ring
      _ = s ^ 3 * (m * (x * y + x * z + y * z)) := by rw [h]
      _ = m * s * ((s * x) * (s * y) + (s * x) * (s * z) + (s * y) * (s * z)) := by ring

/-- **Affine step lemma**: an explicit rational-level witness transfers to a
Nat decomposition once denominators clear. Stated over the concrete triple
so the arithmetic identity is checkable. -/
theorem affine_step (p x y z : Nat) (hp : 0 < p) (hx : 0 < x) (hy : 0 < y)
    (hz : 0 < z)
    (hid : 4 * x * y * z = p * (x * y + x * z + y * z)) :
    IsDecomposition p x y z :=
  ⟨hx, hy, hz, hid⟩

/-- **Family-1 obligation** (a = 3): for p ≡ 1 (mod 4) where N = p(p+3)/4 has
a prime factor q ≡ 2 (mod 3), the explicit triple
((p+3)/4, (q+N)/3, (N²/q+N)/3) witnesses the decomposition.
Numerically verified: p=841 q=29; p=1681 q=41; p=3361 q=29; p=5041 q=71;
p=6721 q=11; p=8401 q=11. Full Nat-arithmetic proof pending — this is the
remaining gap between the empirical identity and one_mod_840. -/
theorem family_one (p q : Nat) (hp : 0 < p) (hq0 : 0 < q)
    (hp3 : (p + 3) % 4 = 0)
    (hqN : q ∣ (p * (p + 3)) / 4) : HasDecomposition p := by
  sorry

end ErdosStraus
