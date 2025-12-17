import pandas as pd

def inspect_headers():
    try:
        df = pd.read_excel("API Templates/$index.xlsm", sheet_name="Headers")
        print("Columns:", df.columns.tolist())
        # Filter for dateTime
        subset = df[df.astype(str).apply(lambda x: x.str.contains('dateTime', case=False, na=False)).any(axis=1)]
        print("\nRows matching 'dateTime':")
        print(subset.to_string())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    inspect_headers()
