import os

fname = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(fname, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_mode = False

for i, line in enumerate(lines):
    # 1. Summary Table Issue Type Sort
    if 'types = sorted(list(set([i.issue_type for i in details_map[scope]])))' in line:
        indent = line[:line.find('types = sorted')]
        new_lines.append(f"{indent}types = sorted(list(set([i.issue_type for i in details_map[scope]])), key=lambda x: 0 if 'description' in x.lower() else 1)\n")
        continue

    # 2. Details Table Issue Type Sort
    if 'types_strs = []' in line:
        skip_mode = True
        indent = line[:line.find('types_strs = []')]
        # Instead of old 4 lines, insert sorted list comprehension direct
        new_lines.append(f"{indent}types_strs = sorted(list(set([iss.issue_type for iss in data])), key=lambda x: 0 if 'description' in x.lower() else 1)\n")
        continue

    if skip_mode:
        if 'if iss.issue_type not in types_strs:' in line or 'types_strs.append(iss.issue_type)' in line:
            continue
        if 'for iss in data:' in line:
            continue
        # stop skip when loop iteration is done
        if 'if types_strs:' in line or 'row_cells[3].text = ""' in line:
            skip_mode = False

    if not skip_mode:
        new_lines.append(line)

with open(fname, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Issue Type sorting applied')
if skip_mode: print('WARNING: skip_mode left open!')
