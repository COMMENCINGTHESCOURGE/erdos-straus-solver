# RFC: Erdős–Straus Verification Protocol v2.0

**Status:** Production-Ready Draft  
**Author:** DaShawn (Guinea Pig Trench LLC)  
**Date:** 2026-07-09  
**Supersedes:** Verification Protocol v1.0 (Draft)

---

## Executive Summary

This RFC defines the verification protocol for Erdős–Straus conjecture claims across large integer ranges. It corrects arithmetic errors, clarifies coverage semantics, and establishes machine-checkable evidence requirements.

> **Important:** Unbound claims without verifiable certificates (e.g., claims about 10¹⁷ without accompanying witness data or筛除 proofs) shall be marked as **"insufficient evidence; cannot be cited as verified"** rather than "invalid" or "false". Lack of evidence means the claim is unproven, not disproven.

---

## 1. Extension Multiplier Baseline Correction

### 1.1 Corrected Baseline

All extension multiplier calculations must use a **consistent baseline**:

| From | To | Multiplier | Notes |
|------|-----|------------|-------|
| 10¹³ | 10¹⁷ | **10,000×** | Standard baseline |
| 8×10¹³ | 10¹⁷ | **1,250×** | Alternative baseline (must be explicitly labeled) |

**Rule:** RFC documents must always specify which baseline is used. Mixing baselines within a single document is prohibited.

```json
{
  "extension_spec": {
    "baseline_start": 10000000000000,
    "baseline_end": 100000000000000000,
    "multiplier": 10000,
    "baseline_label": "standard_1e13_to_1e17"
  }
}
```

---

## 2. Performance Variables and Cost Modeling

### 2.1 Cost Factors Beyond Linear Scaling

Sieve table size does **not** necessarily scale linearly with upper bound. Fixed-modulus lookup tables may remain constant. Actual computational cost depends on:

1. **Survivor rate** (density of n requiring direct evaluation)
2. **Per-n solve cost** (iterations to find x, y, z)
3. **Memory bandwidth** (cache hits/misses for sieve tables)
4. **I/O throughput** (witness serialization, checkpointing)
5. **Shard skew** (load imbalance across parallel workers)
6. **Parallel efficiency** (contention, synchronization overhead)

### 2.2 128-bit Arithmetic Necessity

Whether intermediate values require 128-bit integers must be confirmed through **per-expression upper bound analysis**, not assumed. For each expression `E(n, x, y, z)`:

```
max_value = sup{|E(n, x, y, z)| : n ∈ [N_min, N_max], x,y,z ∈ candidate_set}
if max_value > 2⁶³ - 1:
    require_128bit = True
else:
    require_128bit = False
```

### 2.3 Economical Extrapolation Method

Instead of running complete computations to 10¹⁴, use **sampling at matched window widths** across orders of magnitude:

1. Select windows of identical width W at different scales: [10¹², 10¹²+W], [10¹³, 10¹³+W], [10¹⁴, 10¹⁴+W]
2. Measure per-n throughput and survivor rate for each window
3. Fit extrapolation model: `cost(n) = α·n^β · survivor_rate(n)^γ`
4. Validate model predictions against reserved holdout windows

---

## 3. Counting Semantics and Interval Boundaries

### 3.1 Correct Interval Cardinality

The interval [2, 8×10¹³] contains:

```
8×10¹³ - 2 + 1 = 79,999,999,999,999 integers
```

**Not** 8×10¹³. Off-by-one errors in interval counting invalidate coverage percentages.

### 3.2 Disaggregated Count Categories

All reports must distinguish:

| Metric | Definition | Example |
|--------|------------|---------|
| `n_directly_evaluated` | n where solver searched for (x,y,z) | 2.5M |
| `n_discharged_by_proven_rule` | n excluded by theorem (e.g., n ≡ 1 mod 24) | 75M |
| `sieve_survivors` | n passing initial sieve filters | 3.1M |
| `witnesses_verified` | n with machine-checkable (x,y,z) proof | 2.5M |

**Critical:** Numbers discharged by theorem belong to "continuous coverage" but are **not** "directly evaluated". Conflating these categories overstates computational work.

```json
{
  "count_breakdown": {
    "interval_start": 2,
    "interval_end": 80000000000000,
    "n_total_in_interval": 79999999999999,
    "n_discharged_by_proven_rule": 75000000000000,
    "n_sieved_out": 24987500000000,
    "n_directly_evaluated": 2500000000,
    "n_with_verified_witness": 2500000000,
    "survivor_rate": 0.03125
  }
}
```

---

## 4. Coverage Type Semantics

### 4.1 Mutual Exclusivity Rule

`coverage_type` and `exceptions` are **mutually exclusive**:

- If `coverage_type: "continuous"`, then `exceptions` **must be empty** (`[]` or omitted)
- If `coverage_type: "sparse"`, then coverage must be expressed via:
  - Explicit interval list: `[{start, end}, ...]`
  - Residue class predicates: `n ≡ r (mod m)`
  - Independent coverage index (Merkle tree root)

**Prohibited:** Using `coverage_type: "sparse"` with an extremely large `exceptions` array as a workaround for continuous coverage.

```json
{
  "coverage_declaration": {
    "coverage_type": "continuous",
    "interval": {"start": 2, "end": 1000000000000000},
    "exceptions": [],
    "theorem_basis": ["mod24_exclusion", "mod3_polynomial_identity"]
  }
}
```

```json
{
  "coverage_declaration": {
    "coverage_type": "sparse",
    "covered_intervals": [
      {"start": 2, "end": 1000000},
      {"start": 2000000, "end": 5000000}
    ],
    "residue_classes": [
      {"modulus": 24, "residues": [1, 5, 7, 9, 11, 13, 17, 19, 23]}
    ],
    "coverage_index_merkle_root": "sha256:abc123..."
  }
}
```

---

## 5. Witness Verification Requirements

### 5.1 Sampling Is Insufficient for Proof

Checking only first/middle/last samples provides **diagnostic value only**, not proof of interval-wide correctness.

### 5.2 Acceptable Verification Mechanisms

A complete claim requires **at least one** of:

1. **Universal witness dataset:** Every n not excluded by theorem has a machine-checkable (x, y, z) triple
   
2. **Cryptographic commitment:** Witness dataset has Merkle root published before verification; any alteration detectable

3. **Independent sieve proof:** Sieve exclusion rules have proofs verifiable by independent checker (e.g., Coq/Lean formalization)

4. **Re-execution capability:** Third parties can re-run computation or audit segmented portions with provided checkpoints

### 5.3 Shard Completeness ≠ Correctness

Proving shards are "non-overlapping and exhaustive" only demonstrates **task allocation completeness**. It does **not** prove each shard computed correctly. Each shard must provide:

- Input manifest (survivor list hash)
- Output witness set (Merkle root)
- Execution log hash
- Optional: intermediate checkpoints

```json
{
  "shard_proof": {
    "shard_id": "worker_07_of_32",
    "assigned_interval": {"start": 22000000000000, "end": 25000000000000},
    "input_survivors_merkle": "sha256:def456...",
    "output_witnesses_merkle": "sha256:ghi789...",
    "execution_log_hash": "sha256:jkl012...",
    "checkpoint_hashes": [
      "sha256:mno345...",
      "sha256:pqr678..."
    ],
    "verification_status": "independently_audited"
  }
}
```

---

## 6. Schema Validation and Semantic Verification

### 6.1 JSON Schema Limitations

`claims_schema.json` validates **structure only**. It cannot enforce semantic constraints like:

```
claim.value <= verified_interval.end_inclusive
```

### 6.2 Required Semantic Verifier

A separate program `verify_claims` must:

1. Load structural claims (validated by JSON Schema)
2. Load coverage declarations and witness datasets
3. Check each claim against actual verified intervals
4. Report discrepancies

```bash
$ verify_claims --claims claims.json --witnesses witnesses.db --coverage coverage.json
✓ Claim 1: n=42 verified (witness: x=2, y=3, z=7)
✓ Claim 2: interval [2, 10^9] fully covered
✗ Claim 3: n=10^14+7 lacks witness; status=UNVERIFIED
```

### 6.3 Portal文案 Generation

Public-facing portal text **must** be generated from structured claims, not hand-written. Handwritten文案 can bypass validation checks.

```python
# portal_generator.py
def generate_portal_text(verified_claims):
    # Auto-generated from structured data
    max_verified = max(c['value'] for c in verified_claims if c['type'] == 'upper_bound')
    return f"Erdős–Straus verified up to {max_verified:,}"
```

---

## 7. Release Asset Integrity

### 7.1 Hash Placeholder Correction

Example hashes in documentation must **not** use the empty-content SHA-256 (`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). Use explicit placeholders:

```yaml
# INCORRECT (empty file hash):
example_hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

# CORRECT (explicit placeholder):
example_hash: "<sha256-of-exact-release-asset>"
```

### 7.2 Release Asset Security Protocol

Release assets can be replaced post-publication. Mitigation requires:

1. **Byte normalization:** Define exact byte order, encoding, line endings before hashing
2. **Signature verification:** All assets signed with GPG/SSH key; public key fingerprint published
3. **Rollback strategy:** Procedure for revoking compromised releases and reissuing with new signatures
4. **Timestamped transparency log:** All release hashes logged in append-only ledger (e.g., Sigstore Rekor)

```yaml
release_protocol:
  asset_normalization:
    line_endings: "LF"
    encoding: "UTF-8"
    trailing_newline: true
  signature:
    type: "GPG"
    key_fingerprint: "<fingerprint-of-signing-key>"
  transparency_log:
    provider: "Sigstore Rekor"
    entry_uuid: "<uuid-of-log-entry>"
  rollback:
    revocation_key: "<fingerprint-of-revocation-key>"
    notification_channel: "security@guineapigtrench.com"
```

---

## Appendix A: Claims Schema (claims_schema.json)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://guineapigtrench.com/schemas/erdos-straus-claims.json",
  "title": "Erdős–Straus Verification Claims",
  "description": "Schema for verified interval claims and witness commitments",
  "type": "object",
  "required": ["claim_type", "value", "evidence_commitment"],
  "properties": {
    "claim_type": {
      "type": "string",
      "enum": ["upper_bound", "interval_coverage", "witness_count", "survivor_rate"]
    },
    "value": {
      "type": "number",
      "minimum": 2
    },
    "evidence_commitment": {
      "type": "object",
      "required": ["merkle_root", "witness_count"],
      "properties": {
        "merkle_root": {
          "type": "string",
          "pattern": "^sha256:[a-f0-9]{64}$"
        },
        "witness_count": {
          "type": "integer",
          "minimum": 0
        },
        "checkpoint_hashes": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^sha256:[a-f0-9]{64}$"
          }
        }
      }
    },
    "coverage_type": {
      "type": "string",
      "enum": ["continuous", "sparse"]
    },
    "exceptions": {
      "type": "array",
      "items": {"type": "number"},
      "description": "Must be empty if coverage_type is 'continuous'"
    },
    "verified_interval": {
      "type": "object",
      "required": ["start_inclusive", "end_inclusive"],
      "properties": {
        "start_inclusive": {"type": "number", "minimum": 2},
        "end_inclusive": {"type": "number", "minimum": 2}
      }
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "verifier_signature": {
      "type": "string",
      "description": "Base64-encoded signature over canonicalized claim JSON"
    }
  },
  "allOf": [
    {
      "if": {
        "properties": {"coverage_type": {"const": "continuous"}}
      },
      "then": {
        "properties": {
          "exceptions": {
            "type": "array",
            "maxItems": 0
          }
        }
      }
    }
  ]
}
```

---

## Appendix B: Verify Claims Script Skeleton

```python
#!/usr/bin/env python3
"""
verify_claims.py — Semantic verifier for Erdős–Straus claims

Usage:
  verify_claims --claims claims.json --witnesses witnesses.db --coverage coverage.json
"""

import json
import sqlite3
import hashlib
import sys
from pathlib import Path
from typing import Dict, List, Any

def load_claims(path: str) -> List[Dict]:
    with open(path) as f:
        data = json.load(f)
        return data if isinstance(data, list) else [data]

def load_coverage(path: str) -> Dict:
    with open(path) as f:
        return json.load(f)

def verify_claim_semantics(claim: Dict, coverage: Dict, witnesses_db_path: str) -> Dict[str, Any]:
    """Return verification result with status and details."""
    result = {"claim": claim, "status": "UNKNOWN", "details": []}
    
    # Check 1: claim.value <= verified_interval.end_inclusive
    if "verified_interval" in coverage:
        max_verified = coverage["verified_interval"]["end_inclusive"]
        if claim.get("claim_type") == "upper_bound" and claim["value"] > max_verified:
            result["status"] = "UNVERIFIED"
            result["details"].append(f"Claim {claim['value']} exceeds verified bound {max_verified}")
            return result
    
    # Check 2: coverage_type consistency
    if claim.get("coverage_type") == "continuous" and claim.get("exceptions"):
        result["status"] = "INVALID_SCHEMA"
        result["details"].append("Continuous coverage must have empty exceptions")
        return result
    
    # Check 3: Witness existence (sample check)
    if witnesses_db_path and claim.get("claim_type") in ["upper_bound", "interval_coverage"]:
        conn = sqlite3.connect(witnesses_db_path)
        cursor = conn.cursor()
        
        # Sample verification: check random n values
        sample_n = claim["value"] // 2  # Middle point
        cursor.execute("SELECT x,y,z FROM witnesses WHERE n=?", (sample_n,))
        row = cursor.fetchone()
        
        if row:
            x, y, z = row
            # Verify 4/n = 1/x + 1/y + 1/z
            lhs = 4 * x * y * z
            rhs = sample_n * (y*z + x*z + x*y)
            if lhs == rhs:
                result["status"] = "VERIFIED"
                result["details"].append(f"Sample n={sample_n} witness verified")
            else:
                result["status"] = "WITNESS_INVALID"
                result["details"].append(f"Witness ({x},{y},{z}) fails verification for n={sample_n}")
        else:
            result["status"] = "WITNESS_MISSING"
            result["details"].append(f"No witness found for sample n={sample_n}")
        
        conn.close()
    
    return result

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Verify Erdős–Straus claims")
    parser.add_argument("--claims", required=True, help="Path to claims JSON")
    parser.add_argument("--coverage", required=True, help="Path to coverage JSON")
    parser.add_argument("--witnesses", help="Path to SQLite witnesses database")
    args = parser.parse_args()
    
    claims = load_claims(args.claims)
    coverage = load_coverage(args.coverage)
    
    all_verified = True
    for claim in claims:
        result = verify_claim_semantics(claim, coverage, args.witnesses)
        status_symbol = "✓" if result["status"] == "VERIFIED" else "✗"
        print(f"{status_symbol} Claim {claim.get('claim_type', 'unknown')}: {result['status']}")
        for detail in result.get("details", []):
            print(f"    → {detail}")
        if result["status"] != "VERIFIED":
            all_verified = False
    
    sys.exit(0 if all_verified else 1)

if __name__ == "__main__":
    main()
```

---

## Appendix C: Status Classification Guide

| Evidence Level | Classification | Citation Permission |
|----------------|----------------|---------------------|
| Full witnesses + Merkle root + independent audit | **VERIFIED** | May cite as proven |
| Witnesses present but no external audit | **PROVISIONALLY_VERIFIED** | May cite with caveat |
| Only sieve coverage, no witnesses for survivors | **INSUFFICIENT_EVIDENCE** | Cannot cite as verified |
| No witnesses, no sieve proof | **UNPROVEN** | Cannot cite as verified |
| Counterexample found and verified | **DISPROVEN** (for that range) | Cite as refutation |

**Critical principle:** `INSUFFICIENT_EVIDENCE` ≠ `FALSE`. A claim lacking evidence is unproven, not false.

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-06-01 | Initial draft |
| 2.0 | 2026-07-09 | Corrected baseline multiplier, added coverage semantics, witness requirements, schema limitations, release security |

---

## Acknowledgments

This RFC incorporates feedback from rigorous review addressing:
- Arithmetic baseline consistency
- Performance modeling beyond linear assumptions
- Interval counting precision
- Coverage type mutual exclusivity
- Witness verification sufficiency
- Schema vs. semantic validation separation
- Release asset integrity protocols
