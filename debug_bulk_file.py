import pandas as pd
import os

file_path = r"C:\Users\giuse\.gemini\antigravity\scratch\OAS_Generation_Tool\API Templates\account_assessment_vop_bulk_{bulkId}.251111.xlsm"

def debug_bulk():
    try:
        print("--- SHEET 400 ---")
        df_raw = pd.read_excel(file_path, sheet_name="400", header=None)
        header_idx = -1
        for idx, row in df_raw.head(10).iterrows():
             if "Name" in row.values:
                  header_idx = idx
                  break
        
        if header_idx != -1:
             df_400 = pd.read_excel(file_path, sheet_name="400", header=header_idx)
             # Find Schema Name col
             cols = [c for c in df_400.columns if "Schema Name" in str(c)]
             if cols:
                 schema_col = cols[0]
                 print(f"Schema Column: {schema_col}")
                 print(df_400[["Name", schema_col, "Type"]].head(5).to_string())
             else:
                 print("Schema Name column not found.")
        else:
             print("Could not find header row in 400.")

        print("\n--- SHEET PARAMETERS ---")
        # Try finding the right sheet name
        xl = pd.ExcelFile(file_path)
        print(f"Sheets: {xl.sheet_names}")
        if "Parameters" in xl.sheet_names:
            df_params = pd.read_excel(file_path, sheet_name="Parameters")
            print(df_params.columns.tolist())
            print(df_params[["Name", "In", "Mandatory"]].to_string())
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_bulk()
