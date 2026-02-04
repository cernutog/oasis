
import pandas as pd

def inspect_index():
    path = "Output OAS/$index.xlsx"
    df = pd.read_excel(path, sheet_name="Schemas")
    print(df[["Name", "Parent"]].head(50))

if __name__ == "__main__":
    inspect_index()
