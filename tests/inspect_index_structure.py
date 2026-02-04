
import pandas as pd
import os

p = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy\$index.xlsm"
xl = pd.ExcelFile(p)
s = next((s for s in xl.sheet_names if "path" in s.lower()), None)
print(f"Sheet name: {s}")
df = pd.read_excel(xl, sheet_name=s, header=None)
print("First 10 rows:")
print(df.head(10))
xl.close()
