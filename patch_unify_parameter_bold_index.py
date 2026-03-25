import os

fname_a = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\compatibility_analyzer.py'
with open(fname_a, 'r', encoding='utf-8') as f:
    text_a = f.read()

# 1. Unify Parameter schema_name to use ': ' instead of ' ()'
# Search for: schema_name=f"Parameter ({name})"
text_a = text_a.replace('schema_name=f"Parameter ({name})"', 'schema_name=f"Parameter: {name}"')

with open(fname_a, 'w', encoding='utf-8') as f:
    f.write(text_a)


print("Patching generator for bold indices...")
fname_g = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(fname_g, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if 'run_agg_idx = p_item.add_run(' in line:
        new_lines.append(line)
        indent = line[:line.find('run_agg_idx')]
        new_lines.append(f"{indent}run_agg_idx.bold = True\n")
    elif 'run_det_idx = p_head.add_run(idx_str)' in line:
        new_lines.append(line)
        indent = line[:line.find('run_det_idx')]
        new_lines.append(f"{indent}run_det_idx.bold = True\n")
    elif 'run_det_idx = p_cur.add_run(idx_str)' in line:
        new_lines.append(line)
        indent = line[:line.find('run_det_idx')]
        new_lines.append(f"{indent}run_det_idx.bold = True\n")
    else:
        new_lines.append(line)

with open(fname_g, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Done complete patches for parameter unify and bold indices')
