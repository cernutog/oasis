import pandas as pd
import os

def deep_analyze_excel(file_path, label):
    print(f"\n==================================================")
    print(f"DEEP ANALYSIS: {label}")
    print(f"Path: {file_path}")
    print(f"==================================================")
    try:
        xl = pd.ExcelFile(file_path)
        print(f"Sheets: {xl.sheet_names}")
        for sheet in xl.sheet_names:
            print(f"\n--- [Sheet: {sheet}] ---")
            # Read first 10 rows to see headers and some data
            df = pd.read_excel(xl, sheet_name=sheet, header=None).head(10)
            print(df.to_string(index=False))
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")

legacy_index = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy\$index.xlsm"
modern_index = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Master\$index.xlsx"

deep_analyze_excel(legacy_index, "LEGACY INDEX")
deep_analyze_excel(modern_index, "MODERN INDEX")

legacy_op = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Legacy\apDetails.250410.xlsm"
modern_op = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Master\account_assessment.251111.xlsm"

deep_analyze_excel(legacy_op, "LEGACY OPERATION")
deep_analyze_excel(modern_op, "MODERN OPERATION")
