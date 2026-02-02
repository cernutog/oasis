
import pandas as pd
import os

def inspect_excel():
    index_path = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP/$index.xlsx"
    xl = pd.ExcelFile(index_path)
    df = pd.read_excel(xl, sheet_name="Schemas")
    
    # Clean column names
    df.columns = df.columns.astype(str).str.strip()
    
    party_rows = df[df.apply(lambda row: row.astype(str).str.contains("PartyType").any(), axis=1)]
    print("\n--- Detailed PartyType Data ---")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(party_rows)

if __name__ == "__main__":
    inspect_excel()
