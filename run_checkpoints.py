import subprocess

checkpoints = [100000, 1000000, 10000000, 100000000]

for cp in checkpoints:
    print(f"Running sweep for max_p = {cp}")
    subprocess.run(["python", "sweep_100m.py", "--max-p", str(cp)], check=True)
