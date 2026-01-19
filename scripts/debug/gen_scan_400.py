import pandas as pd
import glob
import os

files = glob.glob("API Templates/*.xlsm")
if not files:
    # try full path pattern
    files = glob.glob(
        "c:/Users/giuse/.gemini/antigravity/scratch/OAS_Generation_Tool/API Templates/*.xlsm"
    )

print(f"Found {len(files)} files.")

for f in files:
    try:
        xls = pd.ExcelFile(f)
        if "400" in xls.sheet_names:
            print(f"\n[{os.path.basename(f)}] HAS '400' SHEET")
            # Peek content
            df = pd.read_excel(f, sheet_name="400", header=None)
            # Find header
            header_idx = -1
            for idx, row in df.iterrows():
                if row.astype(str).str.contains("Name").any():
                    header_idx = idx
                    break
            if header_idx != -1:
                df.columns = df.iloc[header_idx]
                df = df.iloc[header_idx + 1 :].reset_index(drop=True)
                # Check for x-sandbox
                has_sandbox = False
                for c in df.columns:
                    # check col values? No, columns are Name, Parent etc.
                    pass
                # Check Name column for x-sandbox...
                sandbox_rows = df[
                    df["Name"].astype(str).str.contains("x-sandbox", na=False)
                ]
                if not sandbox_rows.empty:
                    print("  -> CONTAINS x-sandbox rows!")
                    print(sandbox_rows[["Name", "Parent"]].to_string())
                else:
                    print("  -> No x-sandbox rows found.")
    except Exception as e:
        print(f"Error reading {f}: {e}")
