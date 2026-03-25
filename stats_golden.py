from docx import Document
import os
import re

path = r"C:\EBA Clearing\APIs\OAS Comparison\RT1 API Participant\2026Q4\OAS_Comparison_Interface_Compatibility_20260324_210401.docx"
doc = Document(path)
desc_changes = []
for table in doc.tables:
    if len(table.columns) == 4 and "Location/Scope" in table.rows[0].cells[0].text:
        for row in table.rows[1:]:
            details = row.cells[3].text
            if "Description changed" in details:
                # Find the location and property
                loc = row.cells[0].text
                prop = row.cells[1].text
                desc_changes.append((loc, prop))

print(f"UNIQUE DESC CHANGES IN GOLDEN: {len(desc_changes)}")
# Group by property
from collections import Counter
counts = Counter([p.strip() for l, p in desc_changes])
for p, c in counts.most_common():
    print(f"{p}: {c}")
