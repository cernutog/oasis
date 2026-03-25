import os

fname = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\compatibility_analyzer.py'
with open(fname, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix child schemas recursion inside _compare_schemas properties loop
old_recurse = "self._compare_schemas(path, method, location, props1[prop], props2[prop], prop_path, visited)"
new_recurse = "self._compare_schemas(path, method, location, props1[prop], props2[prop], prop_path, current_schema, visited)"

text = text.replace(old_recurse, new_recurse)

with open(fname, 'w', encoding='utf-8') as f:
    f.write(text)

print('Argument alignment fixed')
