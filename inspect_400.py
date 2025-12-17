import pandas as pd
import os
import glob

base_dir = r"C:\Users\giuse\.gemini\antigravity\scratch\OAS_Generation_Tool\API Templates"
op_file = os.path.join(base_dir, "account_assessment.251111.xlsm")

def inspect_400():
    try:
        df = pd.read_excel(op_file, sheet_name="400")
        print(df[["Name", "Schema Name", "Parent"]].head())
    except Exception as e:
        print(f"Error reading 400: {e}")
        try:
             df = pd.read_excel(op_file, sheet_name="400")
             print(df.iloc[:5])
        except: pass

if __name__ == "__main__":
    inspect_400()
