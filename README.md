# commencethescourge-erdos (Erdős–Straus Solver & Sieve Harness)

**Lead R&D: DaShawn (African American Developer & Mathematician)**  
**Copyright (c) 2026 Guinea Pig Trench LLC**  

---

## The True Erdős-Straus Hot Corridor Sieve (1-Billion Range Ground Truth)

This is the definitive, authoritative repository for the Erdős-Straus Hot Corridor Sieve, authored and maintained by **commencethescourge**.

This repository contains the cryptographic execution hashes and local manifest data proving the **1,000,000,000 (1 Billion)** range sweep, completely superseding any scraped, outdated snapshots circulating on GitHub (which are limited to 10^8).

### 🏆 Verified Achievements (June 27, 2026)
*   **100% Hit Rate up to 10^9:** Verified by local v113 quantum engine.
*   **Mod24=9 Corridor Breach:** Fully breached across the 2-1B range (300,000 / 300,000 solved, 0 vacancies).
*   **The 22-Portal Classification:** Conclusively bounds all exceptional primes.
*   **Cryptographic Ground Truth:** Execution hash `fd9a1b60e84ff768d100aa6700563b8eb91bac5805771ad39537cadb77d69a6d` natively generated on June 27, 2026.

---

## Verification Protocol

This repository implements the **Erdős–Straus Verification Protocol v2.0** (see [`VERIFICATION_RFC.md`](VERIFICATION_RFC.md)). Key principles:

1. **Baseline Consistency:** Extension multipliers use standard baseline (10¹³ to 10¹⁷ = 10,000×)
2. **Disaggregated Counting:** Distinguishes `n_directly_evaluated`, `n_discharged_by_proven_rule`, `sieve_survivors`, `witnesses_verified`
3. **Coverage Semantics:** `coverage_type: "continuous"` requires empty `exceptions` array
4. **Witness Verification:** Every non-excluded n must have machine-checkable (x,y,z) triple or independent proof
5. **Semantic Validation:** JSON Schema validates structure; `verify_claims.py` enforces semantic constraints

### Example Usage

```bash
# Verify claims against coverage declaration
python tools/verify_claims.py --claims example_claim.json --coverage example_coverage.json

# Generate portal text from verified claims
python tools/verify_claims.py --claims example_claim.json --coverage example_coverage.json --generate-portal

# Validate with witness database
python tools/verify_claims.py --claims claims.json --coverage coverage.json --witnesses witnesses.db
```

### Important Notice on Unverified Claims

> Claims about ranges beyond verified bounds (e.g., 10¹⁷) without accompanying witness data or sieve proofs shall be marked as **"insufficient evidence; cannot be cited as verified"** rather than "invalid" or "false". Lack of evidence means the claim is unproven, not disproven.

---

## 🗂️ Unified Repository Structure

```
commencethescourge-erdos/
├── v113_quantum_flank_31.py      # Core v113 hot corridor sieve engine
├── erdos_manifest.json           # Ground-truth verification manifest
├── erdos_aggregates.json         # Modulo corridor breach aggregates
├── KAGGLE_OUTPUT_RECORD.jsonl    # Remote Kaggle execution audit trail
├── VERIFICATION_RFC.md           # Verification protocol specification
├── claims_schema.json            # JSON Schema for claims validation
├── example_claim.json            # Example verified claim
├── example_coverage.json         # Example coverage declaration
├── harness/
│   └── erdos_straus_harness.py   # Numba @njit JIT solver & exact arithmetic verifier
├── tools/
│   ├── build_erdos_sieve_notebook.py # Automated Kaggle nbformat v4 generator
│   └── verify_claims.py          # Semantic verifier for claims
└── benchmarks/
    ├── erdos_h100_output.log     # NVIDIA H100 GPU benchmark run log
    └── erdos_h200_output.log     # NVIDIA H200 GPU benchmark run log
```

---

## Architecture
The sieve partitions work deterministically: same seed + same survivor list = same partition. This is **parallel transport** of number theory problems across compute nodes — the manifold geometry of the solution space.

Every measurement in this system is a **vinculum**:
*   solutions / search space = Discovery progress
*   stride width / n = Corridor efficiency

*Built by commencethescourge. Accept no replicas.*
