import pandas as pd
import sys

def inspect():
    file_path = "API Templates/$index.xlsm"
    try:
        # Load Responses sheet
        print(f"Loading {file_path} - Responses...")
        df = pd.read_excel(file_path, sheet_name="Responses")
        
        # Filter for errors
        subset = df[df.astype(str).apply(lambda x: x.str.contains('errors', case=False, na=False)).any(axis=1)]
        print("\nRows matching 'errors':")
        print(subset.to_string())
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect()
