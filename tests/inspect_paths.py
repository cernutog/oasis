
import pandas as pd
import os

def inspect_paths_structure():
    index_path = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP/$index.xlsx"
    df = pd.read_excel(index_path, sheet_name="Paths")
    print("\n--- First 10 rows of Paths sheet ---")
    print(df.head(10))

if __name__ == "__main__":
    inspect_paths_structure()
