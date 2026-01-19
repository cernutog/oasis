import pandas as pd
import os

FILE = "API Templates/account_assessment_vop_bulk.251111.xlsm"


def inspect():
    if not os.path.exists(FILE):
        print(f"File not found: {FILE}")
        return

    print(f"Loading {FILE} sheet '400'")
    try:
        df = pd.read_excel(FILE, sheet_name="400", header=None)
        print("First 20 rows raw:")
        print(df.head(20).to_string())
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    inspect()
