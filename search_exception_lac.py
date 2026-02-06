
import pandas as pd
import os

def check_exception_lac_legacy():
    legacy_dir = "Templates Legacy"
    target = "ExceptionLacValues"
    
    results = []
    
    for root, dirs, files in os.walk(legacy_dir):
        for file in files:
            if file.endswith((".xlsm", ".xlsx")):
                path = os.path.join(root, file)
                try:
                    xls = pd.ExcelFile(path)
                    for sheet in xls.sheet_names:
                        df = pd.read_excel(path, sheet_name=sheet).astype(str)
                        # Look for row where target exists in Name or Parent column
                        # (Adjust column indices as needed, or use column names if they exist)
                        # We'll just look for the string in the whole dataframe for now to find the sheet
                        if df.apply(lambda row: row.str.contains(target, case=False).any(), axis=1).any():
                            # Now try to find the specific definition
                            # Assuming standard structure: Name is in one column, Parent in another
                            # We'll print the rows where target is present
                            mask = df.apply(lambda row: row.str.contains(target, case=False).any(), axis=1)
                            relevant_rows = df[mask]
                            results.append({
                                'file': file,
                                'sheet': sheet,
                                'rows': relevant_rows.values.tolist()
                            })
                except Exception as e:
                    pass
    
    for res in results:
        print(f"File: {res['file']} | Sheet: {res['sheet']}")
        for r in res['rows']:
            print(f"  Row: {r}")

if __name__ == "__main__":
    check_exception_lac_legacy()
