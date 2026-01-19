import pandas as pd

df = pd.read_excel(r'C:\Users\giuse\.gemini\antigravity\scratch\OASIS\Imported Templates\$index.xlsx', sheet_name='Schemas')

rows = df[df['Name'].astype(str).str.contains('InsightNotification', na=False)]

print(f'Found {len(rows)} rows containing InsightNotification\n')

for idx, row in rows.iterrows():
    name = row['Name']
    parent = row.get('Parent', '')
    row_type = row.get('Type', '')
    desc = str(row.get('Description', ''))[:60]
    
    print(f"Row {idx}:")
    print(f"  Name: {name}")
    print(f"  Parent: {parent}")
    print(f"  Type: {row_type}")
    print(f"  Description: {desc}...")
    print()
