"""Check RiskInfoArray in Excel."""
import pandas as pd
import os

df = pd.read_excel(os.path.join('Roundtrip_Templates', '$index.xlsx'), sheet_name='Schemas', header=0)

# Find RiskInfoArray related rows
rows = df[(df['Name'] == 'RiskInfoArray') | (df['Parent'] == 'RiskInfoArray')]
print('RiskInfoArray rows in Excel:')
for idx, row in rows.iterrows():
    print(f"  Row {idx}: Name={row['Name']}, Parent={row['Parent']}, Type={row['Type']}")
