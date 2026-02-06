
import pandas as pd
import os

def inspect_converted_schemas():
    path = "Templates Converted V3/$index.xlsx"
    if not os.path.exists(path):
        print(f"Error: {path} not found")
        return
    
    df = pd.read_excel(path, "Schemas")
    print(f"--- Schemas in {path} ---")
    # Show first 50 schema names
    print(df.iloc[:, 0].dropna().unique().tolist())

if __name__ == "__main__":
    inspect_converted_schemas()
