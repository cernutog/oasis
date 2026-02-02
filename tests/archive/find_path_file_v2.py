
import pandas as pd
import os

def find_path_file():
    index_path = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP/$index.xlsx"
    df = pd.read_excel(index_path, sheet_name="Paths")
    df.columns = df.columns.astype(str).str.strip()
    
    # Print columns to debug
    print(f"Columns in Paths: {list(df.columns)}")
    
    target_path = "/vop/v1/payee-information"
    # Find column that contains "Path" (case insensitive)
    path_col = [c for c in df.columns if 'path' in c.lower()][0]
    file_col = [c for c in df.columns if 'file' in c.lower()][0]
    
    row = df[df[path_col] == target_path]
    if not row.empty:
        print(f"\n--- Path: {target_path} ---")
        print(row[[path_col, file_col]])
    else:
        print(f"\nPath {target_path} not found.")

if __name__ == "__main__":
    find_path_file()
