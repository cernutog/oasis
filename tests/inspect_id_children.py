
import pandas as pd

def inspect_identification():
    index_path = "C:/EBA Clearing/APIs/Templates/FPAD VOP for Responding PSP/$index.xlsx"
    df = pd.read_excel(index_path, sheet_name="Schemas")
    df.columns = df.columns.astype(str).str.strip()
    
    id_children = df[df['Parent'] == "identification"]
    print("\n--- Children of 'identification' ---")
    print(id_children[['Name', 'Parent', 'Type']])

if __name__ == "__main__":
    inspect_identification()
