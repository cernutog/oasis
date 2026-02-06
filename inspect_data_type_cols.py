
import pandas as pd
import os

path = r'Templates Legacy/listAlerts.211207.xlsm'
xl = pd.ExcelFile(path)
df = pd.read_excel(xl, "Data Type", header=None, dtype=str)
# Print columns 0, 1, 2 for the first 10 rows
print(df.iloc[:10, [0, 1, 2]])
