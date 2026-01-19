import pandas as pd
import os

file_path = 'Imported Templates/create-transaction-assessment.260114.xlsx'
sheet_name = '201'

if os.path.exists(file_path):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=1)
        print(f"--- Sheet: {sheet_name} ---")
        # print specific rows
        print(df[df['Name'].isin(['application/json', 'fuid', 'riskInfoArray'])][['Section', 'Name', 'Parent', 'Type']])
        print("\nAll Rows:")
        print(df[['Section', 'Name', 'Parent', 'Type']].head(10))
    except Exception as e:
        print(f"Error: {e}")
else:
    print("File not found.")
