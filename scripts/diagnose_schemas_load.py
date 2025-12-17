import pandas as pd

def debug_load():
    file_path = "API Templates/$index.xlsm"
    try:
        # Mimic parser.load_excel_sheet logic partially
        df_raw = pd.read_excel(file_path, sheet_name="Schemas", header=None)
        print("--- RAW HEAD (5 rows) ---")
        print(df_raw.head(5))
        
        # Try finding header
        header_idx = -1
        for idx, row in df_raw.head(10).iterrows():
            row_str = row.astype(str).str.lower()
            if any(x in row_str.values for x in ['name', 'type', 'description']):
                header_idx = idx
                print(f"Header found at index: {idx}")
                break
                
        if header_idx != -1:
            df = pd.read_excel(file_path, sheet_name="Schemas", header=header_idx)
            print("\n--- LOADED COLUMNS ---")
            print(df.columns.tolist())
            print("\n--- DATA HEAD ---")
            # Check identification
            print("\n--- identification ROW ---")
            print(df[df['Name'].str.contains('identification', case=False, na=False)][['Name', 'Type', 'Parent']]) 
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    debug_load()
