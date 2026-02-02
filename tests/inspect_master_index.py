import openpyxl
import os

master_index = r"c:\Users\giuse\.gemini\antigravity\scratch\OASIS\Templates Master\$index.xlsx"
if os.path.exists(master_index):
    wb = openpyxl.load_workbook(master_index)
    ws = wb["Schemas"]
    print(f"--- Schemas Structure ---")
    for r in range(1, 10):
        row_vals = [c.value for c in ws[r]]
        print(f"Row {r}: {row_vals}")
else:
    print("Master index not found.")
