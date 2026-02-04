
import os
import pandas as pd

def audit_headers():
    legacy_dir = "Templates Legacy"
    results = []
    for f in os.listdir(legacy_dir):
        if not f.endswith(".xlsm") or f == "$index.xlsm":
            continue
        try:
            xl = pd.ExcelFile(os.path.join(legacy_dir, f))
            if "Data Type" in xl.sheet_names:
                df = xl.parse("Data Type", nrows=15)
                # Find header
                header_idx = -1
                for idx, row in df.iterrows():
                    row_vals = [str(v).strip().lower() for v in row.values]
                    if any(kw in row_vals for kw in ["data type", "type", "element"]):
                        header_idx = idx
                        break
                
                if header_idx != -1:
                    cols = [str(c).strip() for c in df.iloc[header_idx]]
                    results.append({"file": f, "cols": cols})
                else:
                    results.append({"file": f, "cols": "No header found"})
        except Exception as e:
            results.append({"file": f, "cols": f"Error: {e}"})
            
    for res in results:
        print(f"{res['file']}: {res['cols']}")

if __name__ == "__main__":
    audit_headers()
