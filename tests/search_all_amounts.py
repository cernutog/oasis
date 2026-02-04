
import pandas as pd
import os

legacy_dir = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy"

print(f"{'File':<40} | {'Sheet':<15} | {'Row':<5} | {'Type':<15} | {'Context'}")
print("-" * 100)

for filename in os.listdir(legacy_dir):
    if filename.endswith(".xlsm") and filename != "$index.xlsm":
        path = os.path.join(legacy_dir, filename)
        try:
            xl = pd.ExcelFile(path)
            for sheet in xl.sheet_names:
                df = pd.read_excel(xl, sheet_name=sheet, dtype=str)
                for idx, row in df.iterrows():
                    row_vals = [str(v).strip() for v in row.values]
                    for v in row_vals:
                        if "Amount" in v:
                            print(f"{filename:<40} | {sheet:<15} | {idx:<5} | {v:<15} | {' '.join(row_vals[:3])}")
            xl.close()
        except Exception as e:
            pass
