import pandas as pd
import os

base_dir = r"C:\Users\giuse\.gemini\antigravity\scratch\OAS_Generation_Tool\API Templates"
index_path = os.path.join(base_dir, "$index.xlsm")

def inspect_master_schemas():
    print(f"Inspecting 'Schemas' sheet in {index_path}")
    try:
        df = pd.read_excel(index_path, sheet_name="Schemas")
        print("ALL COLUMNS:", df.columns.tolist())
        
        # Filter for Message or ModelItem
        target_rows = df[df['Name'].isin(['Message', 'ModelItem'])]
        if not target_rows.empty:
            print("\n--- Target Rows ---")
            print(target_rows.T.to_string())
            
        # Check for child rows of Message/ModelItem to see properties
        # Assuming Parent column exists
        if 'Parent' in df.columns:
            children = df[df['Parent'].isin(['Message', 'ModelItem'])]
            if not children.empty:
                print("\n--- Children Rows ---")
                print(children.head(10).T.to_string())
                
    except Exception as e:
        print(f"Error: {e}")

inspect_master_schemas()
