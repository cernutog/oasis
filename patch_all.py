import os
import re

print("1. Patching resolver.py to inject x-ref...")
r_name = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\resolver.py'
with open(r_name, 'r', encoding='utf-8') as f:
    text = f.read()

old_resolver_merge = '''                    merged = copy.deepcopy(resolved_target) if isinstance(resolved_target, dict) else resolved_target
                    if isinstance(merged, dict):
                        for k, v in node.items():'''

new_resolver_merge = '''                    merged = copy.deepcopy(resolved_target) if isinstance(resolved_target, dict) else resolved_target
                    if isinstance(merged, dict):
                        if 'x-ref' not in merged: merged['x-ref'] = ref_path
                        for k, v in node.items():'''

text = text.replace(old_resolver_merge, new_resolver_merge)

with open(r_name, 'w', encoding='utf-8') as f:
    f.write(text)



print("2. Patching compatibility_analyzer.py...")
a_name = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\compatibility_analyzer.py'
with open(a_name, 'r', encoding='utf-8') as f:
    text = f.read()

# Add schema_name to dataclass
text = text.replace('    old_val: Any = None\n    new_val: Any = None', '    old_val: Any = None\n    new_val: Any = None\n    schema_name: str = "-"')

# Update _compare_schemas args
old_compare_def = 'def _compare_schemas(self, path: str, method: str, location: str, s1: Dict, s2: Dict, item_name_prefix: str, visited=None):'
new_compare_def = 'def _compare_schemas(self, path: str, method: str, location: str, s1: Dict, s2: Dict, item_name_prefix: str, current_schema: str = "-", visited=None):'
text = text.replace(old_compare_def, new_compare_def)

# Inject Lookup of x-ref
old_cycle_det = '''        # Cycle detection
        pair_id = (id(s1), id(s2))
        if pair_id in visited:
            return
        visited.add(pair_id)'''

new_cycle_det = '''        # Cycle detection
        pair_id = (id(s1), id(s2))
        if pair_id in visited:
            return
        visited.add(pair_id)

        def _get_s_name(s):
            if isinstance(s, dict):
                ref = s.get('x-ref')
                if ref: return ref.split('/')[-1]
            return None
        n1 = _get_s_name(s1)
        n2 = _get_s_name(s2)
        if n1 or n2: current_schema = n1 or n2'''

text = text.replace(old_cycle_det, new_cycle_det)

# Pass current_schema into recursive calls of _compare_schemas
text = re.sub(
    r'(self\._compare_schemas\(path, method, location, props1\[p\], props2\[p\], [^\n]+?)(\s*,\s*visited\))',
    r'\1, current_schema\2',
    text
)

text = re.sub(
    r'(self\._compare_schemas\(path, method, location, s1\[\'items\'\], s2\[\'items\'\], [^\n]+?)\s*,\s*visited\)',
    r'\1, current_schema, visited)',
    text
)

# Replace all isues.append inside CompatibilityAnalyzer
# Use regex to find `self.issues.append(CompatibilityIssue(....))` and inject `schema_name=current_schema` inside the brackets.
def add_schema_name(match):
    inner = match.group(1)
    if 'schema_name=' not in inner:
        # Check if it was called from _compare_schemas or its inner scopes by looking at position
        # Inside _compare_schemas we have current_schema variable.
        return f'self.issues.append(CompatibilityIssue({inner}, schema_name=current_schema))'
    return match.group(0)

# Apply to append commands that are on a single line
text = re.sub(r'self\.issues\.append\(CompatibilityIssue\(([^)]+?)\)\)', add_schema_name, text)

# For multiline appends (less common but let's check)
# Safety check: if there is multi-line on self.issues.append?
# Standardizing multiline appends back to single line or manual replace for params?
# Parameter appends don't have current_schema. They should have current_schema="-" or something.
# We will just write a specific sub inside `_compare_schemas` scope!

with open(a_name, 'w', encoding='utf-8') as f:
    f.write(text)



print("3. Patching generator.py summary column & widths...")
g_name = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(g_name, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix widths
old_widths = 'widths_s = [Inches(0.3), Inches(1.4), Inches(1.8), Inches(2.8), Inches(0.7)]'
new_widths = 'widths_s = [Inches(0.5), Inches(1.4), Inches(1.4), Inches(2.9), Inches(0.8)]'
text = text.replace(old_widths, new_widths)

# Update schema populate loop in Summary
old_summary_map_load = '''             if key not in schema_map: schema_map[key] = set()
             schema_map[key].add(issue.item_name if issue.item_name else (issue.location or "-"))'''

new_summary_map_load = '''             if key not in schema_map: schema_map[key] = set()
             schema_map[key].add(issue.schema_name)'''

text = text.replace(old_summary_map_load, new_summary_map_load)

with open(g_name, 'w', encoding='utf-8') as f:
     f.write(text)

print("Done all")
