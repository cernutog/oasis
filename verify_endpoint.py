import pandas as pd
import os
import glob
from datetime import datetime

# Find the generated file (with today's date)
current_date = datetime.now().strftime("%y%m%d")
gen_pattern = f"Imported Templates/create-account-assessment.{current_date}.xlsx"
ref_file = "API Templates/account_assessment.251111.xlsm"

gen_files = glob.glob(gen_pattern)
if not gen_files:
    print(f"Error: Generated file not found for pattern {gen_pattern}")
    exit(1)
    
gen_file = gen_files[0]
print(f"Comparing:")
print(f"  Generated: {gen_file}")
print(f"  Reference: {ref_file}")

# Compare Sheets
xl_gen = pd.ExcelFile(gen_file, engine='openpyxl')
xl_ref = pd.ExcelFile(ref_file, engine='openpyxl')

print(f"\nGenerated Sheets: {xl_gen.sheet_names}")
print(f"Reference Sheets: {xl_ref.sheet_names}")

# Compare Parameters Sheet
print("\n--- Parameters Sheet Comparison ---")
df_gen_p = pd.read_excel(gen_file, sheet_name='Parameters', engine='openpyxl')
df_ref_p = pd.read_excel(ref_file, sheet_name='Parameters', engine='openpyxl')

# Check structure
cols_gen = [c.strip() for c in df_gen_p.columns]
cols_ref = [c.strip() for c in df_ref_p.columns]
print(f"Columns match: {cols_gen == cols_ref}")
if cols_gen != cols_ref:
    print(f"  Gen: {cols_gen}")
    print(f"  Ref: {cols_ref}")

print(f"Rows match: {len(df_gen_p) == len(df_ref_p)}")
print(f"Gen Rows: {len(df_gen_p)}, Ref Rows: {len(df_ref_p)}")

# Compare 201 Sheet
print("\n--- 201 Sheet Comparison ---")
if '201' in xl_gen.sheet_names and '201' in xl_ref.sheet_names:
    df_gen_201 = pd.read_excel(gen_file, sheet_name='201', engine='openpyxl', header=1)
    df_ref_201 = pd.read_excel(ref_file, sheet_name='201', engine='openpyxl', header=1)
    
    # Header check (Reponse | 201 | Created)
    # Pandas reads header as columns usually. Let's check header names.
    print(f"Gen 201 Columns: {df_gen_201.columns.tolist()}")
    print(f"Ref 201 Columns: {df_ref_201.columns.tolist()}")
    
    print(f"Gen 201 Rows: {len(df_gen_201)}")
    print(df_gen_201[['Section', 'Name', 'Parent', 'Type']].to_string())
    
    print(f"\nRef 201 Rows: {len(df_ref_201)}")
    print(df_ref_201[['Section', 'Name', 'Parent', 'Type']].to_string())
else:
    print("Sheet 201 missing in one of the files.")

# Compare Body Sheet
print("\n--- Body Sheet Comparison ---")
# Use header=1 because Row 2 (index 1) is the header row for Body sheet
df_gen_b = pd.read_excel(gen_file, sheet_name='Body', engine='openpyxl', header=1)
df_ref_b = pd.read_excel(ref_file, sheet_name='Body', engine='openpyxl', header=1)

print("Gen Body Head:")
# Should see NO parent for top items
cols = [c for c in ['Section', 'Name', 'Parent'] if c in df_gen_b.columns]
print(df_gen_b[cols].head(5).to_string())
print("\nRef Body Head:")
print(df_ref_b[cols].head(5).to_string())

