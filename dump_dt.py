
import pandas as pd
import os

def dump_dt():
    f = "Templates Legacy/operationDetails.230216.xlsm"
    xl = pd.ExcelFile(f)
    if "Data Type" in xl.sheet_names:
        df = xl.parse("Data Type")
        print(f"--- Data Type dump for {f} ---")
        print(df.head(50).to_string())
    else:
        print(f"Sheet 'Data Type' not found in {f}")

if __name__ == "__main__":
    dump_dt()
