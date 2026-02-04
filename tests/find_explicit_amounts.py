
import pandas as pd
import os

legacy_dir = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy"

for filename in os.listdir(legacy_dir):
    if filename.endswith(".xlsm") and filename != "$index.xlsm":
        path = os.path.join(legacy_dir, filename)
        try:
            xl = pd.ExcelFile(path)
            if "Data Type" in xl.sheet_names:
                df = pd.read_excel(xl, sheet_name="Data Type", dtype=str)
                # Check column 0
                names = df.iloc[:, 0].dropna().unique()
                for n in names:
                    if str(n).strip() in ["Amount1", "Amount2"]:
                        print(f"FOUND EXPLICIT NAME '{n}' in {filename}")
            xl.close()
        except: pass
