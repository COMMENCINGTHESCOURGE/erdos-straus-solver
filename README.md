# erdos-straus-solver

[![Python Tests](https://github.com/GUINEA-PIG-TRENCH/erdos-straus-solver/actions/workflows/python-tests.yml/badge.svg)](https://github.com/GUINEA-PIG-TRENCH/erdos-straus-solver/actions/workflows/python-tests.yml)
[![Sieve Verification](https://github.com/GUINEA-PIG-TRENCH/erdos-straus-solver/actions/workflows/sieve-verify.yml/badge.svg)](https://github.com/GUINEA-PIG-TRENCH/erdos-straus-solver/actions/workflows/sieve-verify.yml)
[![OEIS Verification](https://github.com/GUINEA-PIG-TRENCH/erdos-straus-solver/actions/workflows/oeis-verify.yml/badge.svg)](https://github.com/GUINEA-PIG-TRENCH/erdos-straus-solver/actions/workflows/oeis-verify.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue)](./LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)

**Part of the MANIFOLD field computation system.**
**Lead R&D: DaShawn (Guinea Pig Trench LLC)**
**Copyright (c) 2026 Guinea Pig Trench LLC**

---

## What this project is

An **empirical, structural study of the Erdős–Straus conjecture in the
prime-square regime**, with deterministic sieving tooling and CI-enforced
verification.

The Erdős–Straus conjecture (1948): every integer `n ≥ 2` admits
`4/n = 1/x + 1/y + 1/z` with positive integers `x ≤ y ≤ z`. The conjecture
remains **unproven**. This repository does **not** claim a proof. Its purpose
is:

1. A deterministic, reproducible **hot-corridor sieve** for existence checks
   (`sieve_l40s_hot_corridor.py`), developed for distributed runs, with
   integer-only arithmetic and CI gates (`verify_sieve.py`).
2. A **structural classification** of the prime-square equation `4/p²` via the
   "additive shift" framework (`A`-values / 22-portal classification), with an
   OEIS-ready representative data file for the distribution of minimal
   `A` over exceptional primes.

Every discovered triple is re-verified in exact integer arithmetic, both
locally (`verify_sieve.py`) and in CI on every push.

---

## Position relative to the literature (be concrete)

Computational support for Erdős–Straus has a long record. This repository
needs to be read in that light:

| Bound reached | Year | Author(s) |
| --- | --- | --- |
| `10¹⁴` | 1999 | Allan D. Swett |
| `2×10¹⁴` | 2012 | Bello-Hernández, Benito, Fernández |
| `10¹⁷` | 2014 | Serge E. Salez (arXiv:1406.6307) |
| `10¹⁸` | 2025 | Mihnea & Dumitru (arXiv:2509.00128) |

The sieve's own existence runs (8×10¹³ on Kaggle) re-confirm a range already
covered since 1999 — they are **not** a verification record. The genuinely
distinct content here is the **`4/p²` portal classification to 8×10⁸
(tested primes ≤ 10⁸)**, i.e. a structural map of minimal `A`, not an
extension of the verified bound.

### The key distinction: `4/p²` vs `4/p`

- This repo classifies **`4/p²`** (prime squares). Any solution for `4/p`
  immediately yields one for `4/p²` by scaling denominators by `p`;
  the converse requires a descent step that is **not proved in this
  repository** (see [PROOF_SKETCH.md](PROOF_SKETCH.md), which states the
  remaining work explicitly).
- The conjecture is most challenge in the **prime case `4/p`**. Composite `n`
  reduce to primes by scaling. No result here claims progress on `4/p`.

---

## Claims (scoped)

| Claim | Scope | Status |
| --- | --- | --- |
| Corridor existence check | `n ≡ 0 (mod 24)`, hot corridor | `8×10¹³` on Kaggle, zero failures — **within already-verified territory** (CI re-checks to 10⁶ on every push) |
| `4/p²` solved for tested exceptional primes | `p ≤ 10⁸` (289,372 primes) | 100% — **range contained in the 10¹⁸ record**; novelty is the classification |
| 22-portal classification | `4/p²`, minimal `A` values | Empirically exhaustive to `p ≤ 10⁸`, `A ≤ 159` — **empirical, not proved** |
| `A=7` dominance ~49.5%, `A=159` (max) | same range | Stable across scales (empirical) |
| Comparison vs arXiv:2602.11774 (2026) | disjoint `(y,z)` sets | Structural comparison only; that preprint is itself in active review — no validity claim made either way |
| Relation to `4/p` | descent | **open — explicitly flagged as unproven (PROOF_SKETCH.md §7.2)** |

The 22 A-values: 7, 11, 15, 19, 23, 31, 39, 43, 47, 51, 59, 67, 71, 79, 83,
87, 95, 103, 107, 111, 127, 159.

**OEIS submission (empirical data):** prepared, as representative data, not as
a theorem —
- `oeis_a_values_data.txt` (distribution counts)
- `oeis_b_file.txt` (22 distinct `A`-values)
- `bfile_exceptional_1000.txt` (per-exceptional-prime `A`, first 1000)
- `gen_oeis_bfile.py` (b-file generator)

---

## How to verify

```bash
git clone https://github.com/GUINEA-PIG-TRENCH/erdos-straus-solver.git
cd erdos-straus-solver

# Corridor gate (fast, exact): asserts 100% coverage + exact arithmetic
python verify_sieve.py --limit 1000000

# Unit tests
python -m pytest tests/ -x -v
```

CI runs the same gate on every push:
- `Sieve Verification` — corridor coverage + exact triple arithmetic
  (Python 3.11 / 3.12)
- `Python Tests` — unit tests + dataset verification
- `OEIS Verification` — final-verify + OEIS A-value regression check

---

## Architecture

- `sieve_l40s_hot_corridor.py` — primary sieve runner, stride-24 corridor.
- `master_orchestrator.py` / `lightning_worker.py` — deterministic
  seed-based partitioning across nodes.
- `final_verify.py` / `delta_analysis.py` — verification and OEIS data tools.
- `endpoint pro`: notebooks for Kaggle/Colab GPU runs (see Deployment).

---

## Deployment

- **Kaggle (Scale Prover)**: `commencethescourge/erdos-straus-scale-prover`
  — Omega solver, 10⁹-range verification.
- **Kaggle (Hot Corridor)**: `commencethescourge/erdos-p100-hot-corridor-sieve`
  — P100 GPU, daily schedule.
- **Colab**: [erdos_colab_gpu_sieve.ipynb](erdos_colab_gpu_sieve.ipynb)
  — CuPy-accelerated hot corridor sieve.
- **Colab LLM Verifier**: [erdos_colab_llm_verifier.ipynb](erdos_colab_llm_verifier.ipynb).

---

## Entity

| Field | Value |
| --- | --- |
| Lead R&D | DaShawn (Guinea Pig Trench LLC) |
| Copyright | Guinea Pig Trench LLC |
| R&D Entity | Guinea Pig Trench LLC (PA, #13674084) |
| Credit Facility | Truth Holds Enterprise (PA #7049023) |