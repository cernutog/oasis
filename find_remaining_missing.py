
import os
import pandas as pd

def check_missing_in_legacy():
    legacy_dir = "Templates Legacy"
    missing = [
        "Boolean1", "DailyThresholds1", "DefaultDailyThresholds1", 
        "ExceptionLacValues1", "LacAgenda1", "LacDefaultAgenda1", 
        "Number1", "SenderBIC1", "liquidityManagementRequest", "liquidityManagementResponse"
    ]
    
    found = {m: [] for m in missing}
    
    for root, dirs, files in os.walk(legacy_dir):
        for file in files:
            if file.endswith((".xlsm", ".xlsx")):
                path = os.path.join(root, file)
                try:
                    # Search in all sheets
                    xls = pd.ExcelFile(path)
                    for sheet in xls.sheet_names:
                        df = pd.read_excel(path, sheet_name=sheet).astype(str)
                        for m in missing:
                            if df.apply(lambda row: row.str.contains(m, case=False).any(), axis=1).any():
                                found[m].append(f"{file} [{sheet}]")
                except Exception as e:
                    pass
                    
    for m, locs in found.items():
        print(f"{m}: {' | '.join(locs) if locs else 'NOT FOUND'}")

if __name__ == "__main__":
    check_missing_in_legacy()
