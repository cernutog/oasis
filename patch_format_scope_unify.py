import os

fname = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(fname, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add _format_scope method inside class CompatibilityDocxGenerator
class_def = "class CompatibilityDocxGenerator:"
formatter_code = """class CompatibilityDocxGenerator:
    def _format_scope(self, s: str) -> str:
        if ": " in s:
            kind, name = s.split(": ", 1)
            return f"{name}\\n({kind})"
        return s
"""

if "def _format_scope" not in text:
    text = text.replace(class_def, formatter_code)

# 2. Update Column row population in Summary table
old_sum_row = "             row[1].text = scope"
new_sum_row = "             row[1].text = self._format_scope(scope)"

text = text.replace(old_sum_row, new_sum_row)

# 3. Update Column row population in Details table
old_det_row = "                  row_cells[0].text = loc"
new_det_row = "                  row_cells[0].text = self._format_scope(loc) if ':' in loc else loc" # Only if has ':'

text = text.replace(old_det_row, new_det_row)

with open(fname, 'w', encoding='utf-8') as f:
    f.write(text)

print('Scope unity format applied')
