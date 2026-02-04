
import os
import pandas as pd

def diagnose():
    legacy_dir = "Templates Legacy"
    target = "CGSSettlementBIC"
    found = False
    
    print(f"Searching for definition of '{target}' in {legacy_dir}...")
    for f in os.listdir(legacy_dir):
        if not f.endswith(".xlsm") or f == "$index.xlsm":
            continue
        
        try:
            xl = pd.ExcelFile(os.path.join(legacy_dir, f))
            if "Data Type" in xl.sheet_names:
                df = xl.parse("Data Type")
                # Look for target in column 0 (Technical Name/Parent) or column 2 (Element Name)
                mask = df.astype(str).apply(lambda x: x.str.contains(target, case=False, na=False)).any(axis=1)
                if mask.any():
                    print(f"--- MATCH in {f} ---")
                    print(df[mask].iloc[:, [0, 1, 2, 3]]) # Print relevant columns
                    found = True
        except Exception as e:
            print(f"Error reading {f}: {e}")
            
    if not found:
        print(f"'{target}' not found in any operation file's Data Type sheet.")

if __name__ == "__main__":
    diagnose()
