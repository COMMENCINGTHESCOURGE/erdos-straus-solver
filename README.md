# erdos-straus-solver

[![Python Tests](https://github.com/GUINEA-PIG-TRENCH/erdos-straus-solver/actions/workflows/python-tests.yml/badge.svg)](https://github.com/GUINEA-PIG-TRENCH/erdos-straus-solver/actions/workflows/python-tests.yml)
[![Sieve Verification](https://github.com/GUINEA-PIG-TRENCH/erdos-straus-solver/actions/workflows/sieve-verify.yml/badge.svg)](https://github.com/GUINEA-PIG-TRENCH/erdos-straus-solver/actions/workflows/sieve-verify.yml)
[![OEIS Verification](https://github.com/GUINEA-PIG-TRENCH/erdos-straus-solver/actions/workflows/oeis-verify.yml/badge.svg)](https://github.com/GUINEA-PIG-TRENCH/erdos-straus-solver/actions/workflows/oeis-verify.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](./LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)

**Part of the MANIFOLD field computation system.**
**Lead R&D: DaShawn (African American Developer & Mathematician)**
**Copyright (c) 2026 Guinea Pig Trench LLC**

---

Erdos-Straus hot corridor sieve â€” integer solver, stride-24, 100% hit rate in mod-24 corridors (expected: these corridors are pre-filtered to numbers where parametric identities apply).

The Erdos-Straus conjecture states that for every integer n â‰¥ 2, the fraction 4/n can be expressed as the sum of three unit fractions (Egyptian fractions). This solver partitions the search space deterministically using a seed + survivor list, achieving zero-conflict parallel distribution across compute nodes.

This is the vinculum operating on integers instead of fields â€” same algebraic skeleton, different substrate.

---

## ðŸ† Key Results (Verified July 2026)

| Claim | Status |
| --- | --- |
| **Sieve existence check** | **Computational run through ~8.00e13 (80 trillion) on Kaggle; zero survivors. Literature has reached 1e17-1e18 for plain existence checks. The novel contribution is the 22-portal classification at 1e8 -- see EMPIRICAL_NOTE.md.** |
| All tested exceptional-prime-indexed prime squares ($p^2$) solved | **289,372/289,372 up to 10â¸ (100%). Note: solutions are for $4/p^2$, not $4/p$. A descent theorem is required to extend to $4/p$.** |
| 22-portal classification covers all tested $p^2$ | **22 A-values, max A=159** |
| Zero failures at any scale | <!-- ZERO_FAILURES_START --> **10â¶: 4540/4540, 10â·: 35750/35750, 10â¸: 289372/289372** <!-- ZERO_FAILURES_END --> |
| Mean minimal m = 2.25 | Tightly bounded |
| A=7 dominates at ~49.5% | Stable fraction across all scales |
| A=159 (m=39) at p=91,267,201 | Max observed, consistent with O(log p) growth |
| No overlap with Bradford (arXiv 2602.11774) solutions | 0.0% (y,z) agreement on shared n |
| Squareful barrier: Bradford fails on ALL squareful n | Structural, not implementation artifact |
| Xu (May 2026): 9 wild primes for mâ‰¤30,000 | **All 9 fall within 12-portal classification (for $4/p^2$)** |

**The 22 A-values (the "12 portals" plus higher terms):** 7, 11, 15, 19, 23, 31, 39, 43, 47, 51, 59, 67, 71, 79, 83, 87, 95, 103, 107, 111, 127, 159

**OEIS Submission:** Prepared â€” ready for submission to oeis.org/Submit

- Data file: `oeis_a_values_data.txt` (distribution counts)
- b-file: `oeis_b_file.txt` (22 distinct A-values)
- b-file: `bfile_exceptional_1000.txt` (A per exceptional prime, first 1000)
- Generator: `gen_oeis_bfile.py` (produces b-file for N exceptional primes)

## State of the Art & AI Baseline (2026)

This project is explicitly anchored against the 2026 AI mathematics wave. While autonomous reasoning models (e.g., GPT-5.2 paired with Lean/Aristotle) have successfully cleared hundreds of "long-tail" or neglected ErdÅ‘s problems, they structurally fail at frontier, open-ended research.

Because the ErdÅ‘s-Straus conjecture is a frontier problem, it breaks zero-shot AI provers. Therefore, this repository uses a **hybrid architecture**: AI models provide the theoretical scaffolding and write the hyper-optimized C/Python sieves, while deterministic GPU clusters (like Kaggle P100s) map the prime geometry. This repository provides the **empirical geometric blueprint** and vital theoretical scaffolding for the $4/p^2$ domain, strictly separated from the analytic **descent theorem** required to fully bridge solutions to $4/p$.

## Architecture

### The Hot Corridor Sieve

The sieve partitions work deterministically: same seed + same survivor list = same partition. This is **parallel transport** of number theory problems across compute nodes â€” the manifold geometry of the solution space.

- **Stride-24**: exploits the mod-24 structure of known solution corridors
- **Mod9 classification**: STABLE (1,4,7), BREACH (0,3,6), NEUTRAL (2,5,8)
- **Seeded partitioning**: any node with the same seed produces identical work boundaries

### Components

| File | Purpose |
| --- | --- |
| `sieve_l40s_hot_corridor.py` | Primary sieve runner â€” stride-24, hot corridor targeting |
| `master_orchestrator.py` | Coordinates multi-node distribution using sieve-based partitioning |
| `lightning_worker.py` | Remote compute worker for distributed runs |
| `progression.py` | Tracks solution discovery rate and corridor coverage |
| `deepseek_verifier.py` | Parallel verification against DeepSeek reasoning |
| `atomic_writer.py` | Thread-safe checkpoint writer for long-running sieves |
| `sieve_a100.py` / `sieve_a100_classify.py` | A100-optimized sieve + mod9 classification |

## Quick Start

```bash
git clone https://github.com/GUINEA-PIG-TRENCH/erdos-straus-solver.git
cd erdos-straus-solver
python sieve_l40s_hot_corridor.py --v 2 --stride 24 --depth 200
```

For distributed runs:

```bash
# Orchestrator node
python master_orchestrator.py --seed 42 --nodes 3

# Worker nodes
python lightning_worker.py --orchestrator <ip>:<port>
```

## Verification

The solver includes a self-verification mode that validates every discovered solution satisfies the 4/n = 1/a + 1/b + 1/c equation. The DeepSeek verifier cross-checks results against an independent reasoning path.

## The Vinculum Connection

Every measurement in this system is a vinculum:

| Ratio | What it measures |
| --- | --- |
| solutions / search space | Discovery progress |
| stride width / n | Corridor efficiency |
| verified / total | Solution quality |
| nodes with seed / total nodes | Partition completeness |

Same vinculum operator, applied to integers instead of GPU fields.

## Deployment

- **Kaggle (Scale Prover)**: `commencethescourge/erdos-straus-scale-prover` â€” Numba-JIT accelerated Omega solver for 10â¹ range verification
- **Kaggle (Hot Corridor)**: `commencethescourge/erdos-p100-hot-corridor-sieve` â€” P100 GPU, daily schedule
- **Colab**: [erdos_colab_gpu_sieve.ipynb](erdos_colab_gpu_sieve.ipynb) â€” CuPy-accelerated hot corridor sieve for T4/L4/A100 GPU runtimes with Google Drive auto-resume support.
- **Colab LLM Verifier**: [erdos_colab_llm_verifier.ipynb](erdos_colab_llm_verifier.ipynb) â€” Verification and math resonance analysis utilizing Google Gemini API keys to cross-check solutions and compile markdown reports.
- **Local**: Bare-metal runs with configurable thread count

## Entity

| Field | Value |
| --- | --- |
| Lead R&D | DaShawn (African American Developer & Mathematician) |
| Copyright | Guinea Pig Trench LLC |
| R&D Entity | Guinea Pig Trench LLC (PA, #13674084) |
| Credit Facility | Truth Holds Enterprise (PA #7049023) |
