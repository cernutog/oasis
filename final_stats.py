import sys, os, yaml
sys.path.insert(0, os.getcwd())
from src.oas_diff.compatibility_analyzer import CompatibilityAnalyzer
from src.oas_diff.resolver import resolve_spec

old_spec_p = r"C:/EBA Clearing/APIs/Source OAS/20260323/EBACL_RT1_20260323_Openapi3.0-SWIFT_RT1_API_Participants_5_0_v20260323.yaml"
new_spec_p = r"C:/EBA Clearing/APIs/Generated OAS/RT1 API Participants/2026Q4/generated_oas_3.0_SWIFT.yaml"

with open(old_spec_p, 'r', encoding='utf-8') as f: s1 = yaml.safe_load(f)
with open(new_spec_p, 'r', encoding='utf-8') as f: s2 = yaml.safe_load(f)

res1 = resolve_spec(s1)
res2 = resolve_spec(s2)

# Ensure Strat 3 is DISABLED inside the actual file first!
# I already did that in Step 6172.

analyzer = CompatibilityAnalyzer(res1.get('paths',{}), res2.get('paths',{}), res1.get('components',{}), res2.get('components',{}))
issues = analyzer.analyze()

print(f"TOTAL ISSUES: {len(issues)}")
desc = [i for i in issues if i.issue_type == "Description Change"]
print(f"DESCRIPTION ISSUES: {len(desc)}")

lac_count = len([i for i in issues if "LacAmount" in (i.schema_name or "")])
print(f"ISSUES LINKED TO LacAmount SCHEMA: {lac_count}")

base_count = len([i for i in issues if "base" in i.item_name])
print(f"ISSUES LINKED TO 'base' property: {base_count}")
