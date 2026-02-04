
import pandas as pd

# Directly read the Excel to see exact content
xl = pd.ExcelFile("Output Legacy/$index.xlsx")
df = xl.parse("Schemas")

# Find rows where Name contains "Operations" or Parent contains "Operations"
name_col = "Name"
parent_col = "Parent"
type_col = "Type"

print("=== All rows with Operations (Name or Parent) ===")
mask = (df[name_col].astype(str).str.contains("Operations", case=False, na=False) | 
        df[parent_col].astype(str).str.contains("Operations", case=False, na=False))

relevant = df[mask][[name_col, parent_col, type_col, "Schema Name\n(if Type = schema)"]]
print(relevant.to_string())

print(f"\nTotal matching rows: {len(relevant)}")
