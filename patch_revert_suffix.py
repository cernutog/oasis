import os

fname = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(fname, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_mode = False

for i, line in enumerate(lines):
    # 1. Inject Crash diagnostic around freq[scope] = freq.get(scope, 0) + 1
    if 'freq[scope] = freq.get(scope, 0) + 1' in line:
        indent = line[:line.find('freq[scope]')]
        sub_lines = [
            f"{indent}try:\n",
            f"{indent}    freq[scope] = freq.get(scope, 0) + 1\n",
            f"{indent}except TypeError:\n",
            f"{indent}    with open('crash_diag.txt', 'w') as f_diag:\n",
            f"{indent}        f_diag.write(f'SCOPE: {{scope}}\\nTYPE: {{type(scope)}}\\nDETAILS: {{issue.details}}\\nLOCATION: {{issue.location}}\\nITEM: {{issue.item_name}}')\n",
            f"{indent}    raise\n"
        ]
        new_lines.extend(sub_lines)
        continue

    # 2. Revert the loc_suffix from Summary detail bullet list (Lines 175-177)
    if 'loc_suffix = f\' (in {iss.location})\'' in line:
        skip_mode = True
        continue
    if 'if iss.item_name and iss.item_name != \'-\'' in line:
        continue
    if 'run_agg_det = p_item.add_run(f\'{iss.details}{loc_suffix}\')' in line:
        indent = line[:line.find('run_agg_det')]
        new_lines.append(f"{indent}run_agg_det = p_item.add_run(iss.details)\n")
        skip_mode = False
        continue

    if not skip_mode:
        new_lines.append(line)

with open(fname, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Diagnostics injected and suffix reverted')
