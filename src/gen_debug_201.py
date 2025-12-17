import pandas as pd
import glob
import os

files = glob.glob("API Templates/*account_assessment.251111.xlsm")
if not files:
    print("File not found")
else:
    f = files[0]
    print(f"Reading {f}")
    df = pd.read_excel(f, sheet_name="201", header=None)
    # Print first 20 rows
    print(df.head(20).to_string())
