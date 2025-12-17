import pandas as pd

def inspect_schemas():
    try:
        df = pd.read_excel("API Templates/$index.xlsm", sheet_name="Schemas")
        print("Columns:", df.columns.tolist())
        # Filter for identification
        subset = df[df.astype(str).apply(lambda x: x.str.contains('identification', case=False, na=False)).any(axis=1)]
        print("\nRows matching 'identification':")
        print(subset.to_string())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    inspect_schemas()
