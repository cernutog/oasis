
import pandas as pd
import os

p = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Converted\liquidityManagement.250808.xlsx"
df = pd.read_excel(p, sheet_name="Body", header=1) # Row 2 is headers
print("Converted Body Sheet (Top 5 rows):")
cols_to_show = ["Section", "Name", "Parent", "Type", "Schema Name\n(for Type or Items Data Type = 'schema'||'header')", "Max  \nValue/Length/Item"]
print(df[cols_to_show].head(10).to_string())
