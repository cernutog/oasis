
import os
import pandas as pd

def inspect_200_example():
    base_dir = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP"
    file_path = os.path.join(base_dir, "postPayeeInformationRequests.260129.xlsx")
    
    xl = pd.ExcelFile(file_path)
    
    # Check "200" sheet
    if "200" in xl.sheet_names:
        print("\n--- Sheet: 200 ---")
        df = pd.read_excel(xl, sheet_name="200")
        df.columns = df.columns.astype(str).str.strip()
        
        print(f"Columns in 200: {list(df.columns)}")
        
        # Fuzzy find columns
        name_col = [c for c in df.columns if 'name' in c.lower()][0]
        
        # Look for rows where the name column (lowercase) contains "name"
        name_rows = df[df[name_col].astype(str).str.lower().str.contains("name")]
        if not name_rows.empty:
            print("\nRows containing 'name':")
            # Show all columns for these rows to be sure
            print(name_rows)

if __name__ == "__main__":
    inspect_200_example()
