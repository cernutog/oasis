import pandas as pd
import os

FILE = "API Templates/$index.xlsm"

def search():
    if not os.path.exists(FILE):
        print("File not found.")
        return

    xl = pd.ExcelFile(FILE)
    print(f"Sheets: {xl.sheet_names}")
    
    for sheet in xl.sheet_names:
        try:
            df = pd.read_excel(FILE, sheet_name=sheet)
            # Check if Name column exists
            # Normalize columns
            df.columns = df.columns.astype(str).str.strip()
            
            if "Name" in df.columns:
                # Search for 'pri'
                matches = df[df["Name"].astype(str).str.strip() == "pri"]
                if not matches.empty:
                    print(f"\nFound 'pri' in sheet '{sheet}':")
                    print(matches.to_string())
        except Exception as e:
            print(f"Error reading {sheet}: {e}")

if __name__ == "__main__":
    search()
