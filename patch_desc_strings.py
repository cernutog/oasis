import os

fname = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\compatibility_analyzer.py'
with open(fname, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Description Change
# Old: "Description changed"
old_desc = '"Description changed"'
new_desc = 'f"Property \'{item_name_prefix}\' description changed" if item_name_prefix and item_name_prefix != "-" else "Description changed"'
text = text.replace(old_desc, new_desc)

# Restore Parameter description change string which shouldn't be patched because it's localized.
# Wait, let's fix the specific instances instead.
text = text.replace('f"Property \'{item_name_prefix}\' description changed" if item_name_prefix and item_name_prefix != "-" else "Description changed", severity="INFO", old_val=d1', '"Description changed", severity="INFO", old_val=d1')
# Same for operation description
text = text.replace('f"Property \'{item_name_prefix}\' description changed" if item_name_prefix and item_name_prefix != "-" else "Description changed", severity="INFO", old_val=d1, new_val=d2, schema_name="Operation"', '"Description changed", severity="INFO", old_val=d1, new_val=d2, schema_name="Operation"')

# 2. Update Enum Order
# Old: f"Constraint 'enum' order changed"
old_enum = 'f"Constraint \'enum\' order changed"'
new_enum = 'f"Property \'{item_name_prefix}\' constraint \'enum\' order changed" if item_name_prefix and item_name_prefix != "-" else "Constraint \'enum\' order changed"'
text = text.replace(old_enum, new_enum)

# 3. Update Generic Constraint
# Old: f"Constraint '{c}' changed"
old_c = 'f"Constraint \'{c}\' changed"'
new_c = 'f"Property \'{item_name_prefix}\' constraint \'{c}\' changed" if item_name_prefix and item_name_prefix != "-" else f"Constraint \'{c}\' changed"'
text = text.replace(old_c, new_c)

# 4. Update Value Mismatch
# Old: f"Value changed from {s1} to {s2}"
old_v = 'f"Value changed from {s1} to {s2}"'
new_v = 'f"Property \'{item_name_prefix}\' value changed from {s1} to {s2}" if item_name_prefix and item_name_prefix != "-" else f"Value changed from {s1} to {s2}"'
text = text.replace(old_v, new_v)

# 5. Update array removed and added.
# Old: "Array item definition removed in new spec."
old_arr_r = '"Array item definition removed in new spec."'
new_arr_r = 'f"Property \'{item_name_prefix}\' array item definition removed in new spec." if item_name_prefix and item_name_prefix != "-" else "Array item definition removed in new spec."'
text = text.replace(old_arr_r, new_arr_r)

old_arr_a = '"Array item definition added in new spec."'
new_arr_a = 'f"Property \'{item_name_prefix}\' array item definition added in new spec." if item_name_prefix and item_name_prefix != "-" else "Array item definition added in new spec."'
text = text.replace(old_arr_a, new_arr_a)

# 6. Update regular property removed/added/renamed
# Since prop_path is already the relative path, we can use it.
old_prop_r = '"Property removed in new spec."'
new_prop_r = 'f"Property \'{prop_path}\' removed in new spec."'
text = text.replace(old_prop_r, new_prop_r)

old_prop_a = '"Property added in new spec."'
new_prop_a = 'f"Property \'{prop_path}\' added in new spec."'
text = text.replace(old_prop_a, new_prop_a)

old_prop_ren = 'f"Property renamed to \'{a_prop}\' in new spec."'
new_prop_ren = 'f"Property \'{prop_path_old}\' renamed to \'{a_prop}\' in new spec."'
text = text.replace(old_prop_ren, new_prop_ren)

with open(fname, 'w', encoding='utf-8') as f:
    f.write(text)

print('Strings patched successfully')
