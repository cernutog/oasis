
import sys
import os
sys.path.append(os.getcwd())

from src.generator import OASGenerator
import pandas as pd

# Find the schema with title issue
base_dir = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP"
index_path = os.path.join(base_dir, "$index.xlsx")

df = pd.read_excel(index_path, sheet_name="Schemas")

# Search for rows with "title" in the name or as a child
title_rows = df[df.apply(lambda row: 'title' in str(row.get('Name', '')).lower(), axis=1)]

print("=== Rows containing 'title' ===")
for idx, row in title_rows.iterrows():
    name = row.get('Name', 'N/A')
    parent = row.get('Parent', 'N/A')
    row_type = row.get('Type', 'N/A')
    print(f"Row {idx}: Name='{name}', Parent='{parent}', Type='{row_type}'")

# Also check for VerificationOfPayeeResponse which seems to be the schema in the screenshot
vop_rows = df[df.apply(lambda row: 'VerificationOfPayeeResponse' in str(row.get('Name', '')), axis=1)]
print("\n=== VerificationOfPayeeResponse rows ===")
for idx, row in vop_rows.iterrows():
    name = row.get('Name', 'N/A')
    parent = row.get('Parent', 'N/A')
    row_type = row.get('Type', 'N/A')
    print(f"Row {idx}: Name='{name}', Parent='{parent}', Type='{row_type}'")
