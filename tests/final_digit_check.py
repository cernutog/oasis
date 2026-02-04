
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
                        name = row_vals[0]
                        min_v = row_vals[5] if len(row_vals) > 5 else "nan"
                        max_v = row_vals[6] if len(row_vals) > 6 else "nan"
                        
                        # Count nines specifically in the integer part
                        integer_part = max_v.split(".")[0] if max_v != "nan" else ""
                        nines_count = integer_part.count("9")
                        
                        results.append({
                            "file": filename,
                            "min": min_v,
                            "max": max_v,
                            "nines": nines_count
                        })
            xl.close()
        except: pass

summaries = {}
for r in results:
    key = (r['min'], r['max'], r['nines'])
    if key not in summaries: summaries[key] = []
    summaries[key].append(r['file'])

print("LEGACY SOURCE ANALYSIS - 'Amount' Constraints:")
for key, files in summaries.items():
    print(f"Min: {key[0]}, Max: {key[1]} ({key[2]} integer nines)")
    print(f"  Found in {len(files)} files.")
