
import pandas as pd
import os

def inspect_excel():
    index_path = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP/$index.xlsx"
    df = pd.read_excel(index_path, sheet_name="Schemas")
    df.columns = df.columns.astype(str).str.strip()
    
    # Filter for PartyType rows
    pt_rows = df[df['Name'].astype(str).str.contains("PartyType") | df['Parent'].astype(str).str.contains("PartyType")]
    
    cols = ['Name', 'Parent', 'Type', 'Schema Name\n(if Type = schema)', 'Mandatory']
    # Clean column names in the list too
    clean_cols = [c.replace('\n', ' ').strip() for c in cols]
    df.columns = [c.replace('\n', ' ').strip() for c in df.columns]
    
    print("\n--- Focused PartyType Data ---")
    print(pt_rows[clean_cols])

if __name__ == "__main__":
    inspect_excel()
