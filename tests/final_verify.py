
import pandas as pd
import os

print("--- INDEX VERIFICATION ---")
index_path = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Converted\$index.xlsx"
df_schemas = pd.read_excel(index_path, sheet_name="Schemas")
print(f"ErrorCode1 in index: {'ErrorCode1' in df_schemas['Name'].values}")
ec = df_schemas[df_schemas['Name'].str.startswith('ErrorCode', na=False)]
print("ErrorCode variants found:")
print(ec[['Name', 'Example']])

print("\n--- OPERATION VERIFICATION (listAlerts) ---")
op_path = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Converted\listAlerts.211207.xlsx"
df_body = pd.read_excel(op_path, sheet_name="Body", header=1)
sc = df_body[df_body['Name'] == 'searchCriteria']
print("searchCriteria mapping:")
print(sc[['Section', 'Name', 'Parent', 'Type', df_body.columns[6]]])

print("\n--- SECTION COLUMN VERIFICATION ---")
section_vals = df_body['Section'].dropna().unique()
print(f"Unique non-empty values in Section column: {section_vals}")
