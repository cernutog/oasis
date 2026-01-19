import pandas as pd
from datetime import datetime

index_file = "Imported Templates/$index.xlsx"
current_date = datetime.now().strftime("%y%m%d")

print(f"Checking {index_file} for date {current_date}...")
df = pd.read_excel(index_file, sheet_name='Paths', engine='openpyxl')

# Print first few rows of Paths sheet
# Standard layout: File | Path | Method | ...
# We need to find the 'Excel File' column.
print("\nColumns:", df.columns.tolist())
print(df.head(5).to_string())

# Check for date in first filename
found = False
for col in df.columns:
    if "Excel" in str(col) or "File" in str(col) or "Filename" in str(col):
        first_val = str(df.iloc[0][col])
        print(f"\nFirst Filename: {first_val}")
        if current_date in first_val:
            found = True
            print("SUCCESS: Date found in filename.")
        else:
             print("FAILURE: Date NOT found in filename.")
        break

if not found:
    print("\nCould not identify Filename column or date missing.")
