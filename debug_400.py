
import pandas as pd

target_file = "API Templates/account_assessment.251111.xlsm"
sheet_name = "400"

print(f"Loading '{sheet_name}' from {target_file}...")
try:
    df = pd.read_excel(target_file, sheet_name=sheet_name)
    print("\n--- All Rows ---")
    print(df.to_string())
except Exception as e:
    print(f"Error: {e}")
