import pandas as pd
import os

legacy_index = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy\$index.xlsm"
if os.path.exists(legacy_index):
    try:
        xl = pd.ExcelFile(legacy_index)
        print(f"Sheet names: {xl.sheet_names}")
        # Look for sheet that might contain global info
        target_sheet = None
        for s in xl.sheet_names:
            if any(kw in s.lower() for kw in ["general", "global", "info"]):
                target_sheet = s
                break
        
        if target_sheet:
            df = pd.read_excel(xl, sheet_name=target_sheet, header=None)
            print(f"--- {target_sheet} Content ---")
            print(df.to_string())
        else:
            print("No global info sheet found in legacy index.")
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"Legacy index not found at {legacy_index}")
