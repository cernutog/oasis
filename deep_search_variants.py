
import pandas as pd
import os

def deep_search_variants():
    targets = ["DailyThresholds", "LacAgenda", "DefaultDailyThresholds", "LacDefaultAgenda", "ExceptionLacValues", "Boolean", "SenderBIC"]
    legacy_dir = "Templates Legacy"
    
    found_defs = {t: [] for t in targets}
    
    for root, dirs, files in os.walk(legacy_dir):
        for file in files:
            if file.endswith((".xlsm", ".xlsx")):
                path = os.path.join(root, file)
                try:
                    xls = pd.ExcelFile(path)
                    for sheet in xls.sheet_names:
                        df = pd.read_excel(path, sheet_name=sheet).astype(str)
                        for t in targets:
                            # Search in all columns
                            mask = df.apply(lambda row: row.str.contains(f"^{t}$", case=False, regex=True).any(), axis=1)
                            if mask.any():
                                rows = df[mask].values.tolist()
                                found_defs[t].append({
                                    'file': file,
                                    'sheet': sheet,
                                    'rows': rows
                                })
                except:
                    pass
                    
    for t, instances in found_defs.items():
        print(f"\n=== TARGET: {t} ({len(instances)} instances) ===")
        for inst in instances:
            print(f"File: {inst['file']} | Sheet: {inst['sheet']}")
            for r in inst['rows']:
                print(f"  {r}")

if __name__ == "__main__":
    deep_search_variants()
