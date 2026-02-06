
import pandas as pd

def debug_index():
    path = r"Output OAS/$index.xlsx"
    df = pd.read_excel(path, sheet_name="Schemas").astype(str)
    
    # Check all rows where Name or Parent contains 'Alerts' (case-insensitive)
    matches = df[(df.iloc[:, 0].str.contains("Alerts", case=False)) | (df.iloc[:, 1].str.contains("Alerts", case=False))]
    print("--- Alerts/alerts Rows in Index ---")
    print(matches)
    
    # Check what else is there as a root
    roots = df[df.iloc[:, 1] == "nan"]
    print("\n--- First 20 Roots ---")
    print(roots.head(20))

if __name__ == "__main__":
    debug_index()
