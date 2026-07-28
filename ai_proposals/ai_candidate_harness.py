import time
import sqlite3
from typing import Tuple, Iterable, Callable

# Import your existing exact verifier here. Replace the mock below with:
# from solver.core import verify_egyptian
# and update the call sites accordingly.

def verify_egyptian_mock(n: int, x: int, y: int, z: int) -> bool:
    """Fallback mock if import fails. MUST be replaced by your exact verifier."""
    return 4 * x * y * z == n * (y * z + x * z + x * y)


def run_harness(n_values, infer_fn: Callable[[int, int], Iterable[Tuple[int, int, int]]], tries_per_n=64, db_path="ai_proposals.db"):
    """Run the AI candidate harness.

    - n_values: iterable of n to test
    - infer_fn: function(n, k) -> iterable of (x,y,z) candidates
    - tries_per_n: proposals per n
    - db_path: sqlite path to record proposals/results
    """
    # Setup Results DB
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results
                 (n INTEGER, x INTEGER, y INTEGER, z INTEGER, verified BOOLEAN, timestamp REAL)''')

    results = []
    for n in n_values:
        start = time.time()
        verified = False

        # Model proposes candidates
        for (x, y, z) in infer_fn(n, k=tries_per_n):
            if verify_egyptian_mock(n, x, y, z):
                verified = True
                results.append((n, x, y, z))
                c.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?, ?)", 
                          (n, x, y, z, True, time.time()))
                conn.commit()
                break  # Move to next n upon success
            else:
                c.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?, ?)", 
                          (n, x, y, z, False, time.time()))

        conn.commit()
        elapsed = time.time() - start
        print(f"n={n} | verified={verified} | time={elapsed:.3f}s")

    conn.close()
    return results


if __name__ == "__main__":
    # Simple standalone demo when run directly. Uses a naive sampler that will
    # include a known correct witness for n=4 so the smoke-run can succeed.
    def demo_infer(n, k=16):
        # If n==4, yield a known solution (2,3,6)
        if n == 4:
            yield (2, 3, 6)
            return
        # Otherwise yield a few deterministic placeholders
        for i in range(k):
            x = n + 1 + i
            y = x + 1
            z = y + 1
            yield (x, y, z)

    found = run_harness(range(2, 51), infer_fn=demo_infer, tries_per_n=32, db_path='ai_proposals_demo.db')
    print('Found:', found)
