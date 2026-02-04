
import pandas as pd
import os

legacy_dir = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy"
target = "9999999999999.99"

for filename in os.listdir(legacy_dir):
    if filename.endswith(".xlsm"):
        path = os.path.join(legacy_dir, filename)
        try:
            xl = pd.ExcelFile(path)
            for sheet in xl.sheet_names:
                df = pd.read_excel(xl, sheet_name=sheet, dtype=str)
                if df.isin([target]).any().any():
                    print(f"FOUND in {filename}, sheet {sheet}")
            xl.close()
        except: pass
