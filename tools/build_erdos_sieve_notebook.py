"""
P2 Fix: Wraps v113_quantum_flank_31 sieve into proper .ipynb JSON for Kaggle.
The previous submissions failed because raw .py text was fed as a notebook.
This script reads the Python source and embeds it in valid nbformat v4 JSON.
"""
import json
import os

# Source sieve script
sieve_source_path = os.path.join(os.path.dirname(__file__), "..", "v113_quantum_flank_31.py")

if not os.path.exists(sieve_source_path):
    # Fallback to G: drive cold storage
    sieve_source_path = os.path.join(os.path.dirname(__file__), "..", "v113_quantum_flank_31.py")

if not os.path.exists(sieve_source_path):
    print(f"ERROR: Cannot find sieve source at {sieve_source_path}")
    print("Please provide the path to v113_quantum_flank_31.py or v113_clean.py")
    exit(1)

with open(sieve_source_path, "r", encoding="utf-8") as f:
    sieve_code = f.read()

# Build proper nbformat v4 notebook
cells = [
    {
        "cell_type": "markdown",
        "id": "cell_0",
        "metadata": {},
        "source": [
            "# ERDŐS–STRAUS V113 — Quantum Flank 31\n",
            "\n",
            "GPU-accelerated sieve for the Erdős–Straus conjecture.\n",
            "- **Engine**: v113_quantum_flank_31\n",
            "- **Axiom**: STATUTORY_SIEVE_v3\n",
            "- **Target**: 50,000,000\n",
            "- **Stride**: mod-24 hot corridor\n",
            "- **Classification**: mod-9 (STABLE/BREACH/NEUTRAL)\n"
        ]
    },
    {
        "cell_type": "code",
        "id": "cell_1",
        "metadata": {},
        "source": ["!pip install numpy -q\n", "import numpy as np\n", "print('NumPy version:', np.__version__)"],
        "execution_count": None,
        "outputs": []
    },
    {
        "cell_type": "code",
        "id": "cell_2",
        "metadata": {},
        "source": sieve_code.splitlines(keepends=True),
        "execution_count": None,
        "outputs": []
    }
]

notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.12.0"
        },
        "accelerator": "GPU"
    },
    "cells": cells
}

# Output paths
out_notebook = os.path.join(os.path.dirname(__file__), "..", "v113_quantum_flank_31.ipynb")
out_metadata = os.path.join(os.path.dirname(__file__), "..", "kernel-metadata.json")

with open(out_notebook, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1)
print(f"Notebook written: {out_notebook}")

# Also generate matching kernel-metadata.json for Kaggle push
kernel_meta = {
    "id": "commencethescourge/erdos-straus-v113-quantum-flank-31",
    "title": "ERDŐS–STRAUS V113 — Quantum Flank 31",
    "code_file": out_notebook,
    "language": "python",
    "kernel_type": "notebook",
    "is_private": True,
    "enable_gpu": True,
    "enable_internet": False,
    "dataset_sources": [],
    "competition_sources": [],
    "kernel_sources": []
}

with open(out_metadata, "w", encoding="utf-8") as f:
    json.dump(kernel_meta, f, indent=2)
print(f"Kernel metadata written: {out_metadata}")
print("\nTo push to Kaggle: kaggle kernels push -p", os.path.dirname(out_metadata))
