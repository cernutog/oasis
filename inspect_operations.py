
import pandas as pd

def inspect_operations():
    index_path = "Output Legacy/$index.xlsx"
    xl = pd.ExcelFile(index_path)
    df = xl.parse("Schemas")
    
    # Find Operations row
    name_col = "Name"
    parent_col = "Parent"
    type_col = "Type"
    items_col = "Items Data Type \n(Array only)"
    
    ops_row = df[df[name_col] == "Operations"]
    print("=== Operations schema definition ===")
    print(ops_row[[name_col, parent_col, type_col, items_col]].to_string())
    
    # Find children
    children = df[df[parent_col].astype(str).str.strip().str.lower() == "operations"]
    print(f"\n=== Children of Operations ({len(children)} rows) ===")
    print(children[[name_col, parent_col, type_col]].to_string())

if __name__ == "__main__":
    inspect_operations()
