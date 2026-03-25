from docx import Document
import os

path = r"C:\EBA Clearing\APIs\OAS Comparison\RT1 API Participant\2026Q4\OAS_Comparison_Interface_Compatibility_20260324_210401.docx"
doc = Document(path)
table = doc.tables[0]
for row in table.rows:
    print(f"{row.cells[0].text}: {row.cells[1].text} || {row.cells[2].text}")
