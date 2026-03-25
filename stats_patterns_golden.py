from docx import Document
import os

path = r"C:\EBA Clearing\APIs\OAS Comparison\RT1 API Participant\2026Q4\OAS_Comparison_Interface_Compatibility_20260324_210401.docx"
doc = Document(path)
patterns = []
for table in doc.tables:
    if len(table.columns) == 4 and "Location/Scope" in table.rows[0].cells[0].text:
        for row in table.rows[1:]:
            details = row.cells[3].text
            if "pattern" in details.lower():
                loc = row.cells[0].text
                prop = row.cells[1].text
                patterns.append((loc, prop))

print(f"TOTAL PATTERNS IN GOLDEN: {len(patterns)}")
from collections import Counter
counts = Counter([p.strip() for l, p in patterns])
for p, c in counts.most_common():
    print(f" - {p}: {c}")
