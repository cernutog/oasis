
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
                for idx, row in df.iterrows():
                    row_vals = [str(v).strip() for v in row.values]
                    if any("Amount" == v for v in row_vals):
                        # Heuristic: find columns
                        # col 0: Name, col 1: Desc, col 2: Type, col 3: Format, col 5: Min, col 6: Max
                        name = row_vals[0]
                        min_v = row_vals[5] if len(row_vals) > 5 else "N/A"
                        max_v = row_vals[6] if len(row_vals) > 6 else "N/A"
                        
                        max_len = len(max_v.replace(".", "")) if max_v != "nan" else 0
                        
                        results.append({
                            "file": filename,
                            "name": name,
                            "min": min_v,
                            "max": max_v,
                            "digits": max_len
                        })
            xl.close()
        except: pass

# Summarize unique combinations
summaries = {}
for r in results:
    key = (r['min'], r['max'], r['digits'])
    if key not in summaries:
        summaries[key] = []
    summaries[key].append(r['file'])

print("Summary of 'Amount' definitions found in legacy files:")
for key, files in summaries.items():
    print(f"Min: {key[0]}, Max: {key[1]}, Total Digits (no dot): {key[2]}")
    print(f"  Count: {len(files)}")
    print(f"  Example files: {files[:3]}")
    print("-" * 20)
