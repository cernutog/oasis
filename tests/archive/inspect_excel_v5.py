
import pandas as pd
import os

def inspect_excel():
    index_path = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP/$index.xlsx"
    df = pd.read_excel(index_path, sheet_name="Schemas")
    
    # Filter for PartyType rows
    pt_rows = df[df.apply(lambda row: row.astype(str).str.contains("PartyType").any(), axis=1)]
    
    print("\n--- NON-TRUNCATED PartyType Data ---")
    rows_list = pt_rows.to_dict('records')
    for r in rows_list:
        print("-" * 20)
        for k, v in r.items():
            if pd.notna(v):
                print(f"{k}: {v}")

if __name__ == "__main__":
    inspect_excel()
