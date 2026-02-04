
import pandas as pd
import yaml
import os
import re

# Paths
LEGACY_INDEX = r'Templates Legacy/$index.xlsm'.replace('/', os.sep)
LEGACY_DIR = r'Templates Legacy'.replace('/', os.sep)
YAML_PATH = r"C:\Users\giuse\Downloads\EBACL_STEP2_20250507_Openapi3.1_CGS-DKK_API_Participants_2_0_v20251006.yaml"

def analyze():
    print("--- Unified Analysis ---")
    
    # 1. Check Operations structure in YAML vs Excel
    print("\n[1] Operations Structural Check:")
    if os.path.exists(YAML_PATH):
        with open(YAML_PATH, 'r', encoding='utf-8') as f:
            spec = yaml.safe_load(f)
            ops_yaml = spec.get('components', {}).get('schemas', {}).get('Operations')
            print(f"YAML Operations Type: {ops_yaml.get('type') if ops_yaml else 'NOT FOUND'}")
            if ops_yaml and 'properties' in ops_yaml:
                print(f"YAML Operations Properties: {list(ops_yaml['properties'].keys())}")
    
    list_op_path = os.path.join(LEGACY_DIR, "listOperation.230216.xlsm")
    if os.path.exists(list_op_path):
        df_dt = pd.read_excel(list_op_path, sheet_name='Data Type', header=None)
        # Search for 'Operations' in Col 0 (PascalCase or otherwise)
        mask = df_dt.iloc[:, 0].astype(str).str.strip().str.lower() == 'operations'
        ops_row = df_dt[mask]
        if not ops_row.empty:
             row_data = ops_row.iloc[0].values
             print(f"Excel Operations Definition (Row {ops_row.index[0]}):")
             print(f"  Col 0: {row_data[0]}")
             print(f"  Col 2 (Type): {row_data[2]}")
             print(f"  Col 4 (Parent?): {row_data[4]}")
        
        # Check if there are other fields with Parent = 'Operations'
        children = df_dt[df_dt.iloc[:, 2].astype(str).str.strip().str.lower() == 'operations']
        if not children.empty:
            print("Fields with Parent=Operations (in Data Type sheet):")
            print(children.iloc[:, [0, 2]].to_string())

    # 2. Check 200 Response structure for listOperation
    print("\n[2] listOperation 200 Response Check:")
    if os.path.exists(list_op_path):
        try:
            df_200 = pd.read_excel(list_op_path, sheet_name='200', header=None)
            print("Excel listOperation 200 First Rows:")
            print(df_200.head(15).iloc[:, 0:7].to_string())
        except Exception as e:
             print(f"Error reading 200 sheet: {e}")

    # 3. Check liquidityManagement row in Index
    print("\n[3] liquidityManagement Index Row:")
    if os.path.exists(LEGACY_INDEX):
        try:
            df_p = pd.read_excel(LEGACY_INDEX, sheet_name='Paths', header=1)
            # Find row for liquidityManagement
            row = df_p[df_p.iloc[:, 0].astype(str).str.contains('liquidityManagement', na=False)]
            if not row.empty:
                print("Index Row for liquidityManagement:")
                # Show Excel File and OperationId
                print(row[['Excel file', 'OperationId']].to_string())
        except Exception as e:
            print(f"Error reading Index: {e}")

if __name__ == "__main__":
    analyze()
