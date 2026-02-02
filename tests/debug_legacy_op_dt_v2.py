import pandas as pd
import os
import glob

legacy_dir = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy"
operation_files = glob.glob(os.path.join(legacy_dir, "*.xlsm"))
operation_files = [f for f in operation_files if "$index" not in f]

if operation_files:
    leg_file = operation_files[0]
    print(f"Checking {leg_file}")
    xl = pd.ExcelFile(leg_file)
    df = pd.read_excel(xl, sheet_name="Data Type", header=None)
    
    header_row_idx = -1
    for idx, row in df.head(10).iterrows():
        row_vals = [str(v).strip().lower() for v in row.values]
        if "data type" in row_vals or "type" in row_vals:
            header_row_idx = idx
            break
            
    if header_row_idx != -1:
        headers = [str(c).strip() for c in df.iloc[header_row_idx]]
        print(f"Header Row: {header_row_idx}")
        print(f"Headers: {headers}")
        df.columns = headers
        df = df.iloc[header_row_idx+1:].reset_index(drop=True)
        print("Data Row 0:")
        print(df.iloc[0].to_dict())
    else:
        print("Header not found with keywords.")
        print("First 2 rows:")
        print(df.head(2).to_string())
else:
    print("No legacy files.")
