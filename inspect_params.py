import pandas as pd
import os

base_dir = r"C:\Users\giuse\.gemini\antigravity\scratch\OAS_Generation_Tool\API Templates"
index_file = os.path.join(base_dir, "$index.xlsm")

try:
    df = pd.read_excel(index_file, sheet_name="Parameters")
    print(df.head(20))
    # Filter for fuid
    print("\n--- FUID ROW ---")
    print(df.columns)
    row = df[df['Name'] == 'fuid'].iloc[0]
    print(f"In: '{row['In']}'")
    print(f"Mandatory: '{row['Mandatory']}'")
except Exception as e:
    print(e)
