# ErdosStraus — Lean 4 formalization

Formal layer (Lean 4 + mathlib) for the Erdős–Straus conjecture,
complementing the Python/harness verification in this repo.

**Status: scaffold only.** Definitions are in place; every theorem is a
`sorry`-marked open obligation. Nothing is claimed proved.

## Layout

- `ErdosStraus/Basic.lean` — definitions: `IsDecomposition` (positive
  triple with `4xyz = n(xy + xz + yz)`), `HasDecomposition`, and the two
  conjecture statements (all `n`, primes). Statements, not proofs.
- `ErdosStraus/Targets.lean` — the open proof obligations:
  - `identity4` — every multiple of 4 decomposes
  - `identity3` — every multiple of 3 decomposes
  - `corridor` — `24 | n` (the corridor class)
  - `one_mod_840` — the open `1 (mod 840)` class, per the repository's
    position this is the slot to formalize
  - `tier1_prime_square` / `tier2_prime_square` — the seed families
    (A = p for p ≡ 3 mod 4; A = 3p for the Tier-2 family) that may feed
    the 1 (mod 840) construction

## Toolchain

- `lean-toolchain`: `leanprover/lean4:v4.28.0`
- `lakefile.lean`: requires `mathlib` v4.28.0
- CI: `.github/workflows/lean.yml` runs `lake build` + lint via
  `leanprover/lean-action` on push / PR

## Build

```bash
lake build
lake lint                    # lints doc-string conventions
```

Note: first build downloads and compiles mathlib (heavy; CI makes it
cache-friendly via lean-action).

## Honesty boundary

Filling any `sorry` = a theorem. The sieve results are empirical; this
layer is where they must earn their axioms-free status. The genuinely
open point of contact with the literature is the 1 (mod 840) class —
nobody has closed that with an elementary construction; that is the
goal of the Tier-1/Tier-2 seeds in `Targets.lean`.

(c) 2026 Guinea Pig Trench LLC. MIT.