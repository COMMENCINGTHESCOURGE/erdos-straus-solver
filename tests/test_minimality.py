"""Regression tests for minimality, import safety, and p² verification.

Tests that the biased minimal-A scan has been replaced with strict ascending
enumeration, that sweep_100m.py is importable, and that check_A solves
4/p² (not 4/p).
"""
import sys
from pathlib import Path

# Ensure repo root is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest


# ---------- Test 1: find_min_A uses strict ascending enumeration ----------

def test_find_min_A_is_strictly_ascending():
    """Verify find_min_A returns the same result as a brute-force ascending scan.

    For a set of known exceptional primes, the minimal A returned by find_min_A
    must equal the first A = 4m+3 (ascending from m=0) that check_A(p, A) accepts.
    """
    from sweep_100m import find_min_A, check_A

    # Small exceptional primes (p ≡ 1 mod 12, c = (p+3)/4 has no factor ≡ 2 mod 3)
    test_primes = [13, 37, 61, 157, 193, 241, 277, 313, 349, 397, 421, 457]

    for p in test_primes:
        result = find_min_A(p, max_m=200)
        if result is None:
            continue

        # Brute-force ascending scan for ground truth
        ground_truth_A = None
        for m in range(200):
            A = 4 * m + 3
            ok, info = check_A(p, A)
            if ok:
                ground_truth_A = A
                break

        assert ground_truth_A is not None, f"Brute force found nothing for p={p}"
        assert result["A"] == ground_truth_A, (
            f"find_min_A returned A={result['A']} for p={p}, "
            f"but strict ascending scan found A={ground_truth_A}"
        )


# ---------- Test 2: Unlisted A-values below listed ones ----------

def test_unlisted_A_below_listed(monkeypatch):
    """Verify find_min_A checks A-values in strict ascending order using a mock.
    
    We inject a fake predicate that accepts both A=27 and A=31. If the scan
    is correctly ascending, it must return 27 (m=6), even though 31 (m=7) is 
    one of the 'historically listed' A-values and 27 is an 'unlisted' one.
    """
    import sweep_100m
    
    def fake_check_A(p, A):
        # Fake predicate that only accepts A=27 and A=31
        if A in (27, 31):
            return True, {"A": A}
        return False, None
        
    # Patch check_A in the sweep_100m module
    monkeypatch.setattr(sweep_100m, "check_A", fake_check_A)
    
    # Run find_min_A with any prime (the prime value is ignored by our mock)
    result = sweep_100m.find_min_A(13, max_m=200)
    
    assert result is not None, "find_min_A should have found a solution"
    assert result["A"] == 27, (
        f"Strict ascending order violated! Expected A=27 (m=6) but got A={result['A']}. "
        f"The scan likely jumped ahead to known values like 31."
    )


# ---------- Test 3: sweep_100m.py is importable ----------

def test_sweep_100m_importable():
    """Importing sweep_100m must not raise NameError or any other exception.

    This catches the bug where scan variables (MAX_P, is_p) were defined only
    inside an else block but referenced globally.
    """
    # If this import succeeds, the test passes
    import sweep_100m
    assert hasattr(sweep_100m, 'find_min_A')
    assert hasattr(sweep_100m, 'find_any_A')
    assert hasattr(sweep_100m, 'check_A')
    assert hasattr(sweep_100m, 'main')
    assert hasattr(sweep_100m, 'is_exceptional')


# ---------- Test 4: check_A solves 4/p², not 4/p ----------

def test_check_A_solves_p_squared():
    """Verify that check_A produces solutions for 4/p², and that those solutions
    do NOT necessarily satisfy 4/p = 1/x + 1/y + 1/z.

    This documents the p² vs p distinction.
    """
    from sweep_100m import check_A

    test_primes = [13, 37, 61, 157, 193]

    for p in test_primes:
        for m in range(50):
            A = 4 * m + 3
            ok, info = check_A(p, A)
            if not ok:
                continue

            # check_A sets n = p*p internally, so reconstruct the triple
            n = p * p
            x = (n + A) // 4

            # The triple must satisfy 4/p² = 1/x + 1/y + 1/z
            # i.e., 4 * x * y * z == n * (x*y + x*z + y*z)
            # We can't directly get y,z from check_A's return value (it only
            # returns {"A": A}), so we re-derive them
            nx = n * x
            from sweep_100m import factorize_full, divisors_from_factors
            fac = factorize_full(x)
            for q in list(fac):
                fac[q] *= 2
            fac[p] = fac.get(p, 0) + 4
            divs = divisors_from_factors(fac)
            target_mod = (-nx) % A

            found_valid = False
            for d in divs:
                if d % A == target_mod:
                    y = (nx + d) // A
                    z = (nx + nx * nx // d) // A
                    if y > 0 and z > 0:
                        # Must satisfy 4/n = 1/x + 1/y + 1/z where n = p²
                        assert 4 * x * y * z == n * (x*y + x*z + y*z), (
                            f"Triple ({x},{y},{z}) does not satisfy 4/{n}"
                        )
                        found_valid = True
                        break

            assert found_valid, f"check_A said OK for p={p}, A={A} but no valid triple found"
            break  # Only need one A per prime
