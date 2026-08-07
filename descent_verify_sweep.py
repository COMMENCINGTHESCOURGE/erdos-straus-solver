#!/usr/bin/env python3
"""
DESCENT VERIFIER — 22-Portal Sweep -> Original Erdős–Straus
============================================================
For every exceptional prime p in the Omega sweep results, reconstruct
the full (x, y, z) solution for 4/p^2 using the Omega divisor formula:

    x = (n + A) // 4,        n = p^2
    nx = n * x
    d  = stored minimal divisor  (d = -nx mod A,  d | nx^2)
    y  = (nx + d) // A
    z  = (nx + nx*nx//d) // A
    verify: 4*x*y*z == n*(x*y + x*z + y*z)

Then test the DESCENT THEOREM: if p|x, p|y, p|z, the scaled-down
(a,b,c) = (x//p, y//p, z//p) solves the ORIGINAL conjecture 4/p.

This answers the open question flagged in EMPIRICAL_NOTE.md:
"Whether this extends to the original Erdős–Straus case (4/p)
 requires a descent theorem."

vinculum: jacobian_scaling / prime_square_descent
  det(J) of the map (a,b,c) -> p*(a,b,c) is p^3.
  The descent is valid exactly where the scaling lattice pZ^3
  collapses back intact (x%p==y%p==z%p==0).

usage:  python descent_verify_sweep.py results/sweep_p*.json.gz
"""
from __future__ import annotations
import sys, json, gzip, argparse
from pathlib import Path


def reconstruct_solution(p: int, A: int, d: int) -> dict | None:
    """Reconstruct (x,y,z) for n = p^2 from stored (p, A, d)."""
    n = p * p
    x = (n + A) // 4
    nx = n * x
    # guard: d must be congruent and dividing nx^2 exactly like the solver
    if (nx * nx) % d != 0:
        return None
    y = (nx + d) // A
    z = (nx + nx * nx // d) // A
    if y <= 0 or z <= 0:
        return None
    # exact-arithmetic invariant from the harness
    if 4 * x * y * z != n * (x * y + x * z + y * z):
        return None
    m9 = n % 9
    return {"p": p, "A": A, "x": x, "y": y, "z": z,
            "nx": nx, "d": d, "mod9": m9, "mod24": p % 24}


def descent_ok(sol: dict) -> bool:
    """p | x  AND  p | y  AND  p | z  -> descent collapses. det(J)=p^3."""
    p = sol["p"]
    return sol["x"] % p == 0 and sol["y"] % p == 0 and sol["z"] % p == 0


def main(paths: list[Path]) -> None:
    rows: list[dict] = []
    for path in paths:
        opener = gzip.open(path, "rt") if path.suffix == ".gz" else open(path, "rt")
        with opener as f:
            data = json.load(f)
        if isinstance(data, list):
            rows.extend(data)
        else:
            rows.extend(data.get("results", data.get("items", [])))

    print("=" * 68)
    print("DESCENT VERIFIER — Omega 22-portal sweep -> 4/p (original)")
    print("=" * 68)

    solved, descend_ok, descend_fail, ver_fail = 0, 0, 0, 0
    max_A, worst_desc = 0, 0
    desc_by_A: dict[int, int] = {}
    mod9_breach = 0

    for rec in rows:
        p = int(rec["p"]); A = int(rec["A"]); m = int(rec.get("m", (A - 3) // 4))
        sol = reconstruct_solution(p, A, d=int(rec.get("d") or rec.get("D") or 0))
        if sol is None:
            ver_fail += 1
            continue
        solved += 1
        max_A = max(max_A, A)
        if sol["mod9"] in (0, 3, 6):
            mod9_breach += 1
        desc_by_A[A] = desc_by_A.get(A, 0) + 1

        if descent_ok(sol):
            descend_ok += 1
            if A > worst_desc:
                worst_desc = A
        else:
            descend_fail += 1

    total = len(rows)
    pct_desc = 100.0 * descend_ok / max(1, solved)
    print(f"\n  Records scanned        : {total:,}")
    print(f"  Reconstructed (x,y,z)  : {solved:,}   (verify failures: {ver_fail:,})")
    print(f"  DESCEND OK (p|x,y,z)   : {descend_ok:,}  ({pct_desc:.2f}%)")
    print(f"  DESCEND FAIL           : {descend_fail:,}")
    print(f"  Max minimal A used     : {max_A}   (worst self A that descends: {worst_desc})")
    print(f"  mod9 in {{0,3,6}} cases : {mod9_breach:,}")
    print("\n  Descend rate by shift A:")
    for a in sorted(desc_by_A):
        print(f"    A={a:>3}: {desc_by_A[a]:>8,}")

    summary = {
        "records": total, "reconstructed": solved, "verify_fail": ver_fail,
        "descend_ok": descend_ok, "descend_fail": descend_fail,
        "descend_rate": round(pct_desc, 4), "max_A": max_A,
        "worst_descending_A": worst_desc, "mod9_breach": mod9_breach,
        "distribution_A": desc_by_A,
    }
    out = Path(__file__).with_name("descent_verify_summary.json")
    out.write_text(json.dumps(summary, indent=2))
    print(f"\n  Saved: {out}")
    return summary


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", type=Path,
                    default=list(Path(__file__).parent.glob("results/sweep_*.json*")))
    args = ap.parse_args()
    if not args.paths:
        print("No sweep result files found.")
        sys.exit(1)
    main(args.paths)