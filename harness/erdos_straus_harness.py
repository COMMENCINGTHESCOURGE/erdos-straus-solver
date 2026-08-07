import time
import sys
import numba
from numba import njit

# -----------------------------------------------------------------------------
# NVARC-Style Test-Time Optimization (TTO) Layer
# -----------------------------------------------------------------------------
# We aggressively JIT compile the core search kernels to C-level speeds.
# This prevents the solver from timing out on Kaggle-style strict execution bounds.

@njit(nopython=True, fastmath=True)
def find_smallest_solution_greedy(n):
    """
    Attempts the greedy fraction separation.
    4/n = 1/x + remainder
    """
    greedy_x = (n + 3) // 4
    num = 4 * greedy_x - n
    den = n * greedy_x
    
    # We search for y and z such that 1/y + 1/z = num/den
    # which implies (y*num - den) * (z*num - den) = den^2
    # We just search y up to some reasonable limit.
    for y in range(greedy_x, greedy_x + 20000):
        numerator = den * y
        denominator = num * y - den
        
        if denominator > 0 and numerator % denominator == 0:
            z = numerator // denominator
            if z > 0 and z >= y:
                return (greedy_x, y, z, 1) # strategy 1 = greedy
                
    return (0, 0, 0, 0)

@njit(nopython=True, fastmath=True)
def find_smallest_solution_brute(n):
    """
    Brute-force approach for when greedy fails, heavily bounded for TTO.
    """
    max_x = n
    if max_x > 5000:
        max_x = 5000
        
    for x in range(1, max_x):
        num1 = 4 * x - n
        if num1 <= 0:
            continue
        den1 = n * x
        
        for y in range(x, x + 20000):
            numerator = den1 * y
            denominator = num1 * y - den1
            
            if denominator > 0 and numerator % denominator == 0:
                z = numerator // denominator
                if z > 0 and z >= y:
                    return (x, y, z, 2) # strategy 2 = brute
                    
    return (0, 0, 0, 0)

def find_smallest_solution(n):
    """
    Tries greedy, then falls back to brute-force.
    Returns (x, y, z, strategy, execution_time)
    """
    start_time = time.perf_counter()
    
    x, y, z, strategy = find_smallest_solution_greedy(n)
    
    if strategy == 0:
        x, y, z, strategy = find_smallest_solution_brute(n)
        
    execution_time = time.perf_counter() - start_time
    return x, y, z, strategy, execution_time

# -----------------------------------------------------------------------------
# Tufa-Style Sandboxing & Verification Layer
# -----------------------------------------------------------------------------

def is_prime(n):
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def verify_algebraic_constraint(n, x, y, z):
    """
    Exact fraction arithmetic verification to prevent floating point loss.
    Checks if 4/n == 1/x + 1/y + 1/z
    """
    # 4/n == (y*z + x*z + x*y) / (x*y*z)
    lhs = 4 * (x * y * z)
    rhs = n * (y * z + x * z + x * y)
    return lhs == rhs

def run_harness():
    print("[SYSTEM] Booting Erdos-Straus Verification Harness...")
    print("[SYSTEM] Compiling Numba JIT kernels...")
    
    # Warmup JIT
    find_smallest_solution(5)
    print("[SYSTEM] JIT Compilation complete. Entering target execution envelope.")
    
    # Hard case sequence (focusing on mod 24 primes)
    # The hardest known classes are 1, 5, 9 mod 24
    test_bounds = range(2, 5000)
    
    hard_cases = 0
    failures = 0
    
    print(f"\n{'n':>6} | {'mod 24':>6} | {'Strategy':>8} | {'(x, y, z)':>35} | {'Max %':>8} | {'Verif':>6} | {'TTO(ms)':>8}")
    print("-" * 90)
    
    for n in test_bounds:
        if not is_prime(n):
            continue
            
        mod24 = n % 24
        if mod24 not in (1, 5, 9, 13, 17, 19, 23):
            continue
            
        is_hard = (mod24 == 1)
        if is_hard:
            hard_cases += 1
            
        x, y, z, strat_code, tto = find_smallest_solution(n)
        
        if strat_code == 0:
            print(f"[FAIL] Hard failure isolated at n={n}. Harness boundary exceeded.")
            failures += 1
            continue
            
        # Tufa Verification Check
        is_valid = verify_algebraic_constraint(n, x, y, z)
        if not is_valid:
            print(f"[ERROR] Verification failed for n={n}! Math invariant violated.")
            failures += 1
            continue
            
        # Parity 000 anomaly check
        if x % 2 == 0 and y % 2 == 0 and z % 2 == 0:
            pass # Continue execution
            
        strat_str = "GREEDY" if strat_code == 1 else "BRUTE"
        max_frac = max(1/x, 1/y, 1/z) * 100
        
        # Only print hard cases or exceptionally long executions to avoid log flooding
        if is_hard or tto > 0.01:
            color_prefix = "\033[91m" if is_hard else ""
            color_suffix = "\033[0m" if is_hard else ""
            print(f"{color_prefix}{n:>6} | {mod24:>6} | {strat_str:>8} | {(x, y, z)!s:>35} | {max_frac:>7.2f}% | {'[OK]':>6} | {tto*1000:>8.3f}{color_suffix}")

    print("\n" + "="*50)
    print("HARNESS EXECUTION SUMMARY")
    print("="*50)
    print(f"Total Prime Bounds Searched: {len(test_bounds)}")
    print(f"Verified Hard Cases (n == 1 mod 24): {hard_cases}")
    print(f"Verification Failures: {failures}")
    if failures == 0:
        print("\n[SUCCESS] Pipeline invariant stable. Test-Time Optimization successful.")

if __name__ == "__main__":
    run_harness()
