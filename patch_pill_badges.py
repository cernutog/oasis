import os

fname = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(fname, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'key = iss.schema_name if iss.schema_name else "-"' in line:
        new_lines.append(line.replace('key = iss.schema_name if iss.schema_name else "-"', 'key = (iss.schema_name if iss.schema_name else "-", iss.details, iss.old_val, iss.new_val)'))
    elif 'self.doc.add_heading(endpoint, 2)' in line:
        # Replace the entire add_heading with sub-badges execution
        indent = line[:line.find('self.doc.add_heading')]
        sub_lines = [
            f"{indent}parts = endpoint.split(' ', 1)\n",
            f"{indent}method = parts[0] if len(parts) > 0 else ''\n",
            f"{indent}path = parts[1] if len(parts) > 1 else ''\n",
            f"{indent}p_head = self.doc.add_heading('', level=2)\n",
            f"{indent}if method:\n",
            f"{indent}     run_m = p_head.add_run(f' {{method.upper()}} ')\n",
            f"{indent}     run_m.bold = True\n",
            f"{indent}     from docx.shared import RGBColor\n",
            f"{indent}     run_m.font.color.rgb = RGBColor(255, 255, 255)\n",
            f"{indent}     color_map = {{'GET': '1167B1', 'POST': '188038', 'PUT': 'E37400', 'DELETE': 'D93025', 'PATCH': '9334E6'}}\n",
            f"{indent}     self._apply_shading(run_m, color_map.get(method.upper(), '70757A'))\n",
            f"{indent}     p_head.add_run(f' {{path}}')\n",
            f"{indent}else:\n",
            f"{indent}     p_head.add_run(endpoint)\n"
        ]
        new_lines.extend(sub_lines)
    else:
        new_lines.append(line)

with open(fname, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Done complete lines-replace')
