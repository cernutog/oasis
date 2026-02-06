
import pandas as pd
import os

def find_pascal_alerts():
    legacy_dir = "Templates Legacy"
    for root, dirs, files in os.walk(legacy_dir):
        for file in files:
            if file.endswith((".xlsm", ".xlsx")):
                path = os.path.join(root, file)
                try:
                    xls = pd.ExcelFile(path)
                    for sheet in xls.sheet_names:
                        df = pd.read_excel(path, sheet_name=sheet).astype(str)
                        if df.apply(lambda row: row.str.contains("^Alerts$", regex=True).any(), axis=1).any():
                            print(f"MATCH 'Alerts' in {file} [{sheet}]")
                except:
                    pass

if __name__ == "__main__":
    find_pascal_alerts()
