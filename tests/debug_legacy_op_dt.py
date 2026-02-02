import pandas as pd
import os
import glob

legacy_dir = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy"
operation_files = glob.glob(os.path.join(legacy_dir, "*.xlsm"))
operation_files = [f for f in operation_files if "$index" not in f]

if operation_files:
    leg_file = operation_files[0]
    print(f"Checking {leg_file}")
    try:
        xl = pd.ExcelFile(leg_file)
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
    print(f"No legacy operation files found in {legacy_dir}")
