
import pandas as pd
import os

targets = ["PartyTime", "FpadResponseIdentifier"]

print("--- Searching Definitions ---")
dir_path = "API Templates"
for f in os.listdir(dir_path):
    if f.endswith(".xlsx") or f.endswith(".xlsm"):
        path = os.path.join(dir_path, f)
        try:
            xl = pd.ExcelFile(path)
            for s in xl.sheet_names:
                df = pd.read_excel(path, sheet_name=s)
                # Assume Name is 2nd col (index 1) or 'Field Name'/'Name'
                # Let's check first few cols
                cols_to_check = df.columns[:3]
                
                for t in targets:
                     for col in cols_to_check:
                         # Exact match in Name column often has spaces?
                         # Let's try contains
                         matches = df[df[col].astype(str).str.strip() == t]
                         if not matches.empty:
                             print(f"FOUND DEFINITION '{t}' in {f} [Sheet: {s}]")
                             print(matches.iloc[0].to_string())
        except: pass

print("\n--- YAML Context 391 ---")
with open("API Templates/generated/generated_oas_3.1.yaml", "r") as f:
    lines = f.readlines()
    start = max(0, 380)
    end = min(len(lines), 410)
    for i in range(start, end):
        print(f"{i+1}: {lines[i].rstrip()}")
