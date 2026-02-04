
import pandas as pd
import os

legacy_dir = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy"
idx_path = os.path.join(legacy_dir, "$index.xlsm")

def dump_index():
    xl_idx = pd.ExcelFile(idx_path)
    sheet_name = next((s for s in xl_idx.sheet_names if "path" in s.lower()), "Paths")
    df_p = pd.read_excel(xl_idx, sheet_name=sheet_name, header=1)
    file_col = next((c for c in df_p.columns if "excel" in str(c).lower()), df_p.columns[0])
    files = df_p[file_col].dropna().unique().tolist()
    print("Files in Index Order:")
    for f in files[:5]:
        print(f" - {f}")

dump_index()
