"""
vinculum_sudoku_solver.py
Wrapper to run the differentiable sudoku solver notebook programmatically.
"""
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os
import sys

notebook_path = r"C:\Users\dasha\.gemini\antigravity-ide\scratch\erdos-straus-solver\sudoku_diff_solver.ipynb"

if not os.path.exists(notebook_path):
    print(f"Error: Notebook not found at {notebook_path}")
    sys.exit(1)

print(f"Loading notebook: {notebook_path}")
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

print("Executing notebook cells...")
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

try:
    ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path)}})
    print("Notebook executed successfully.")
    
    # Extract printed outputs from code cells
    print("\n--- Execution Output ---")
    for cell in nb.cells:
        if cell.cell_type == 'code' and 'outputs' in cell:
            for out in cell.outputs:
                if out.output_type == 'stream':
                    print(out.text, end='')
                elif out.output_type == 'execute_result':
                    if 'text/plain' in out.data:
                        print(out.data['text/plain'])
except Exception as e:
    print(f"Error during notebook execution: {e}")
    sys.exit(1)
