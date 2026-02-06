
import pandas as pd
import os

path = r'Templates Legacy/$index.xlsm'
if os.path.exists(path):
    xl = pd.ExcelFile(path)
    print(f"Sheets in {path}:")
    print(xl.sheet_names)
else:
    print(f"File not found: {path}")
