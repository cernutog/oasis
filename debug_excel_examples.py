
import pandas as pd

target_file = "API Templates/account_assessment.251111.xlsm"
sheet_name = "Body Example"

print(f"Loading '{sheet_name}' from {target_file}...")
try:
    df = pd.read_excel(target_file, sheet_name=sheet_name)
    print("\n--- DataFrame Head ---")
    print(df.to_string())
    print("\n--- Columns ---")
    print(df.columns.tolist())
    
    # Check first row values
    if not df.empty:
        print("\n--- First Row Values ---")
        for col in df.columns:
            val = df.iloc[0][col]
            print(f"{col}: {repr(val)}")

except Exception as e:
    print(f"Error: {e}")
