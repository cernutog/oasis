import os

fname_a = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\compatibility_analyzer.py'
with open(fname_a, 'r', encoding='utf-8') as f:
    text_a = f.read()

# 1. Prepend 'Schema:' to component names
old_get_s_name = '''        def _get_s_name(s):
            if isinstance(s, dict):
                ref = s.get('x-ref')
                if ref: return ref.split('/')[-1]
            return None'''

new_get_s_name = '''        def _get_s_name(s):
            if isinstance(s, dict):
                ref = s.get('x-ref')
                if ref: return f"Schema: {ref.split('/')[-1]}"
            return None'''

text_a = text_a.replace(old_get_s_name, new_get_s_name)

with open(fname_a, 'w', encoding='utf-8') as f:
    f.write(text_a)



print("Patching generator for bullet location suffixes...")
fname_g = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(fname_g, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if "run_agg_det = p_item.add_run(iss.details)" in line:
        indent = line[:line.find("run_agg_det")]
        sub_lines = [
            f"{indent}loc_suffix = f' (in {{iss.location}})' if iss.location and iss.location not in ('Operation', 'Request Body') else ''\n",
            f"{indent}if iss.item_name and iss.item_name != '-' and iss.item_name not in loc_suffix: loc_suffix = loc_suffix.replace(')', f' - {{iss.item_name}})')\n",
            f"{indent}run_agg_det = p_item.add_run(f'{{iss.details}}{{loc_suffix}}')\n"
        ]
        new_lines.extend(sub_lines)
    else:
        new_lines.append(line)

with open(fname_g, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Done complete patches')
