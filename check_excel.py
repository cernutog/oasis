"""Check raw Excel content."""
import pandas as pd
import os

path = os.path.join('Imported Templates', '$index.xlsx')
print(f"Path: {path}")
print(f"Exists: {os.path.exists(path)}")

df = pd.read_excel(path, sheet_name='Schemas', header=0)
print(f"\nColumns: {df.columns.tolist()[:6]}")
print()

# Find debtorBic
for idx, row in df.iterrows():
    if row.iloc[0] == 'debtorBic':
        print(f'Row {idx}:')
        print(f'  Name: {row.iloc[0]}')
        print(f'  Parent: {row.iloc[1]}')
        print(f'  Description: {row.iloc[2]}')
        print(f'  Type: {row.iloc[3]}')
        print()
