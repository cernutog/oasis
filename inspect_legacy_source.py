
import pandas as pd
import os

def inspect_legacy_excel():
    file_path = os.path.join('Templates Legacy', 'rejectParticipantOperation.210702.xlsm')
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return

    print(f"--- Inspecting {file_path} ---")
    xl = pd.ExcelFile(file_path)
    
    if 'Body' in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name='Body', dtype=str, header=None)
        print("\nBody Sheet (first 10 rows):")
        # Print raw content to see column headers and names
        for i, row in df.head(10).iterrows():
            print(f"Row {i}: {row.tolist()}")
    else:
        print("\n'Body' sheet not found.")

    if '200' in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name='200', dtype=str, header=None)
        print("\n200 Sheet (first 10 rows):")
        for i, row in df.head(10).iterrows():
            print(f"Row {i}: {row.tolist()}")

if __name__ == "__main__":
    inspect_legacy_excel()
