
import pandas as pd
import os

target_file = "API Templates/account_assessment.251111.xlsm"
sheet_name = "201"

print(f"Loading '{sheet_name}' from {target_file}...")
try:
    # Load raw with no header to see top rows
    df = pd.read_excel(target_file, sheet_name=sheet_name, header=None)
    print("\n--- DataFrame Head (First 5 Rows) ---")
    print(df.head(5).to_string())
    
    # Check C1 specifically (Row 0, Col 2)
    c1_val = df.iloc[0, 2] if df.shape[1] > 2 else "N/A"
    print(f"\nValue at C1 (Row 0, Col 2): {c1_val}")
    
except Exception as e:
    print(f"Error: {e}")
