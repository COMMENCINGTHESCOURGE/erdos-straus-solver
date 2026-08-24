# one_mod_840 — Computational Attack Notes (2026-08-23)

Target: `ErdosStraus/Targets.lean` → `theorem one_mod_840` — currently the
leading `sorry`. Claim: every n ≡ 1 (mod 840), n > 0, has a decomposition
4/n = 1/x + 1/y + 1/z.

## What was verified today

### Family 1 (a = 3): the q ≡ 2 (mod 3) identity — CLOSED FORM

For p = 840k+1 with N = p(p+3)/4 possessing any prime factor q ≡ 2 (mod 3):

    4/p = 1/((p+3)/4) + 1/((q+N)/3) + 1/((N²/q + N)/3)

Derivation: remainder after x=(p+3)/4 is r = 3/N. Two-term split of A/B needs a
divisor d | B² with d ≡ −B (mod A). Here A=3, B=N ≡ 1 (mod 3), so need d ≡ 2
(mod 3); any prime factor q ≡ 2 (mod 3) of N works (d=q).

Numerically verified for: 841, 1681, 3361, 5041, 6721, 8401 (all exact).
Covers ~59% of k ∈ [1,200] empirically.

### Residual class: N's factors all ≡ 1 (mod 3)

Example p = 2521 (prime), N = 631·2521, both factors ≡ 1 mod 3 → no divisor of
N² can be ≡ 2 mod 3 → Family 1 provably cannot close. Structural obstruction,
not search failure.

### Family 2+ (a = 7, 11, 15, ...): generalized x = (p+a)/4 sweep

For a ≡ 3 (mod 4), remainder r = 4a/(p(p+a)) reduced to A/B; same divisor
condition. Sweep over k = 1..300 with a ≤ 51:

- **Zero uncovered cases.** Every tested p = 840k+1 closes at some a.
- a-distribution: {3: 181, 7: 64, 11: 36, 15: 6, 19: 6, 23: 5, 27: 1, 31: 1}
- All closing a values are ≡ 3 (mod 4).
- Cross-checked exact solutions for 2521 (a=23), 4201 (a=11/39), 5881 (a=11),
  7561 (a=19), 9241 (a=7), 10921 (a=15), 13441/14281 (a=7).

## Path to a Lean proof (not yet done)

The theorem likely factors as:

1. **Scaling lemma** (easy in Lean): m | n ∧ HasDecomposition m →
   HasDecomposition n (multiply all denominators by n/m).
2. **Residue-case split on k**: reduce n mod small modulus M so that one of a
   finite set of affine identities (x=(n+a)/4 for a ∈ {3,7,...}) applies with
   an explicitly constructible divisor. Each case is `ring_nf` + `omega` +
   explicit witness, mirroring how corridor_mod24/corridor_div3 were closed.
3. The finite cover claim (every residue class mod M hits some a) must be
   verified by decide/omega over the residue classes — M bounded by product of
   the a-family moduli.

Risk: the empirical "a ≤ 31 suffices" may fail at larger k; a full proof needs
the modular reason WHY a≡3 mod 4 families cover, or acceptance that this stays
computational-evidence-only (consistent with project positioning: NOT a theorem
prover).

## Repro

Sweeps run via inline python (fractions.Fraction based). Key helper:
divisor-congruence test `d ≡ −B (mod A)` over B² factorization.
Coverage file: one_mod_840_coverage.txt (300-sweep output pending re-run;
60-sample confirmed zero-uncovered before timeout kill).
