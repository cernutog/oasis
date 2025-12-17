import pandas as pd
import os

file_path = r"C:\Users\giuse\.gemini\antigravity\scratch\OAS_Generation_Tool\API Templates\$index.xlsm"

def inspect():
    try:
        print("--- RESPONSES ---")
        df_resp = pd.read_excel(file_path, sheet_name="Responses")
        print(df_resp[["Name"]].to_string())
        
        print("\n--- HEADERS ---")
        df_head = pd.read_excel(file_path, sheet_name="Headers")
        print(df_head.iloc[0:2]) # Print first 2 rows
        
        print("\n--- SCHEMAS ---")
        df_sch = pd.read_excel(file_path, sheet_name="Schemas")
        if "ErrorResponse" in df_sch["Name"].values:
            print("ErrorResponse schema FOUND.")
        else:
            print("ErrorResponse schema NOT FOUND.")
            
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    inspect()
