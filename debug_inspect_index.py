import pandas as pd
from pathlib import Path
import os

index_path = Path(r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy\$index.xlsm")

def find_header_row(df, keywords):
    for i, row in df.iterrows():
        row_vals = [str(x).lower() for x in row if pd.notna(x)]
        if all(any(k in v for v in row_vals) for k in keywords):
            return i
    return -1

if not index_path.exists():
    print(f"Index not found at {index_path}")
else:
    try:
        xl = pd.ExcelFile(index_path)
        print(f"Sheets: {xl.sheet_names}")
        if "Paths" in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name="Paths", dtype=str, header=None)
            hr = find_header_row(df, ["excel file", "operationid"])
            print(f"Header row found at: {hr}")
            if hr != -1:
                header_vals = [str(c).strip().lower() for c in df.iloc[hr]]
                print(f"Headers: {header_vals}")
                df.columns = header_vals
                df = df.iloc[hr + 1:].reset_index(drop=True)
                
                print("\nFirst 10 rows:")
                print(df.head(10))
                
                file_col = next((c for c in df.columns if "excel file" in c or "file" in c), None)
                if file_col:
                    files = df[file_col].dropna().tolist()
                    print(f"\nTotal files in index: {len(files)}")
                    print(f"Order: {files[:5]} ...")
                else:
                    print("File column not found!")
    except Exception as e:
        print(f"Error: {e}")
