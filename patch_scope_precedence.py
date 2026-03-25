import os
import re

fname = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\compatibility_analyzer.py'
with open(fname, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update _get_s_name assignment inside _compare_schemas to NOT overwrite if already set
old_assign = '''        n1 = _get_s_name(s1)
        n2 = _get_s_name(s2)
        if n1 or n2: current_schema = n1 or n2'''

new_assign = '''        n1 = _get_s_name(s1)
        n2 = _get_s_name(s2)
        if (n1 or n2) and (not current_schema or current_schema == "-"):
             current_schema = n1 or n2'''

text = text.replace(old_assign, new_assign)

# 2. Update caller: _compare_parameters
old_param_call = "self._compare_schemas(path, method, f\"Parameter ({location})\", p1['schema'], p2['schema'], name)"
# Replace with passing current_schema directly
new_param_call = "self._compare_schemas(path, method, f\"Parameter ({location})\", p1['schema'], p2['schema'], name, current_schema=f\"Parameter: {name}\")"

text = text.replace(old_param_call, new_param_call)

# 3. Update caller: Response Headers
old_header_call = "self._compare_schemas(path, method, f\"Response {code} Header\", s1, s2, h)"
new_header_call = "self._compare_schemas(path, method, f\"Response {code} Header\", s1, s2, h, current_schema=f\"Header: {h}\")"

text = text.replace(old_header_call, new_header_call)

with open(fname, 'w', encoding='utf-8') as f:
    f.write(text)

print('Scope precedence patch applied')
