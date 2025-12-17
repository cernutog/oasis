import pandas as pd
import os

base_dir = r"C:\Users\giuse\.gemini\antigravity\scratch\OAS_Generation_Tool\API Templates"
index_path = os.path.join(base_dir, "$index.xlsm")
bulk_op_path = os.path.join(base_dir, "account_assessment_vop_bulk_{bulkId}.251111.xlsm")

def inspect_files():
    print(f"--- Inspecting {index_path} Headers ---")
    try:
        df_h = pd.read_excel(index_path, sheet_name="Headers")
        print(df_h.head())
    except Exception as e:
        print(e)

    print(f"\n--- Inspecting {index_path} Responses ---")
    try:
        df_r = pd.read_excel(index_path, sheet_name="Responses")
        print(df_r.head())
    except Exception as e:
        print(e)
        
    print(f"\n--- Inspecting {bulk_op_path} Parameters ---")
    try:
        df_p = pd.read_excel(bulk_op_path, sheet_name="Parameters")
        print(df_p.head())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    inspect_files()
