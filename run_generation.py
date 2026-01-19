from src.main import generate_oas
import os
import sys

# Ensure src is in path
sys.path.append(os.getcwd())

BASE_DIR = os.path.abspath('Imported Templates')

print(f"Running OAS Generation in {BASE_DIR}...")
generate_oas(base_dir=BASE_DIR, gen_30=False, gen_31=True)
print("Done.")
