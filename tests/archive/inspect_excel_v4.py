
import pandas as pd
import os

def inspect_excel():
    index_path = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP/$index.xlsx"
    df = pd.read_excel(index_path, sheet_name="Schemas")
    
    # Filter for PartyType rows
    pt_rows = df[df.apply(lambda row: row.astype(str).str.contains("PartyType").any(), axis=1)]
    
    print("\n--- Raw PartyType Rows (Selected Columns) ---")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    # Print all columns to be safe, but just for these rows
    print(pt_rows)

if __name__ == "__main__":
    inspect_excel()
