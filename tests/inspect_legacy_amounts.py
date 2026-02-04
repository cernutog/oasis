
import pandas as pd
import os

legacy_dir = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy"
results = []

for filename in os.listdir(legacy_dir):
    if filename.endswith(".xlsm") and filename != "$index.xlsm":
        path = os.path.join(legacy_dir, filename)
        try:
            xl = pd.ExcelFile(path)
            if "Data Type" in xl.sheet_names:
                df = pd.read_excel(xl, sheet_name="Data Type", dtype=str)
                # Find row with Amount
                for idx, row in df.iterrows():
                    row_vals = [str(v).strip() for v in row.values]
                    if any("Amount" == v for v in row_vals):
                        # Find which column is Amount
                        col_idx = row_vals.index("Amount")
                        # Usually Type is next, then Format, then Min, Max...
                        # Let's just store the whole row for analysis
                        results.append({
                            "file": filename,
                            "row": row_vals
                        })
            xl.close()
        except Exception as e:
            print(f"Error reading {filename}: {e}")

for res in results:
    print(f"File: {res['file']}")
    print(f"  Row: {res['row']}")
