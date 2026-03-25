import os
import re

fname = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\compatibility_analyzer.py'
with open(fname, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update dataclass default to "Schema" if unnamed and recursive, OR just leave it as can be set generally.
# Default in dataclass can be "-" still, but we'll explicitly pass explicit names for direct operation hooks!

# 2. Add schema_name="Operation" to operation description change
text = text.replace(
    'self.issues.append(CompatibilityIssue(path, method, "Operation", "description", "Description Change", "Description changed", severity="INFO", old_val=d1, new_val=d2))',
    'self.issues.append(CompatibilityIssue(path, method, "Operation", "description", "Description Change", "Description changed", severity="INFO", old_val=d1, new_val=d2, schema_name="Operation"))'
)

# 3. Request Body appends
text = text.replace(
    'self.issues.append(CompatibilityIssue(path, method, "Request Body", "-", "Removed", "Request body was removed in new spec."))',
    'self.issues.append(CompatibilityIssue(path, method, "Request Body", "-", "Removed", "Request body was removed in new spec.", schema_name="Request Body"))'
)
text = text.replace(
    'self.issues.append(CompatibilityIssue(path, method, "Request Body", "-", "Added", "Request body was added in new spec."))',
    'self.issues.append(CompatibilityIssue(path, method, "Request Body", "-", "Added", "Request body was added in new spec.", schema_name="Request Body"))'
)

# 4. _compare_parameters descriptions and required
text = text.replace(
    'self.issues.append(CompatibilityIssue(path, method, f"Parameter ({location})", name, "Constraint Mismatch", f"Property \'required\' changed from {p1.get(\'required\')} to {p2.get(\'required\')}"))',
    'self.issues.append(CompatibilityIssue(path, method, f"Parameter ({location})", name, "Constraint Mismatch", f"Property \'required\' changed from {p1.get(\'required\')} to {p2.get(\'required\')}\", schema_name=f\"Parameter ({name})\"))'
)

text = text.replace(
    'self.issues.append(CompatibilityIssue(path, method, f"Parameter ({location})", name, "Description Change", "Description changed", severity="INFO", old_val=d1, new_val=d2))',
    'self.issues.append(CompatibilityIssue(path, method, f"Parameter ({location})", name, "Description Change", "Description changed", severity="INFO", old_val=d1, new_val=d2, schema_name=f"Parameter ({name})"))'
)

with open(fname, 'w', encoding='utf-8') as f:
    f.write(text)



print("Patching generator column header...")
fname_g = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\generators\compatibility_generator.py'
with open(fname_g, 'r', encoding='utf-8') as f:
    text_g = f.read()

text_g = text_g.replace("hdr[2].text = 'Schema'", "hdr[2].text = 'Scope'")

with open(fname_g, 'w', encoding='utf-8') as f:
    f.write(text_g)

print('Done scope patch')
