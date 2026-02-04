
import pandas as pd
import os

def search_for_property(prop_name):
    legacy_dir = 'Templates Legacy'
    results = []
    
    for filename in os.listdir(legacy_dir):
        if filename.endswith(".xlsm") and filename != "$index.xlsm":
            file_path = os.path.join(legacy_dir, filename)
            try:
                xl = pd.ExcelFile(file_path)
                for sheet in xl.sheet_names:
                    if sheet == 'Body' or (sheet.isdigit() and int(sheet) >= 200):
                        df = pd.read_excel(xl, sheet_name=sheet, dtype=str, header=None)
                        # Check all cells for the prop_name
                        if df.isin([prop_name]).any().any():
                            results.append((filename, sheet))
            except:
                pass
    
    if results:
        print(f"Found '{prop_name}' in:")
        for res in results[:20]:
            print(f"  {res[0]} (Sheet: {res[1]})")
    else:
        print(f"'{prop_name}' NOT found in any Legacy Excel files.")

if __name__ == "__main__":
    search_for_property('operationRef')
    print("\n--- Searching for commandRef ---")
    search_for_property('commandRef')
