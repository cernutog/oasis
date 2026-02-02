
import pandas as pd
import os

def inspect_excel():
    index_path = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP/$index.xlsx"
    if not os.path.exists(index_path):
        print("Index not found.")
        return

    print(f"Reading {index_path}...")
    xl = pd.ExcelFile(index_path)
    for sheet in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=sheet)
        # Search for PartyType in any column
        matches = df.apply(lambda row: row.astype(str).str.contains("PartyType").any(), axis=1)
        if matches.any():
            print(f"\n--- FOUND PartyType in Sheet: {sheet} ---")
            print(df[matches])
            # Let's see the columns to understand the structure
            print(f"Columns: {list(df.columns)}")

if __name__ == "__main__":
    inspect_excel()
