
import pandas as pd
import os

def inspect_converted_output():
    index_path = "Output Legacy/$index.xlsx"
    
    if not os.path.exists(index_path):
        print(f"ERROR: {index_path} not found")
        return
    
    xl = pd.ExcelFile(index_path)
    print(f"Sheets in converted index: {xl.sheet_names}")
    
    # Check Schemas sheet
    if "Schemas" in xl.sheet_names:
        df_schemas = xl.parse("Schemas")
        print(f"\n=== Schemas sheet: {len(df_schemas)} rows ===")
        print(f"Columns: {df_schemas.columns.tolist()}")
        
        # Count hoisted vs standard schemas
        name_col = "Name" if "Name" in df_schemas.columns else df_schemas.columns[0]
        all_names = df_schemas[name_col].dropna().astype(str).unique()
        
        hoisted = [n for n in all_names if n.endswith(("Request", "Response")) and not n.startswith("Error")]
        standard = [n for n in all_names if not n.endswith(("Request", "Response"))]
        
        print(f"\nHoisted schemas ({len(hoisted)}):")
        for h in sorted(hoisted)[:10]:  # Show first 10
            print(f"  - {h}")
        if len(hoisted) > 10:
            print(f"  ... and {len(hoisted) - 10} more")
        
        print(f"\nStandard schemas ({len(standard)}):")
        for s in sorted(standard)[:10]:
            print(f"  - {s}")
        if len(standard) > 10:
            print(f"  ... and {len(standard) - 10} more")
        
        # Check for CGSSettlementBIC
        if "CGSSettlementBIC" in all_names:
            print("\n[PASS] CGSSettlementBIC found in Schemas sheet")
        else:
            print("\n[FAIL] CGSSettlementBIC NOT found in Schemas sheet")
        
        # Check for Operations
        if "Operations" in all_names:
            print("[PASS] Operations found in Schemas sheet")
            # Show its children
            parent_col = "Parent" if "Parent" in df_schemas.columns else df_schemas.columns[1]
            ops_children = df_schemas[df_schemas[parent_col].astype(str).str.lower() == "operations"]
            print(f"  Children under Operations: {len(ops_children)}")
        else:
            print("[FAIL] Operations NOT found in Schemas sheet")
    else:
        print("ERROR: 'Schemas' sheet not found")

if __name__ == "__main__":
    inspect_converted_output()
