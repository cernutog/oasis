import sys, os, yaml
sys.path.insert(0, os.getcwd())
from src.oas_diff.compatibility_analyzer import CompatibilityAnalyzer
from src.oas_diff.resolver import resolve_spec

# Re-apply the analyzer without the dot-filter
path = r'c:\Users\giuse\.gemini\antigravity\scratch\OASIS\src\oas_diff\compatibility_analyzer.py'
with open(path, 'r', encoding='utf-8') as f: lines = f.readlines()
with open(path, 'w', encoding='utf-8') as f:
    for line in lines:
        if "if not item_name_prefix or '.' not in item_name_prefix:" in line:
            continue
        if "self.issues.append(CompatibilityIssue(path, method, location, item_name_prefix, \"Description Change\", \"Description changed\", old_value=v1, new_value=v2, schema_name=schema_name))" in line:
            # Shift back
            f.write(line.replace("                    ", "            "))
        else:
            f.write(line)

from src.oas_diff.compatibility_analyzer import CompatibilityAnalyzer # re-import

old_spec_p = r"C:/EBA Clearing/APIs/Source OAS/20260323/EBACL_RT1_20260323_Openapi3.0-SWIFT_RT1_API_Participants_5_0_v20260323.yaml"
new_spec_p = r"C:/EBA Clearing/APIs/Generated OAS/RT1 API Participants/2026Q4/generated_oas_3.0_SWIFT.yaml"

with open(old_spec_p, 'r', encoding='utf-8') as f: s1 = yaml.safe_load(f)
with open(new_spec_p, 'r', encoding='utf-8') as f: s2 = yaml.safe_load(f)

res1 = resolve_spec(s1)
res2 = resolve_spec(s2)

analyzer = CompatibilityAnalyzer(res1.get('paths',{}), res2.get('paths',{}), res1.get('components',{}), res2.get('components',{}))
issues = analyzer.analyze()

desc_issues = [i for i in issues if i.issue_type == "Description Change"]
print(f"TOTAL DESCRIPTION ISSUES: {len(desc_issues)}")
for i, iss in enumerate(desc_issues[:100]):
    print(f"{i+1}. {iss.item_name} | {iss.location}")
