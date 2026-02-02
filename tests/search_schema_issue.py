import pandas as pd
import os
import glob

legacy_dir = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy"
files = glob.glob(os.path.join(legacy_dir, "*.xlsm"))

for f in files:
    if "$index" in f: continue
    print(f"Checking {os.path.basename(f)}")
    try:
        df = pd.read_excel(f, sheet_name="Data Type", header=None)
        for idx, row in df.iterrows():
            row_vals = [str(v).strip() for v in row.values]
            if any("standard amount" in v.lower() for v in row_vals):
                print(f"  Row {idx}: {row_vals}")
    except Exception as e:
        pass
