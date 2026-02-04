
import pandas as pd
import os

p = r'Templates Legacy/$index.xlsm'
if not os.path.exists(p):
    p = p.replace('/', '\\')

try:
    xl = pd.ExcelFile(p)
    sheet_name = next((s for s in xl.sheet_names if 'path' in s.lower()), 'Paths')
    df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
    for idx, row in df.iterrows():
        row_str = row.astype(str).str.lower()
        if any('liquidity' in v for v in row_str.values):
            print(f"Row {idx}: {row.to_list()}")
    xl.close()
except Exception as e:
    print(f"Error: {e}")
