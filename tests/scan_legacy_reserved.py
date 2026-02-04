
import pandas as pd
import os

legacy_dir = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy"
files = [f for f in os.listdir(legacy_dir) if f.endswith(".xlsm") and f != "$index.xlsm"]

reserved = ["object", "array"]
found = []

for f in files:
    p = os.path.join(legacy_dir, f)
    try:
        xl = pd.ExcelFile(p)
        if "Data Type" in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name="Data Type")
            # Heuristic: find any cell containing reserved words in column 0 or 1
            for idx, row in df.head(50).iterrows():
                for val in row.astype(str).values:
                    if str(val).strip().lower() in reserved:
                        found.append(f"{f}: Found '{val}' at row {idx}")
        xl.close()
    except Exception as e:
        pass

if not found:
    print("No explicit definitions of 'object' or 'array' found in legacy Data Type sheets.")
else:
    for f in found:
        print(f)
