
import os
import pandas as pd

def find_and_inspect_op_file():
    base_dir = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP"
    file_name = "postPayeeInformationRequests.260129.xlsx"
    
    # Fuzzy find the file
    all_files = os.listdir(base_dir)
    matches = [f for f in all_files if file_name.lower() in f.lower()]
    
    if not matches:
        print(f"File {file_name} not found in {base_dir}")
        return
    
    full_path = os.path.join(base_dir, matches[0])
    print(f"Inspecting file: {full_path}")
    
    xl = pd.ExcelFile(full_path)
    print(f"Sheet names: {xl.sheet_names}")
    
    if "Responses" in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name="Responses")
        df.columns = df.columns.astype(str).str.strip()
        print("\n--- Responses Data (First 20 rows) ---")
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        # Filter for rows that might have PartyTypeExtended
        # In operation files, we use Schema Name usually.
        print(df.head(20))
        
        # Search for examples
        example_cols = [c for c in df.columns if 'Example' in c]
        if example_cols:
            print(f"\nExample columns found: {example_cols}")
            # Filter rows with non-empty examples
            cols_to_show = ['Name', 'Parent', 'Type'] + example_cols
            # Clean columns list to show only those present
            cols_to_show = [c for c in cols_to_show if c in df.columns]
            print(df[df[example_cols[0]].notna()][cols_to_show])
    else:
        print("Sheet 'Responses' not found.")

if __name__ == "__main__":
    find_and_inspect_op_file()
