import pandas as pd
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
try:
    from parser import load_excel_sheet
except ImportError:
    # Quick mock if parser import fails or just use pandas directly
    pass

def search_value_in_sheet(file_path, sheet_name, targets):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        # Normalize columns
        df.columns = df.columns.astype(str).str.strip()
        
        # Columns to search (where references typically live)
        search_cols = [c for c in df.columns if any(x in c.lower() for x in ['schema', 'type', 'items', 'parent', 'ref'])]
        
        found = []
        for idx, row in df.iterrows():
            for col in search_cols:
                val = str(row[col]).strip()
                if val in targets:
                    found.append({
                        "file": os.path.basename(file_path),
                        "sheet": sheet_name,
                        "row": idx + 2, # +1 for 0-index, +1 for header
                        "column": col,
                        "value": val
                    })
        return found
    except Exception as e:
        # print(f"Skipping {sheet_name}: {e}")
        return []

def main():
    base_dir = "API Templates"
    index_file = os.path.join(base_dir, "$index.xlsm")
    
    targets = ["dateTime", "identification", "name", "DateTime", "Name", "Identification"]
    
    print(f"Searching for {targets} in Excel files...")
    
    all_findings = []
    
    # Check Index
    sheets = ["Schemas", "Parameters", "Headers", "Responses", "PATHS"] 
    # Note: Paths is usually "Paths" but let's be careful.
    
    xl = pd.ExcelFile(index_file)
    for sheet in xl.sheet_names:
        if sheet in ["General Description", "Tags"]: continue
        findings = search_value_in_sheet(index_file, sheet, targets)
        all_findings.extend(findings)
        
    # Check operation files (basic scan)
    # We can list them from directory
    for f in os.listdir(base_dir):
        if f.endswith(".xlsm") and f != "$index.xlsm":
            fpath = os.path.join(base_dir, f)
            try:
                xl_op = pd.ExcelFile(fpath)
                for sheet in xl_op.sheet_names:
                    if sheet in ["Parameters", "Body", "Body Example"] or sheet.isdigit():
                         findings = search_value_in_sheet(fpath, sheet, targets)
                         all_findings.extend(findings)
            except:
                pass

    print("\n--- RESULTS ---")
    if not all_findings:
        print("No matches found.")
    else:
        # Group by value
        df_res = pd.DataFrame(all_findings)
        for val in targets:
            subset = df_res[df_res['value'] == val]
            if not subset.empty:
                print(f"\nValue: '{val}'")
                print(subset[['file', 'sheet', 'row', 'column']].to_string(index=False))

if __name__ == "__main__":
    main()
