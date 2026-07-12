import sys, os, gzip, json, hashlib

def verify_dataset(json_gz_path, manifest_path):
    print(f"Verifying {json_gz_path}...")
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    # 1. SHA-256
    sha256 = hashlib.sha256()
    with open(json_gz_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    file_hash = sha256.hexdigest()
    if file_hash != manifest['data_sha256']:
        raise ValueError(f"Hash mismatch! Expected {manifest['data_sha256']}, got {file_hash}")
        
    # 2. Certificates
    with gzip.open(json_gz_path, 'rt', encoding='utf-8') as f:
        data = json.load(f)
        
    if len(data) != manifest['total_solved']:
        raise ValueError(f"Count mismatch! Expected {manifest['total_solved']}, got {len(data)}")
        
    from collections import Counter
    m_dist = Counter()
    
    for row in data:
        p, A, m, d = row['p'], row['A'], row['m'], row['d']
        m_dist[str(m)] += 1
        
        n = p * p
        x = (n + A) // 4
        nx = n * x
        if d == 0 or (nx * nx) % d != 0:
            raise ValueError(f"Invalid d={d} for p={p}, A={A}")
        y = (nx + d) // A
        z = (nx + nx * nx // d) // A
        
        if not (y > 0 and z > 0 and 4 * x * y * z == n * (x*y + x*z + y*z)):
            raise ValueError(f"Identity failed for p={p}, A={A}, d={d}")
            
    # Check dist
    manifest_dist = manifest['distribution_m']
    for k, v in m_dist.items():
        if manifest_dist.get(str(k)) != v:
            raise ValueError(f"Distribution mismatch for m={k}")
            
    print(f"Verification passed for {manifest['total_solved']} records.")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--results-dir', default='results')
    args = parser.parse_args()

    results_dir = args.results_dir
    success = True
    for mf in os.listdir(results_dir):
        if mf.endswith('_manifest.json'):
            json_gz = mf.replace('_manifest.json', '.json.gz')
            try:
                verify_dataset(os.path.join(results_dir, json_gz), os.path.join(results_dir, mf))
            except Exception as e:
                print(f"Failed {json_gz}: {e}")
                success = False
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()
