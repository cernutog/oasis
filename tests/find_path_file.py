
import pandas as pd
import os

def find_path_file():
    index_path = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP/$index.xlsx"
    df = pd.read_excel(index_path, sheet_name="Paths")
    df.columns = df.columns.astype(str).str.strip()
    
    target_path = "/vop/v1/payee-information"
    row = df[df['Path'] == target_path]
    if not row.empty:
        print(f"\n--- Path: {target_path} ---")
        print(row[['Path', 'Method', 'File']])
    else:
        print(f"\nPath {target_path} not found.")

if __name__ == "__main__":
    find_path_file()
