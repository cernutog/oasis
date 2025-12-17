
import pandas as pd
import os

file_path = "API Templates/$index.xlsm"
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    exit(1)

try:
    xl = pd.ExcelFile(file_path)
    print(f"Sheets in {file_path}: {xl.sheet_names}")
    
    if "Tags" in xl.sheet_names:
        print("\n--- 'Tags' Sheet Content ---")
        df = pd.read_excel(file_path, sheet_name="Tags")
        print(df)
        print("\nColumns:", df.columns.tolist())
    else:
        print("\n'Tags' sheet not found.")
        # Check if 'Tag' or similar exists
        for sheet in xl.sheet_names:
            if "tag" in sheet.lower():
                print(f"Maybe it's named: {sheet}?")
                
except Exception as e:
    print(f"Error: {e}")
