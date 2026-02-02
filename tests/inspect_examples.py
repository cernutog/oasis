
import pandas as pd
import os

def inspect_examples():
    index_path = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP/$index.xlsx"
    df = pd.read_excel(index_path, sheet_name="Schemas")
    df.columns = df.columns.astype(str).str.strip()
    
    # Filter for PartyType rows
    pt_rows = df[df.apply(lambda row: row.astype(str).str.contains("PartyType").any(), axis=1)]
    
    print("\n--- Examples for PartyType Data ---")
    cols = ['Name', 'Parent', 'Type', 'Example']
    # Filter columns that exist
    actual_cols = [c for c in df.columns if any(x in c for x in cols)]
    
    # Let's just print Name, Parent, Type and whatever column looks like Example
    example_col = [c for c in df.columns if 'Example' in c][0]
    
    for _, row in pt_rows.iterrows():
        print(f"Name: {row['Name']} | Parent: {row['Parent']} | Type: {row['Type']} | Example: {row[example_col]}")

if __name__ == "__main__":
    inspect_examples()
