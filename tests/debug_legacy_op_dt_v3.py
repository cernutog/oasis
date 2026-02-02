import pandas as pd
import os
import glob

legacy_dir = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy"
operation_files = glob.glob(os.path.join(legacy_dir, "*.xlsm"))
operation_files = [f for f in operation_files if "$index" not in f]

if operation_files:
    leg_file = operation_files[0]
    print(f"Checking {leg_file}")
    df = pd.read_excel(leg_file, sheet_name="Data Type", header=None)
    print("--- First 20 rows (RAW) ---")
    print(df.head(20).to_string())
else:
    print("No legacy files.")
