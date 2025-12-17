
import pandas as pd
from src.parser import load_excel_sheet

# We need to find the file for /v1/accounts/assessments
# Based on previous logs: account_assessment.251111.xlsm

file_path = "API Templates/account_assessment.251111.xlsm"
sheet_name = "Body" # Or "Request Body"? Or "Operation"?
# Wait, description is usually in "Operation" meta?
# Let's try to parse paths index first to find the file and meta.

index_path = "API Templates/$index.xlsm"
df_paths = load_excel_sheet(index_path, "Paths")
target_path = "/v1/accounts/assessments"

found_row = None
for idx, row in df_paths.iterrows():
    if row.get("Path") == target_path and row.get("Method", "").lower() == "post":
        found_row = row
        break

if found_row is not None:
    print("Found Path Meta:")
    print(found_row)
    
    desc = found_row.get("Description")
    print("\n--- Raw Description from DataFrame ---")
    print(f"Type: {type(desc)}")
    print(f"Repr: {repr(desc)}")
    if isinstance(desc, str):
        print(f"Has \\n? {'\\n' in desc}")
else:
    print("Path not found in index.")
