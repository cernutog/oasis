import pandas as pd
import os

base_dir = r"C:\Users\giuse\.gemini\antigravity\scratch\OAS_Generation_Tool\API Templates"
# File for get-transaction-investigation-report
fname = "v1_transactions_investigations_reports.251111.xlsm"
fpath = os.path.join(base_dir, fname)

def inspect_response_sheet():
    print(f"Inspecting '409' sheet in {fname}")
    try:
        df = pd.read_excel(fpath, sheet_name="409", header=None) # Read raw first
        print("--- Raw First 10 Rows ---")
        print(df.head(10).to_string())
        
        # Try finding header
        print("\n--- Columns if header=0 ---")
        df0 = pd.read_excel(fpath, sheet_name="409")
        print(df0.columns.tolist())
    except Exception as e:
        print(f"Error: {e}")

inspect_response_sheet()
