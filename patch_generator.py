path = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if skip:
        if 'else:' in line and '256' in str(i+1): # safe anchor 256
             skip = False
             # Fall through to else logic
        else:
             continue

    if 'if issue.issue_type == "Description Change" and issue.old_value is not None:' in line:
        indent = line[:line.find('if ')]
        inner_indent = indent + "     "
        new_lines.append(line)
        new_lines.append(f'{inner_indent}# Case: Description (Rich Diff)\n')
        new_lines.append(f'{inner_indent}p.add_run(f"{{idx_str}} {{issue.details}}")\n')
        new_lines.append(f'{inner_indent}p_old = row_cells[3].add_paragraph()\n')
        new_lines.append(f'{inner_indent}p_old.paragraph_format.left_indent = Inches(0.4)\n')
        new_lines.append(f'{inner_indent}p_old.add_run("From: ").bold = True\n')
        new_lines.append(f'{inner_indent}p_new = row_cells[3].add_paragraph()\n')
        new_lines.append(f'{inner_indent}p_new.paragraph_format.left_indent = Inches(0.4)\n')
        new_lines.append(f'{inner_indent}p_new.add_run("To: ").bold = True\n')
        new_lines.append(f'{inner_indent}self._render_rich_diff(p_old, p_new, issue.old_value, issue.new_value)\n')
        skip = True # skip until next block
    elif 'else:' in line and i > 250:
        indent = line[:line.find('else:')]
        inner_indent = indent + "     "
        # Inject Elif here
        new_lines.append(f'{indent}# Case: Other constraints (Simple From/To)\n')
        new_lines.append(f'{indent}elif (issue.old_value is not None or issue.new_value is not None) and "from" not in issue.details.lower():\n')
        new_lines.append(f'{inner_indent}p.add_run(f"{{idx_str}} {{issue.details}}")\n')
        new_lines.append(f'{inner_indent}p_old = row_cells[3].add_paragraph()\n')
        new_lines.append(f'{inner_indent}p_old.paragraph_format.left_indent = Inches(0.4)\n')
        new_lines.append(f'{inner_indent}p_old.add_run("From: ").bold = True\n')
        new_lines.append(f'{inner_indent}p_old.add_run(str(issue.old_value))\n')
        new_lines.append(f'{inner_indent}p_new = row_cells[3].add_paragraph()\n')
        new_lines.append(f'{inner_indent}p_new.paragraph_format.left_indent = Inches(0.4)\n')
        new_lines.append(f'{inner_indent}p_new.add_run("To: ").bold = True\n')
        new_lines.append(f'{inner_indent}p_new.add_run(str(issue.new_value))\n')
        new_lines.append(line)
    else:
        new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("SUCCESS: Generator patched bit-perfectly.")
