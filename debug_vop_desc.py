
import pandas as pd
from src.parser import load_excel_sheet

# Inspecting description for /v1/accounts/assessments/vop
index_path = "API Templates/$index.xlsm"
df_paths = load_excel_sheet(index_path, "Paths")
target_path = "/v1/accounts/assessments/vop"

found_row = None
for idx, row in df_paths.iterrows():
    if row.get("Path") == target_path and row.get("Method", "").lower() == "post":
        found_row = row
        break

if found_row is not None:
    desc = found_row.get("Description")
    print(f"\n--- Description for {target_path} ---")
    print(f"Type: {type(desc)}")
    print(f"Repr: {repr(desc)}")
    
    if isinstance(desc, str):
        print(f"Has \\n? {'\\n' in desc}")
        # Check for trailing spaces
        lines = desc.split('\n')
        for i, line in enumerate(lines):
            print(f"Line {i} length: {len(line)}, Trailing space? {line.endswith(' ')}")
else:
    print("Path not found.")
