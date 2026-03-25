import os

fname = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(fname, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_mode = False
p_item_patched = False

for i, line in enumerate(lines):
    # 1. Bold the bullet detail in Summary Table
    if 'p_item.text = f"• [{sub_idx_str}] {iss.details}"' in line:
        indent = line[:line.find('p_item.text')]
        sub_lines = [
            f"{indent}p_item.text = ''\n",
            f"{indent}run_agg_idx = p_item.add_run(f'• [{{sub_idx_str}}] ')\n",
            f"{indent}run_agg_det = p_item.add_run(iss.details)\n",
            f"{indent}run_agg_det.bold = True\n"
        ]
        new_lines.extend(sub_lines)
        p_item_patched = True
        continue

    # 2. Bold the detail in Detailed Section tables too
    if 'p_head.text = f"{idx_str}{iss.details}"' in line:
        indent = line[:line.find('p_head.text')]
        sub_lines = [
            f"{indent}p_head.text = ''\n",
            f"{indent}run_det_idx = p_head.add_run(idx_str)\n",
            f"{indent}run_det_det = p_head.add_run(iss.details)\n",
            f"{indent}run_det_det.bold = True\n"
        ]
        new_lines.extend(sub_lines)
        continue
    
    if 'p_cur.text = f"{idx_str}{iss.details}"' in line:
        indent = line[:line.find('p_cur.text')]
        sub_lines = [
            f"{indent}p_cur.text = ''\n",
            f"{indent}run_det_idx = p_cur.add_run(idx_str)\n",
            f"{indent}run_det_det = p_cur.add_run(iss.details)\n",
            f"{indent}run_det_det.bold = True\n"
        ]
        new_lines.extend(sub_lines)
        continue

    # 3. Revert/Remove HTTP method badges
    if 'parts = endpoint.split(' in line and 'issues' not in line: # issues contains endpoint iterate
        # Start skip
        skip_mode = True
        p_head_found = False
        # Insert back self.doc.add_heading(endpoint, level=2)
        indent = line[:line.find('parts = endpoint')]
        new_lines.append(f"{indent}self.doc.add_heading(endpoint, level=2)\n")
    
    if skip_mode:
        if 'p_head.add_run(endpoint)' in line:
            p_head_found = True
        # Once we find the closing node, skip until the last line of that block
        if p_head_found and 'else:' not in line and 'run_m' not in line:
             if 'p_head.add_run(' not in line and 'add_heading' not in line:
                 skip_mode = False
                 continue
        continue

    new_lines.append(line)

with open(fname, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f'Done boldings patches. Bullet patched: {p_item_patched}')
if skip_mode: print('WARNING: skip_mode was left open! Possible issue during parse.')
