import pandas as pd
import os

legacy_index = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy\$index.xlsm"

if os.path.exists(legacy_index):
    try:
        xl = pd.ExcelFile(legacy_index)
        sheet_name = "Data Type"
        if sheet_name in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None, nrows=10)
            print(f"--- {sheet_name} Top Rows ---")
            print(df.to_string())
        else:
            print(f"Sheet {sheet_name} not found. Available: {xl.sheet_names}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"Legacy index not found at {legacy_index}")
