import openpyxl

# Read the REGENERATED $index.xlsx
wb = openpyxl.load_workbook(r'Imported Templates\$index.xlsx')
ws = wb['Paths']
val = ws.cell(row=3, column=9).value
if val:
    print("=== First 500 chars of Custom Extensions cell ===")
    print(repr(val[:500]))
    print("\n=== Visualized with line numbers ===")
    for i, line in enumerate(val.split('\n')[:10]):
        indent = len(line) - len(line.lstrip())
        print(f"{i}: [{indent} spaces] {line[:80]}")
else:
    print("Cell is EMPTY")
