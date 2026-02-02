
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
        
        # Look for PartyTypeExtended and its examples
        example_cols = [c for c in df.columns if 'Example' in c]
        name_rows = df[df['Name'].astype(str).str.contains("name")]
        if not name_rows.empty:
            print("\nRows containing 'name':")
            cols_to_show = ['Name', 'Parent', 'Type'] + example_cols
            cols_to_show = [c for c in cols_to_show if c in df.columns]
            print(name_rows[cols_to_show])
            
    # Check "Body Example" sheet
    if "Body Example" in xl.sheet_names:
        print("\n--- Sheet: Body Example ---")
        df = pd.read_excel(xl, sheet_name="Body Example")
        print(df.head(20))

if __name__ == "__main__":
    inspect_200_example()
