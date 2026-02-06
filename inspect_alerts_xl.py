
import pandas as pd
import os

def check_list_alerts_structure():
    path = r"Templates Legacy/listAlerts.211207.xlsm"
    xl = pd.ExcelFile(path)
    df = pd.read_excel(path, sheet_name="200").astype(str)
    # Output important columns: Name (col 1), Parent (col 2), Type (col 4)
    # Actually, let's look at the raw data to see column names
    print(df.columns.tolist())
    print(df.iloc[:15, [0, 1, 2, 3, 4]])

if __name__ == "__main__":
    check_list_alerts_structure()
