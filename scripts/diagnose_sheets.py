import pandas as pd

def list_sheets():
    try:
        xl = pd.ExcelFile("API Templates/$index.xlsm")
        print("Sheets found:", xl.sheet_names)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    list_sheets()
