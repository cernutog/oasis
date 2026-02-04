
import pandas as pd
import os

p = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Converted\$index.xlsx"
df = pd.read_excel(p, sheet_name="Schemas")
ec = df[df['Name'].str.startswith('ErrorCode', na=False)]

print("Comparing ErrorCode variants:")
for _, row in ec.iterrows():
    print(f"\n--- {row['Name']} ---")
    for col in df.columns:
        if col != 'Name':
            print(f"{col}: '{row[col]}'")

# Comparison
if len(ec) >= 2:
    row1 = ec.iloc[0]
    row2 = ec.iloc[1]
    diffs = []
    for col in df.columns:
        if col not in ['Name', 'Description', 'Parent']: # Description is allowed to differ
            val1 = str(row1[col]).strip()
            val2 = str(row2[col]).strip()
            if val1 != val2:
                diffs.append(f"Column '{col}': '{val1}' vs '{val2}'")
    
    if not diffs:
        print("\nIDENTICAL (except Name/Description/Parent)")
    else:
        print("\nDifferences found:")
        for d in diffs:
            print(f"  - {d}")
