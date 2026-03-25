from docx import Document
import os

path = r"C:\EBA Clearing\APIs\OAS Comparison\RT1 API Participant\2026Q4\OAS_Comparison_Interface_Compatibility_20260324_210401.docx"
if not os.path.exists(path):
    print("GOLDEN NOT FOUND")
    exit()

doc = Document(path)
issues = []
for table in doc.tables:
    if len(table.columns) == 4 and "Location/Scope" in table.rows[0].cells[0].text:
        for row in table.rows[1:]:
            loc = row.cells[0].text
            prop = row.cells[1].text
            type_it = row.cells[2].text
            details = row.cells[3].text
            issues.append((loc, prop, type_it, details))

print(f"TOTAL ISSUES IN GOLDEN: {len(issues)}")
# Print first 20 to see the style
for i, (l, p, t, d) in enumerate(issues[:20]):
    print(f"{i+1}. {l} | {p} | {t} | {d[:100]}...")

# Specifically check for LacAmount
lac_issues = [iss for iss in issues if "LacAmount" in iss[1]]
print(f"LACAMOUNT ISSUES IN GOLDEN: {len(lac_issues)}")
