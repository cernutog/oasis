"""
Check what DataTypes are defined in the legacy template and if NetworkFileName exists
"""
import sys
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

INPUT_DIR = ROOT / "Templates Legacy"
legacy_path = INPUT_DIR / "retransmitOutFiles.210702.xlsm"

if legacy_path.exists():
    print(f"\n=== DataTypes sheet in {legacy_path.name} ===")
    try:
        # Read the DataTypes sheet
        df = pd.read_excel(legacy_path, sheet_name="Data Type", header=None, dtype=str)
        
        # Find header row
        header_row_idx = -1
        for idx, row in df.head(10).iterrows():
            row_str = row.astype(str).str.lower()
            header_keywords = ["name", "type", "format", "mandatory", "required"]
            matches = sum(1 for keyword in header_keywords if keyword in row_str.values)
            if matches >= 2:
                header_row_idx = idx
                break
        
        if header_row_idx != -1:
            df = pd.read_excel(legacy_path, sheet_name="Data Type", header=header_row_idx, dtype=str)
            print(f"Found header at row {header_row_idx + 1}")
            print(f"Columns: {list(df.columns)}")
            
            # Look for NetworkFileName
            network_rows = df[df.iloc[:, 0].str.contains("NetworkFileName", na=False, case=False)]
            if not network_rows.empty:
                print(f"\n--- NetworkFileName entries ---")
                for idx, row in network_rows.iterrows():
                    print(f"Row {idx+1}: {dict(row)}")
            else:
                print("\n--- No NetworkFileName found ---")
                
            # Show all type names for reference
            print(f"\n--- All DataType names (first 10) ---")
            for idx, row in df.head(10).iterrows():
                name = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
                if name and name.lower() != "nan":
                    print(f"  {name}")
        else:
            print("Could not find header row in DataTypes sheet")
            
    except Exception as e:
        print(f"Error reading DataTypes sheet: {e}")
else:
    print(f"File not found: {legacy_path}")
