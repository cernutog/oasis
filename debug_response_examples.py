
import pandas as pd

target_file = "API Templates/account_assessment.251111.xlsm"
sheet_name = "201"

print(f"Loading '{sheet_name}' from {target_file}...")
try:
    # Load all rows
    df = pd.read_excel(target_file, sheet_name=sheet_name)
    
    # Filter for Section == 'examples' or rows around 8-15
    print("\n--- Rows 8 to 20 ---")
    print(df.iloc[6:20].to_string())
    
except Exception as e:
    print(f"Error: {e}")
