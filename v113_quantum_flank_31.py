# ERDOS–STRAUS V113 — Quantum Flank 31 (OPTIMIZED)
# Paste into Kaggle notebook — ONE cell at a time
# DaShawn / Guinea Pig Trench LLC — May 2026

# ═══════════════════════════════════════
# CELL 1: Setup
# ═══════════════════════════════════════
import numpy as np, json, time, hashlib, os, subprocess
from datetime import datetime
from numba import njit
import multiprocessing as mp

try:
    result = subprocess.run(['nvidia-smi','--query-gpu=name','--format=csv,noheader'],
                          capture_output=True, text=True, timeout=5)
    GPU = result.stdout.strip() if result.returncode == 0 else 'CPU'
except:
    GPU = 'CPU'

print(f'GPU: {GPU} | NumPy: {np.__version__}')

# ═══════════════════════════════════════
# CELL 2: Config
# ═══════════════════════════════════════
TARGET = 1_000_000_000
CHUNK = 1_000_000
MOD24 = np.array([1, 5, 7, 9, 11, 13, 17, 19, 23], dtype=np.int64)
NUM_WORKERS = mp.cpu_count()
print(f'Target: {TARGET:,} | Chunk: {CHUNK:,} | Mod24: {MOD24.tolist()} | Workers: {NUM_WORKERS}')

# ═══════════════════════════════════════
# CELL 3: Optimized Sieve with Numba JIT
# ═══════════════════════════════════════
@njit(fastmath=True)
def sieve_chunk(start, end, mod24_classes):
    """JIT-compiled sieve for maximum performance"""
    sols_n = []
    sols_x = []
    sols_y = []
    sols_z = []
    sols_m = []
    
    for mc_idx in range(len(mod24_classes)):
        mc = mod24_classes[mc_idx]
        n = start
        # Find first n ≡ mc (mod 24)
        remainder = n % 24
        offset = (mc - remainder) % 24
        n = n + offset
        
        count = 0
        while n < end and count < 300:
            xs = (n + 3) // 4
            if xs < 1:
                xs = 1
            xe = n * 2
            step = (xe - xs) // 60
            if step < 1:
                step = 1
            
            found = False
            x = xs
            while x <= xe and not found:
                d = 4 * x - n
                if d > 0:
                    ys = (n * x + d - 1) // d
                    if ys < 1:
                        ys = 1
                    ye = (2 * n * x) // d
                    if ye >= ys:
                        y_max = ys + 30
                        if ye + 1 < y_max:
                            y_max = ye + 1
                        y = ys
                        while y < y_max:
                            dz = 4 * x * y - n * (x + y)
                            if dz > 0:
                                nxy = n * x * y
                                if nxy % dz == 0:
                                    z = nxy // dz
                                    if z > 0:
                                        sols_n.append(n)
                                        sols_x.append(x)
                                        sols_y.append(y)
                                        sols_z.append(z)
                                        sols_m.append(mc)
                                        found = True
                                        break
                            y += 1
                x += step
            n += 24
            count += 1
    
    return np.array(sols_n), np.array(sols_x), np.array(sols_y), np.array(sols_z), np.array(sols_m)

def sieve(start, end, mod24_classes):
    """Wrapper that converts numpy arrays to list of dicts"""
    n_arr, x_arr, y_arr, z_arr, m_arr = sieve_chunk(start, end, mod24_classes)
    sols = []
    for i in range(len(n_arr)):
        sols.append({
            'n': int(n_arr[i]),
            'x': int(x_arr[i]),
            'y': int(y_arr[i]),
            'z': int(z_arr[i]),
            'm': int(m_arr[i])
        })
    return sols

print('Sieve ready (JIT compiled)')

# ═══════════════════════════════════════
# CELL 4: Optimized Run with JIT Warmup
# ═══════════════════════════════════════
if __name__ == '__main__':
    print('Warming up JIT compiler...')
    _ = sieve_chunk(2, 1000, MOD24)
    print('JIT warmup complete')

    print('Running optimized sieve...')
    start_time = time.perf_counter()
    chunks_done = 0
    total_sols = 0
    stable = 0
    breach = 0

    for cs in range(2, TARGET, CHUNK):
        ce = min(cs + CHUNK, TARGET)
        sols = sieve(cs, ce, MOD24)
        total_sols += len(sols)
        chunks_done += 1
        
        if sols:
            # Vectorized computation using numpy arrays
            n_arr = np.array([s['n'] for s in sols])
            z_arr = np.array([s['z'] for s in sols])
            x_arr = np.array([s['x'] for s in sols])
            y_arr = np.array([s['y'] for s in sols])
            
            denom = x_arr + y_arr
            valid_mask = denom > 0
            if np.sum(valid_mask) > 1:
                tors = (n_arr[valid_mask] * z_arr[valid_mask]) / denom[valid_mask]
                mean_tors = np.mean(tors)
                std_tors = np.std(tors)
                if std_tors / (mean_tors + 1) < 0.3:
                    stable += 1
                else:
                    breach += 1
        
        if chunks_done % 100 == 0:
            elapsed = time.perf_counter() - start_time
            rate = chunks_done / elapsed if elapsed > 0 else 0
            print(f'  [{ce/TARGET*100:.1f}%] {total_sols:,} solutions | STABLE:{stable} BREACH:{breach} | {rate:.1f} chunks/s')

    elapsed = time.perf_counter() - start_time
    print(f'\nDONE: {total_sols:,} solutions | STABLE:{stable} | BREACH:{breach}')
    print(f'Total time: {elapsed:.2f}s | Rate: {chunks_done/elapsed:.1f} chunks/s')

    # ═══════════════════════════════════════
    # CELL 5: Save
    # ═══════════════════════════════════════
    output = {
        'flank': 31,
        'version': 'v113',
    'gpu': GPU,
    'target': TARGET,
    'solutions': total_sols,
    'stable': stable,
    'breach': breach,
    'ts': datetime.now().isoformat(),
    'hash': hashlib.sha256(f'{total_sols}{stable}{breach}'.encode()).hexdigest()
}

with open('/kaggle/working/v113_output.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f'\nSaved to /kaggle/working/v113_output.json')
print(f'Hash: {output["hash"][:16]}...')
print(f'\nCOPY THIS FOR LOCAL MERGE:')
print(json.dumps(output))
