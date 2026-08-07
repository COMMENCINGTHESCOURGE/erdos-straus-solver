#!/usr/bin/env python
"""SIEVE CORRIDOR VERIFICATION — deterministic CI gate for the hot corridor claim.

Guarantees checked (all integer arithmetic, no floats):

1. CORRIDOR COVERAGE: for every n with n % 24 == 0 in [24, limit],
   erdos_straus(n) must return has_sol=True.
   Mathematically guaranteed: n % 24 == 0  =>  n % 4 == 0  =>  Identity 1
   (4/n = 1/(3k) + 1/(3k) + 1/(3k) with k = n/4) always applies.

2. SOLUTION CORRECTNESS: every (x, y, z) returned by erdos_straus_int()
   satisfies 4/n = 1/x + 1/y + 1/z exactly, verified as
   4*x*y*z == n*(y*z + x*z + x*y).

3. NO ANOMALY: within the scanned corridor the solver must never return
   depth "ANOMALY".

Run:  python verify_sieve.py [--limit N] [--start N]
Default limit 1,000,000 => ~41,667 corridor n values, ~10-30s CI runtime.
"""
import argparse
import json
import math
import time
from datetime import datetime, timezone

from sieve_l40s_hot_corridor import erdos_straus, erdos_straus_int


def triple_valid(n, x, y, z):
    """Exact integer check: 4/n == 1/x + 1/y + 1/z."""
    return 4 * x * y * z == n * (y * z + x * z + x * y) and x <= y <= z


def main():
    parser = argparse.ArgumentParser(description="Hot-corridor sieve verification gate")
    parser.add_argument("--limit", type=int, default=1_000_000,
                        help="Upper bound of corridor scan (math.gcd n scanned)")
    parser.add_argument("--start", type=int, default=24)
    args = parser.parse_args()

    t0 = time.time()
    corridor_checked = 0
    corridor_solved = 0
    anomalies = []
    triples_checked = 0
    depth_counts = {}

    for n in range(args.start, args.limit + 1, 24):
        corridor_checked += 1
        has_sol, depth, triple, num_sol = erdos_straus(n)
        if not has_sol:
            anomalies.append((n, depth))
            continue
        depth_counts[depth] = depth_counts.get(depth, 0) + 1
        corridor_solved += 1
        if triple:
            assert triple_valid(n, *triple), f"INVALID triple {triple} for n={n}"
        for t in erdos_straus_int(n):
            triples_checked += 1
            assert triple_valid(n, *t), f"INVALID triple {t} for n={n}"

    elapsed = time.time() - t0
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "corridor_start": args.start,
        "corridor_limit": args.limit,
        "corridor_checked": corridor_checked,
        "corridor_solved": corridor_solved,
        "anomalies": anomalies,
        "depth_counts": depth_counts,
        "triples_verified": triples_checked,
        "elapsed_seconds": round(elapsed, 2),
    }
    with open("verify_sieve_report.json", "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)

    print(f"corridor scanned  : {corridor_checked}"
          f"  solved: {corridor_solved}")
    print(f"triples verified  : {triples_checked}")
    print(f"depth counts      : {depth_counts}")
    print(f"anomalies         : {len(anomalies)}")
    print(f"elapsed           : {elapsed:.2f}s")

    if anomalies:
        print(f"FAIL: {len(anomalies)} corridor anomalies, first: {anomalies[:5]}")
        raise SystemExit(1)
    if corridor_solved != corridor_checked:
        print("FAIL: corridor coverage below 100%")
        raise SystemExit(1)
    print("VERIFY PASSED — corridor coverage 100%, all triples exact.")


if __name__ == "__main__":
    main()