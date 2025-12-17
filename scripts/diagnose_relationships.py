import pandas as pd

def inspect_structure():
    try:
        df = pd.read_excel("API Templates/$index.xlsm", sheet_name="Responses")
        # Clean columns
        df.columns = df.columns.str.strip()
        
        # Filter where Name or Parent contains errors or dateTime
        mask = df['Name'].astype(str).str.contains('errors|dateTime', case=False, na=False) | \
               df['Parent'].astype(str).str.contains('errors|dateTime', case=False, na=False)
               
        subset = df[mask][['Name', 'Parent', 'Type']]
        print(subset.to_string())
        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    inspect_structure()
