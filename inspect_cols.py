
import pandas as pd
import os
import glob

def inspect_columns():
    target_files = glob.glob("API Templates/$index.xlsm")
    
    for path in target_files:
        print(f"--- Checking {os.path.basename(path)} ---")
        try:
            xl = pd.ExcelFile(path)
            for sheet in ["Schemas", "Paths", "Tags"]:
                if sheet in xl.sheet_names:
                    df = pd.read_excel(path, sheet_name=sheet, header=None)
                    print(f"\n[Sheet: {sheet}]")
                    print(df.head(5).to_string())
                    
                    # Try to find header
                    for idx, row in df.iterrows():
                         s = row.astype(str).str.cat()
                         if "Name" in s and "Type" in s:
                              print(f"Header likely at row {idx}")
                              print(row.tolist())
                              break
                
        except Exception as e:
            print(f"Error reading {path}: {e}")

if __name__ == "__main__":
    inspect_columns()
