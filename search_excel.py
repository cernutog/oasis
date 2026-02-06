
import pandas as pd
import os
import zipfile
import xml.etree.ElementTree as ET

def search_in_excel(folder, query):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith((".xlsx", ".xlsm")):
                path = os.path.join(root, file)
                try:
                    # Quick check using shared strings if possible, but let's just use pandas for simplicity
                    xl = pd.ExcelFile(path)
                    for sheet in xl.sheet_names:
                        df = pd.read_excel(path, sheet_name=sheet).astype(str)
                        if df.apply(lambda row: row.str.contains(query, case=False).any(), axis=1).any():
                            print(f"FOUND '{query}' in {path} [Sheet: {sheet}]")
                except Exception as e:
                    pass

if __name__ == "__main__":
    search_in_excel("Templates Legacy", "Alerts")
