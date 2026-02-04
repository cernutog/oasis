
import pandas as pd
import os

def dump_200():
    f = "Templates Legacy/operationDetails.230216.xlsm"
    xl = pd.ExcelFile(f)
    if "200" in xl.sheet_names:
        df = xl.parse("200")
        print(f"--- 200 sheet dump (rows 10-30) for {f} ---")
        print(df.iloc[10:30, [0,1,2,3,4]].to_string())
    else:
        print(f"Sheet '200' not found in {f}")

if __name__ == "__main__":
    dump_200()
