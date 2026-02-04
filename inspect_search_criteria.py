
import pandas as pd
import os

def inspect_search_criteria():
    index_path = os.path.join('Templates Legacy', '$index.xlsm')
    if not os.path.exists(index_path):
        print(f"FAIL: {index_path} not found")
        return
    
    xl = pd.ExcelFile(index_path)
    if 'Data Type' in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name='Data Type', dtype=str)
        # Find SearchCriteria
        sc_df = df[df.astype(str).apply(lambda x: x.str.contains('SearchCriteria', case=False)).any(axis=1)]
        print("SearchCriteria rows in Data Type sheet:")
        print(sc_df.head(20))
        
        # Also find its children
        parent_col = next((c for c in df.columns if "parent" in str(c).lower()), None)
        if parent_col:
            children = df[df[parent_col].astype(str).str.contains('SearchCriteria', case=False)]
            print("\nChildren of SearchCriteria:")
            print(children[['Data Type', parent_col, 'Type']]) # Adjust column names based on previous knowledge
        else:
            print("\nParent column not found in Data Type sheet.")

if __name__ == "__main__":
    inspect_search_criteria()
