import pandas as pd
import os

legacy_index = r"Templates Legacy\$index.xlsm"
if os.path.exists(legacy_index):
    xl = pd.ExcelFile(legacy_index)
    print("Sheets:", xl.sheet_names)
    if "Paths" in xl.sheet_names:
        df = pd.read_excel(xl, "Paths")
        print("Paths Columns:", df.columns.tolist())
        print("First 5 rows of Paths:\n", df.head(5))
else:
    print("Legacy index not found at:", os.path.abspath(legacy_index))
