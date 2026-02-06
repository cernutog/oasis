
import pandas as pd
import os

def inspect_master():
    master_dir = "Templates Master"
    
    # 1. Index
    index_path = os.path.join(master_dir, "$index.xlsx")
    xl_index = pd.ExcelFile(index_path)
    print(f"\nSheets in Master $index: {xl_index.sheet_names}")
    if "Schemas" in xl_index.sheet_names:
        df = pd.read_excel(xl_index, "Schemas")
        print(f"Schemas Headers: {list(df.columns)}")
    if "Paths" in xl_index.sheet_names:
        df = pd.read_excel(xl_index, "Paths")
        print(f"Paths Headers: {list(df.columns)}")

    # 2. Endpoint
    endpoint_path = os.path.join(master_dir, "endpoint.xlsx")
    xl_end = pd.ExcelFile(endpoint_path)
    print(f"\nSheets in Master endpoint: {xl_end.sheet_names}")
    for s in ["Body", "Responses"]:
        if s in xl_end.sheet_names:
            df = pd.read_excel(xl_end, s)
            print(f"{s} Headers: {list(df.columns)}")

if __name__ == "__main__":
    inspect_master()
