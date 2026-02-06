
import pandas as pd
import os

def check_index_row_12():
    index_path = r"Templates Legacy/$index.xlsm"
    if not os.path.exists(index_path):
        print(f"Error: {index_path} not found")
        return
        
    xl = pd.ExcelFile(index_path)
    if "Paths" in xl.sheet_names:
        df = pd.read_excel(index_path, sheet_name="Paths").astype(str)
        if len(df) > 12:
            print("Row 12 content:")
            print(df.iloc[12])
        else:
            print(f"Index has only {len(df)} rows.")
    else:
        print("Paths sheet not found in index.xlsm")

if __name__ == "__main__":
    check_index_row_12()
