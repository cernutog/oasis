
import pandas as pd
import os

legacy_dir = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy"
idx_path = os.path.join(legacy_dir, "$index.xlsm")

def find_first_usage():
    xl_idx = pd.ExcelFile(idx_path)
    sheet_name = next((s for s in xl_idx.sheet_names if "path" in s.lower()), "Paths")
    df_p = pd.read_excel(xl_idx, sheet_name=sheet_name, header=1)
    file_col = next((c for c in df_p.columns if "excel" in str(c).lower()), df_p.columns[0])
    files = df_p[file_col].dropna().unique().tolist()
    
    for filename in files:
        filename = str(filename).strip()
        if not filename.endswith(".xlsm"): filename += ".xlsm"
        path = os.path.join(legacy_dir, filename)
        if not os.path.exists(path): continue
        xl = pd.ExcelFile(path)
        for sheet in xl.sheet_names:
            if sheet.isdigit() or sheet in ["Path", "Header", "Body"]:
                df = pd.read_excel(xl, sheet_name=sheet)
                for v in df.values.flatten():
                    if str(v).strip() == "Amount":
                        print(f"File: {filename}, Sheet: {sheet}")
                        return
find_first_usage()
