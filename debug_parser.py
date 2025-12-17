import pandas as pd
from src import parser
import os

base_dir = "API Templates"
target_file = "account_assessment_vop.251111.xlsm"
full_path = os.path.join(base_dir, target_file)

print(f"Loading {full_path}...")
df_body = parser.load_excel_sheet(full_path, "Body")

if df_body is not None:
    print("Columns found:")
    print(df_body.columns.tolist())
    print("\nFirst row:")
    print(df_body.iloc[0])
else:
    print("Body sheet not found or error.")

print("-" * 20)
print("Loading 201...")
df_201 = parser.load_excel_sheet(full_path, "201")
if df_201 is not None:
    print("Columns 201:")
    print(df_201.columns.tolist())
else:
    print("201 not found.")
