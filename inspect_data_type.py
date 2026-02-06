
import pandas as pd
import os

path = r'Templates Legacy/listAlerts.211207.xlsm'
xl = pd.ExcelFile(path)
df = pd.read_excel(xl, "Data Type", header=None, dtype=str)
print(df.head(10))
