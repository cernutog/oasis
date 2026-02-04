
import os
import pandas as pd

def exhaustive_search():
    legacy_dir = "Templates Legacy"
    target = "CGSSettlementBIC"
    found_any = False
    
    print(f"Exhaustive search for '{target}' in {legacy_dir} (ALL SHEETS)...")
    for f in os.listdir(legacy_dir):
        if not f.endswith(".xlsm") and not f.endswith(".xlsx"):
            continue
        
        try:
            xl = pd.ExcelFile(os.path.join(legacy_dir, f))
            for sheet in xl.sheet_names:
                df = xl.parse(sheet)
                mask = df.astype(str).apply(lambda x: x.str.contains(target, case=False, na=False)).any(axis=1)
                if mask.any():
                    print(f"\n--- FOUND in {f} | Sheet: {sheet} ---")
                    print(df[mask].to_string())
                    found_any = True
        except Exception as e:
            pass
            
    if not found_any:
        print(f"'{target}' not found anywhere in legacy directory.")

if __name__ == "__main__":
    exhaustive_search()
