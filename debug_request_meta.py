
import pandas as pd
from src.parser import load_excel_sheet

# Inspecting Account Assessment file as representative example
target_file = "API Templates/account_assessment.251111.xlsm"
sheet_name = "Body"

print(f"Loading {sheet_name} from {target_file}...")
try:
    # Use load_excel_sheet logic: read raw first
    df_raw = pd.read_excel(target_file, sheet_name=sheet_name, header=None)
    
    print("\n--- Raw DataFrame Head (first 5 rows) ---")
    print(df_raw.head().to_string())
    
    # Check Coordinates
    try:
        b1_val = df_raw.iloc[0, 1] # Row 0, Col 1 => B1
        c1_val = df_raw.iloc[0, 2] # Row 0, Col 2 => C1
        
        print(f"\n[B1] Description Candidate: '{b1_val}' (Type: {type(b1_val)})")
        print(f"[C1] Required Candidate: '{c1_val}' (Type: {type(c1_val)})")
        
        # Check logic:
        # Description
        desc = str(b1_val).strip() if pd.notna(b1_val) else None
        print(f"Parsed Description: {desc}")
        
        # Required
        req_flag = str(c1_val).strip().upper() if pd.notna(c1_val) else ""
        is_required = (req_flag == "M")
        print(f"Parsed Required (C1=='M'): {is_required} (Flag: '{req_flag}')")

    except IndexError:
        print("Error: Sheet is too small to contain B1/C1.")
        
except Exception as e:
    print(f"Error: {e}")
