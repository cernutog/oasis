import os

fname = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(fname, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_summary_loop = False
in_details_loop = False

for i, line in enumerate(lines):
    # 1. Summary Table Sort
    if 'for j_idx, iss in enumerate(dedup_dict.values()):' in line:
        indent = line[:line.find('for j_idx')]
        sub_lines = [
            f"{indent}sorted_items = sorted(dedup_dict.values(), key=lambda x: 0 if ('description' in x.issue_type.lower() or 'description' in x.details.lower()) else 1)\n",
            f"{indent}for j_idx, iss in enumerate(sorted_items):\n"
        ]
        new_lines.extend(sub_lines)
        continue

    # 2. Details Table Sort
    if 'for idx, iss in enumerate(data):' in line:
        indent = line[:line.find('for idx')]
        sub_lines = [
            f"{indent}sorted_data = sorted(data, key=lambda x: 0 if ('description' in x.issue_type.lower() or 'description' in x.details.lower()) else 1)\n",
            f"{indent}for idx, iss in enumerate(sorted_data):\n"
        ]
        new_lines.extend(sub_lines)
        continue

    new_lines.append(line)

with open(fname, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Description sorting applied')
