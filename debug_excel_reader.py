import pandas as pd
import os
import glob

def inspect_excel():
    # Find $index.xlsm
    base_dir = os.path.join(os.getcwd(), "API Templates")
    files = glob.glob(os.path.join(base_dir, "*index.xlsm"))
    if not files:
        print("No index file found in", base_dir)
        return

    fpath = files[0]
    print(f"Inspecting: {fpath}")
    
    try:
        # Load raw first to see what pandas sees
        df = pd.read_excel(fpath, sheet_name="General Description", header=None)
        print("\n--- Raw Data (First 20 rows) ---")
        print(df.head(20))
        
        # Check what the parser would see
        print("\n--- Parser Logic Check ---")
        for index, row in df.iterrows():
            key = str(row.iloc[0]).strip().lower()
            val = row.iloc[1]
            print(f"Row {index}: Key='{key}' -> Val='{val}'")
            
            if "filename" in key and "pattern" in key:
                print(">>> FOUND PATTERN KEY!")
            if "release" in key:
                print(">>> FOUND RELEASE KEY!")

    except Exception as e:
        print(f"Error reading excel: {e}")

if __name__ == "__main__":
    inspect_excel()
