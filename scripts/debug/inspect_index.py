import pandas as pd
import os

INDEX_FILE = "API Templates/$index.xlsm"


def inspect():
    if not os.path.exists(INDEX_FILE):
        print(f"File not found: {INDEX_FILE}")
        return

    xl = pd.ExcelFile(INDEX_FILE)
    print("Sheets:", xl.sheet_names)

    target_sheet = "Paths"

    print(f"Loading sheet: {target_sheet}")
    df = pd.read_excel(INDEX_FILE, sheet_name=target_sheet)
    print("Columns:", df.columns.tolist())
    print("First 5 rows:")
    print(df.head(5).to_string())


if __name__ == "__main__":
    inspect()
